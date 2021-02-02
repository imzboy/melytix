from Systems.Google.GoogleAuth import auth_credentials

from googleapiclient.discovery import build

def get_site_list(token: str):
    webmasters_service = build('webmasters', 'v3', http=auth_credentials(token))
    site_list = webmasters_service.sites().list().execute()

    verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                           if s['permissionLevel'] != 'siteUnverifiedUser'
                           and s['siteUrl'][:4] == 'http']
    return verified_sites_urls


def make_sc_request(token, site_uri, start_date, end_date):
    service = build('webmasters', 'v3', http=auth_credentials(token))
    request = {
        'startDate': start_date.date().isoformat(),
        'endDate': end_date.date().isoformat(),
        'dimensions': ['date']
    }
    response = service.searchanalytics().query(siteUrl=site_uri, body=request).execute()
    return response
