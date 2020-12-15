import user as User
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from Systems.Google.GoogleAuth import auth_credentials


def generate_report_body(view_id: str, start_date: str, end_date: str, metrics: list, dimensions: list):
    body_template = {
        'viewId': view_id,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [],
        'dimensions': [],
        "includeEmptyRows": True
    }

    metric_tempalate = {'expression': '{}'}
    dimension_template = {'name': '{}'}



# Google analytics query and setup
def google_analytics_query(token, view_id, start_date, end_date):
    # Google Analytics v4 api setup to make a request to google analytics
    api_client = build(serviceName='analyticsreporting', version='v4', http=auth_credentials(token))
    # Max of 10 metrics in one request body
    response = api_client.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': view_id,
                    'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                    'metrics': [{'expression': 'ga:sessions'},
                                {'expression': 'ga:users'},
                                {'expression': 'ga:pageviews'},
                                {'expression': 'ga:pageviewsPerSession'},
                                {'expression': 'ga:avgSessionDuration'},
                                {'expression': 'ga:bounces'},
                                {'expression': 'ga:percentNewSessions'},
                                {'expression': 'ga:browser'},
                                {'expression': 'ga:browserVersion'},
                                {'expression': 'ga:operatingSystem'}],
                    'dimensions': [{'name': 'ga:date'}],
                    "includeEmptyRows": True
                },
                # {
                #     'viewId': view_id,
                #     'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                #     'metrics': [{'expression': 'ga:operatingSystemVersion'},
                #                 {'expression': 'ga:mobileDeviceBranding'},
                #                 {'expression': 'ga:mobileDeviceModel'},
                #                 {'expression': 'ga:mobileInputSelector'},
                #                 {'expression': 'ga:mobileDeviceInfo'},
                #                 {'expression': 'ga:deviceCategory'},
                #                 {'expression': 'ga:browserSize'},
                #                 {'expression': 'ga:country'},
                #                 {'expression': 'ga:region'},
                #                 {'expression': 'ga:city'}],
                #     'dimensions': [{'name': 'ga:date'}],
                #     "includeEmptyRows": True
                # },
                # ga:language
                # ga:pageviews
                # ga:timeOnPage
                # ga:pageLoadTime
                # ga:avgPageLoadTime
                # ga:transactionsPerSession
                # ga:transactionRevenue
                # ga:userAgeBracket
                # ga:userGender
                # ga:interestOtherCategory
                # TODO: metrics to add
                # {
                #     'viewId': view_id,
                #     'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
                #     'metrics': [{'expression': 'ga:adClicks'},
                #                 {'expression': 'ga:adCost'},
                #                 {'expression': 'ga:CPC'},
                #                 {'expression': 'ga:CTR'},
                #                 {'expression': 'ga:costPerConversion'}],
                #     'dimensions': [{'name': 'ga:adwordsCampaignID'},
                #                    {'name': 'ga:date'}],
                #     "includeEmptyRows": True
                # }
                #
            ]
        }).execute()
    # data = dump_data_for_melytips(response)
    return response


def g_get_viewid(account, web_property, token):
    service = build(serviceName='analytics', version='v3', http=auth_credentials(token))
    profiles = service.management().profiles().list(
        accountId=account,
        webPropertyId=web_property).execute()
    return profiles.get('items')[0].get('id')


def g_get_select_data(token: str):
    """Gets the property and web property in dict
       for a view id choosing drop down"""
    service = build(serviceName='analytics', version='v3', http=auth_credentials(token))
    # Get a list of all Google Analytics accounts for the authorized user.
    try:
        accounts_list = service.management().accounts().list().execute()
        if accounts_list.get('items'):
            accounts = []
            for x in range(accounts_list.get('totalResults')):
                accounts.append({'name': accounts_list.get('items')[x].get('name'),
                                'id': accounts_list.get('items')[x].get('id')})
            # Get a list of all the properties for all accounts.
            for x in accounts:
                response = service.management().webproperties().list(accountId=x.get('id')).execute()
                if response.get('items'):
                    webProperties = []
                    for k in range(response.get('totalResults')):
                        webProperties.append(
                            {'prop_name': response.get('items')[k].get('name'),
                            'prop_id': response.get('items')[k].get('id')})
                    x['webProperties'] = webProperties
            return accounts
    except HttpError:
        return {'error': 'User does not have any Google Analytics account.'}


def insert_ga_data_in_db(token, ga_data):
    User.db.find_one_and_update(
        {'auth_token': token},
        {'$set': {
            'G_Analytics.ga_data': ga_data
        }},
        upsert=False
    )
