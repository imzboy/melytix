from Systems.Google.GoogleAuth import auth_credentials

from googleapiclient.discovery import build

def get_site_list(token: str):
    webmasters_service = webmasters_service = build('searchconsole', 'v1', http=auth_credentials(token))
    site_list = webmasters_service.sites().list().execute()
    if site_list.get('siteEntry'):

        verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                            if s['permissionLevel'] != 'siteUnverifiedUser'
                            and s['siteUrl'][:4] == 'http']
        return verified_sites_urls
    return None

def make_sc_request(token, site_uri, start_date, end_date):
    service = build('searchconsole', 'v1', http=auth_credentials(token))
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['date']
    }
    response = service.searchanalytics().query(siteUrl=site_uri, body=request).execute()
    return response
