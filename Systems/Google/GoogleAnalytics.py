import user as User
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from Systems.Google.GoogleAuth import auth_credentials


def generate_report_body(view_id: str, start_date: str, end_date: str, metrics: list, dimensions: list):
    body_template = {
        'viewId': view_id,
        'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
        'metrics': [],
        'dimensions': [{'name': dimension} for dimension in dimensions],  # not optimized but i don't know how to do it otherwise
        "includeEmptyRows": True
    }

    # metric_tempalate = {'expression': '{}'}
    # dimension_template = {'name': '{}'}

    report_requests = []
    step = 10  # Max of 10 metrics per report body
    for i in range(0, len(metrics), step):
        metrics_slice = metrics[i:i+step]

        tmp_report_request = body_template.copy()
        tmp_report_request['metrics'] = [{'expression': metric} for metric in metrics_slice]
        report_requests.append(tmp_report_request)

    return report_requests


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
