from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from user.models import User
from Utils.FacebookUtils import fields, fill_campaign_metrics


def facebook_insights_query(token, start_date, end_date):
    if (user := User.get(auth_token=token)):

        if(access_token := user.tokens.get('f_access_token')):

            if(account_id := user.connected_systems.get('facebook_insights').get('account_id')):
                FacebookAdsApi.init(access_token=access_token)
                my_account = AdAccount(account_id)
                campaigns = my_account.get_campaigns()
                data_metrics = {}
                for campaignId in campaigns:
                    params = {'time_range': {'since': start_date, 'until': end_date},
                              'time_increment': 1,
                              'level': 'campaign'}
                    response = campaignId.get_insights(params=params, fields=fields)

                    result = []
                    for item in response:
                        result.append(dict(item))

                    campaign_name = (dict(campaignId.api_get(fields=[AdAccount.Field.name]))).get('name')
                    campaign_metrics = fill_campaign_metrics(result, start_date, end_date)
                    data_metrics.update({campaign_name: campaign_metrics})
                return data_metrics

            return {'Error': 'no facebook ad account selected'}, 403

        return {'Error': 'no credentials provided'}, 403

    return {'Error': 'Wrong auth token'}, 403


