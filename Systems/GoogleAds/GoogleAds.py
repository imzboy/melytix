from google.ads.google_ads.client import GoogleAdsClient
from google.protobuf.json_format import MessageToJson
import json
from Systems.Google.GoogleAuth import CLIENT_ID, CLIENT_SECRET
from Systems.GoogleAds.views import DEVELOPER_TOKEN
from user.models import User
from Utils.FacebookUtils import create_list_of_dates
metrics = [
    'absoluteTopImpressionPercentage',
    'activeViewCpm',
    'activeViewCtr',
    'activeViewImpressions',
    'activeViewMeasurability',
    'activeViewMeasurableCostMicros',
    'activeViewMeasurableImpressions',
    'activeViewViewability',
    'allConversions',
    'allConversionsByConversionDate',
    'allConversionsFromInteractionsRate',
    'allConversionsValue',
    'allConversionsValueByConversionDate',
    'averageCost',
    'averageCpc',
    'averageCpe',
    'averageCpm',
    'averageCpv',
    'averagePageViews',
    'averageTimeOnSite',
    'bounceRate',
    'clicks',
    'contentBudgetLostImpressionShare',
    'contentImpressionShare',
    'contentRankLostImpressionShare',
    'conversions',
    'conversionsByConversionDate',
    'conversionsFromInteractionsRate',
    'conversionsValue',
    'conversionsValueByConversionDate',
    'costMicros',
    'costPerAllConversions',
    'costPerConversion',
    'costPerCurrentModelAttributedConversion',
    'crossDeviceConversions',
    'ctr',
    'currentModelAttributedConversions',
    'currentModelAttributedConversionsFromInteractionsRate',
    'currentModelAttributedConversionsFromInteractionsValuePerInteraction',
    'currentModelAttributedConversionsValue',
    'currentModelAttributedConversionsValuePerCost',
    'engagementRate',
    'engagements',
    'gmailForwards',
    'gmailSaves',
    'gmailSecondaryClicks',
    'impressions',
    'interactionEventTypes',
    'interactionRate',
    'interactions',
    'invalidClickRate',
    'invalidClicks',
    'percentNewVisitors',
    'phoneCalls',
    'phoneImpressions',
    'phoneThroughRate',
    'relativeCtr',
    'searchAbsoluteTopImpressionShare',
    'searchBudgetLostAbsoluteTopImpressionShare',
    'searchBudgetLostImpressionShare',
    'searchBudgetLostTopImpressionShare',
    'searchClickShare',
    'searchExactMatchImpressionShare',
    'searchImpressionShare',
    'searchRankLostAbsoluteTopImpressionShare',
    'searchRankLostImpressionShare',
    'searchRankLostTopImpressionShare',
    'searchTopImpressionShare',
    'topImpressionPercentage',
    'valuePerAllConversions',
    'valuePerAllConversionsByConversionDate',
    'valuePerConversion',
    'valuePerConversionsByConversionDate',
    'valuePerCurrentModelAttributedConversion',
    'videoQuartileP100Rate',
    'videoQuartileP25Rate',
    'videoQuartileP50Rate',
    'videoQuartileP75Rate',
    'videoViewRate',
    'videoViews'
]

