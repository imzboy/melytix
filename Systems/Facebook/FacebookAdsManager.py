from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
import requests
import user as User
from Utils.FacebookUtils import fields, fill_campaign_metrics


def facebook_insights_query(token, start_time, end_time):
    user = User.query(auth_token=token)
    access_token = user.get('tokens').get('f_access_token')
    r = requests.get(f'https://graph.facebook.com/v9.0/me/adaccounts?access_token={access_token}')
    act_id = r.json()['data'][0]['id']
    FacebookAdsApi.init(access_token=access_token)
    my_account = AdAccount(act_id)
    campaigns = my_account.get_campaigns()

    data_metrics = {}
    for campaignId in campaigns:
        params = {'time_range': {'since': start_time, 'until': end_time},
                  'time_increment': 1,
                  'level': 'campaign'}
        response = campaignId.get_insights(params=params, fields=fields)

        result = []
        for item in response:
            result.append(dict(item))
        if len(result) != 0:
            campaign_name, campaign_metrics = fill_campaign_metrics(result)
            data_metrics.update({campaign_name: campaign_metrics})

    return data_metrics