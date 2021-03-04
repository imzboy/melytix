from bson.objectid import ObjectId
from Systems.Google.GoogleAnalytics import generate_report_body
from Utils.FacebookUtils import create_list_of_dates
from Systems.Google.GoogleAuth import auth_credentials
from googleapiclient.discovery import build
from Utils import GoogleUtils
from user.models import User
import json
import os


def ga_totals(report, start_date, end_date, token):
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token), cache_discovery=False)
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    if response.get('reports')[0].get('data').get('rows'):
        parsed_response = GoogleUtils.GoogleTotalsReportsParser(response).parse()
        parsed_response.pop('ga_dates')
    else:
        l = len(create_list_of_dates(start_date, end_date))
        metrics = ['ga:sessions', 'ga:users', 'ga:pageviews',
                     'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                     'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                     'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue']
        parsed_response = {k: [0] * l for k in metrics}

    return parsed_response


def ga_child(report: list, start_date, end_date, token):
    # Google Analytics v4 api setup to make a request to google analytics
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token), cache_discovery=False)
    response = api_client.reports().batchGet(
        body={
            'reportRequests': report
        }).execute()

    dates = create_list_of_dates(start_date, end_date)

    if response.get('reports')[0].get('data').get('rows'):
        return  GoogleUtils.GoogleReportsParser(response, dates).parse()

    return GoogleUtils.fill_all_with_zeros(response, dates)

def ga(token, view_id, start_date, end_date):
    # Max of 10 metrics and 7 dimesions in one report body
    dimensions = ['ga:browser', 'ga:operatingSystem',
                  'ga:mobileDeviceBranding', 'ga:mobileInputSelector', 'ga:mobileDeviceModel',
                  'ga:mobileDeviceInfo', 'ga:deviceCategory', 'ga:browserSize', 'ga:country',
                  'ga:region', 'ga:language', 'ga:userAgeBracket', 'ga:userGender',
                  'ga:interestOtherCategory', 'ga:city']
    dates = create_list_of_dates(start_date, end_date)

    metrics = ['ga:sessions', 'ga:users', 'ga:pageviews',
                     'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
                     'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
                     'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue']
    result = {
        'ga_dates':dates,
        **{k.replace(':', '_'):{} for k in metrics}
    }
    for dimension in dimensions:

        report = generate_report_body(
            view_id=view_id,
            start_date=start_date,
            end_date=end_date,

            metrics=metrics,

            dimensions=['ga:date', dimension])
        res = ga_child(report, start_date, end_date, token)
        for metric_name, value in res.items():
            result[metric_name].update(**value)

    return result


almost_all_users = User.filter_only(fields={'metrics':True})
test_user = User.get_only(email='art-holst@gmail.com', fields={'metrics':True})
print('got users')
for i, user in enumerate(almost_all_users):
    if user.get('_id') == test_user.get('_id'):
        index = i

almost_all_users.pop(index)
print('poped user')

for user in almost_all_users:
    path = f'users_metrics/{str(user.get("_id"))}'
    print(f'working on {path}')
    if not os.path.exists(path):
        os.makedirs(path)
        print('created dir')
    with open(f'{path}/metrics.json', 'w') as f:
        f.write(json.dumps(user.get('metrics')))
        print(f'dumped user<{str(user.get("_id"))}> metrics to {path}/metrics.json','\n')

print('done with simple users')

test_metrics = test_user.get('metrics')
test_metrics.pop('google_analytics', {})
print('starting ga parsing')
token, view_id, start_date, end_date = 'fd7bb0e1c867916e57e2b2ba47abe7ac5c6d0fe6', '49893866', '2021-01-02', '2021-03-03'
ga_result = ga(token, view_id, start_date, end_date)
print('parsign success')
#add totals
totals_report = generate_report_body(
view_id=view_id,
start_date=start_date,
end_date=end_date,

metrics=['ga:sessions', 'ga:users', 'ga:pageviews',
            'ga:pageviewsPerSession', 'ga:avgSessionDuration', 'ga:bounces',
            'ga:percentNewSessions', 'ga:pageviews', 'ga:timeOnPage', 'ga:pageLoadTime',
            'ga:avgPageLoadTime', 'ga:transactionsPerSession', 'ga:transactionRevenue'],

dimensions=['ga:date'])
print('starting totals parsing')
totals = ga_totals(totals_report, start_date, end_date, token)
for metric, total in totals.items():
    ga_result[metric]['total']= total
print('totals added')
test_metrics['google_analytics'] = ga_result

path = f'users_metrics/{test_user.get("_id")}'
os.makedirs(path)
with open(f'{path}/metrics.json', 'w') as f:
        f.write(json.dumps(test_metrics))

print(f'Done check {path}/metrics.json')