def google_ads_query_metrics(token: str, start_date, end_date):
    user = User.get(auth_token=token)
    customer_id = user.connected_systems.get('google_ads').get('customer_id')
    account_id = user.connected_systems.get('google_ads').get('account_id')

    access_token, refresh_token = User.get_g_tokens(token)
    request_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'developer_token': DEVELOPER_TOKEN,
        'refresh_token': refresh_token,
        'login_customer_id': customer_id,
    }

    data_client = GoogleAdsClient.load_from_dict(request_data)
    ga_service = data_client.get_service("GoogleAdsService", version="v6")

    # get all campaigns names
    query_name = """
            SELECT
              campaign.name
            FROM campaign"""
    campaign_names = []
    names = ga_service.search(account_id, query=query_name)
    for row in names:
        campaign_names.append(row.campaign.name)

    date_range = create_list_of_dates(start_date, end_date)
    result = create_helper_dict(campaign_names, date_range)

    for date in date_range:
        query = f"""
                SELECT
                  campaign.name,
                  metrics.absolute_top_impression_percentage,
                  metrics.active_view_cpm,
                  metrics.active_view_ctr,
                  metrics.active_view_impressions,
                  metrics.active_view_measurability,
                  metrics.active_view_measurable_cost_micros,
                  metrics.active_view_measurable_impressions,
                  metrics.active_view_viewability,
                  metrics.all_conversions,
                  metrics.all_conversions_by_conversion_date,
                  metrics.all_conversions_from_interactions_rate,
                  metrics.all_conversions_value,
                  metrics.all_conversions_value_by_conversion_date,
                  metrics.average_cost,
                  metrics.average_cpc,
                  metrics.average_cpe,
                  metrics.average_cpm,
                  metrics.average_cpv,
                  metrics.average_page_views,
                  metrics.average_time_on_site,
                  metrics.bounce_rate,
                  metrics.clicks,
                  metrics.content_budget_lost_impression_share,
                  metrics.content_impression_share,
                  metrics.content_rank_lost_impression_share,
                  metrics.conversions,
                  metrics.conversions_by_conversion_date,
                  metrics.conversions_from_interactions_rate,
                  metrics.conversions_value,
                  metrics.conversions_value_by_conversion_date,
                  metrics.cost_micros,
                  metrics.cost_per_all_conversions,
                  metrics.cost_per_conversion,
                  metrics.cost_per_current_model_attributed_conversion,
                  metrics.cross_device_conversions,
                  metrics.ctr,
                  metrics.current_model_attributed_conversions,
                  metrics.current_model_attributed_conversions_from_interactions_rate,
                  metrics.current_model_attributed_conversions_from_interactions_value_per_interaction,
                  metrics.current_model_attributed_conversions_value,
                  metrics.current_model_attributed_conversions_value_per_cost,
                  metrics.engagement_rate,
                  metrics.engagements,
                  metrics.gmail_forwards,
                  metrics.gmail_saves,
                  metrics.gmail_secondary_clicks,
                  metrics.impressions,
                  metrics.interaction_event_types,
                  metrics.interaction_rate,
                  metrics.interactions,
                  metrics.invalid_click_rate,
                  metrics.invalid_clicks,
                  metrics.percent_new_visitors,
                  metrics.phone_calls,
                  metrics.phone_impressions,
                  metrics.phone_through_rate,
                  metrics.relative_ctr,
                  metrics.search_absolute_top_impression_share,
                  metrics.search_budget_lost_absolute_top_impression_share,
                  metrics.search_budget_lost_impression_share,
                  metrics.search_budget_lost_top_impression_share,
                  metrics.search_click_share,
                  metrics.search_exact_match_impression_share,
                  metrics.search_impression_share,
                  metrics.search_rank_lost_absolute_top_impression_share,
                  metrics.search_rank_lost_impression_share,
                  metrics.search_rank_lost_top_impression_share,
                  metrics.search_top_impression_share,
                  metrics.top_impression_percentage,
                  metrics.value_per_all_conversions,
                  metrics.value_per_all_conversions_by_conversion_date,
                  metrics.value_per_conversion,
                  metrics.value_per_conversions_by_conversion_date,
                  metrics.value_per_current_model_attributed_conversion,
                  metrics.video_quartile_p100_rate,
                  metrics.video_quartile_p25_rate,
                  metrics.video_quartile_p50_rate,
                  metrics.video_quartile_p75_rate,
                  metrics.video_view_rate,
                  metrics.video_views,
                  metrics.view_through_conversions
                FROM campaign
                WHERE segments.date = '{date}'"""
        campaign_response = ga_service.search(account_id, query=query)

        for row in campaign_response:
            json_str = MessageToJson(row)
            dict_data = json.loads(json_str)

            for metric in metrics:
                campaign = dict_data.get('campaign').get('name')
                metric_data = dict_data.get('metrics').get(metric, 0)
                result[campaign][metric].append(metric_data)

    return result


def create_helper_dict(campaign_names: list, date_range: list):
    """{
    'campaign':
        {
            'metric': [],
            ...
        },
    'data': [dates]
    }"""
    result = {}
    for campaign in campaign_names:
        temp_metrics = {}
        for metric in metrics:
            temp_metrics.update({metric: []})
        result.update({campaign: temp_metrics})
    result.update({'dates': date_range})

    return result
