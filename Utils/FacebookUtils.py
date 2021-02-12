import copy
from datetime import datetime, timedelta

from facebook_business.adobjects.adsinsights import AdsInsights

fields = [
    AdsInsights.Field.account_currency,
    AdsInsights.Field.account_id,
    AdsInsights.Field.account_name,
    AdsInsights.Field.action_values,
    AdsInsights.Field.actions,
    AdsInsights.Field.age_targeting,
    AdsInsights.Field.auction_bid,
    AdsInsights.Field.auction_competitiveness,
    AdsInsights.Field.auction_max_competitor_bid,
    AdsInsights.Field.buying_type,
    AdsInsights.Field.campaign_id,
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.canvas_avg_view_percent,
    AdsInsights.Field.canvas_avg_view_time,
    AdsInsights.Field.catalog_segment_actions,
    AdsInsights.Field.catalog_segment_value,
    AdsInsights.Field.catalog_segment_value_mobile_purchase_roas,
    AdsInsights.Field.catalog_segment_value_omni_purchase_roas,
    AdsInsights.Field.catalog_segment_value_website_purchase_roas,
    AdsInsights.Field.clicks,
    AdsInsights.Field.conversion_values,
    AdsInsights.Field.conversions,
    AdsInsights.Field.converted_product_quantity,
    AdsInsights.Field.converted_product_value,
    AdsInsights.Field.cost_per_15_sec_video_view,
    AdsInsights.Field.cost_per_2_sec_continuous_video_view,
    AdsInsights.Field.cost_per_action_type,
    AdsInsights.Field.cost_per_ad_click,
    AdsInsights.Field.cost_per_conversion,
    AdsInsights.Field.cost_per_dda_countby_convs,
    AdsInsights.Field.cost_per_inline_link_click,
    AdsInsights.Field.cost_per_inline_post_engagement,
    AdsInsights.Field.cost_per_one_thousand_ad_impression,
    AdsInsights.Field.cost_per_outbound_click,
    AdsInsights.Field.cost_per_store_visit_action,
    AdsInsights.Field.cost_per_thruplay,
    AdsInsights.Field.cost_per_unique_action_type,
    AdsInsights.Field.cost_per_unique_click,
    AdsInsights.Field.cost_per_unique_inline_link_click,
    AdsInsights.Field.cost_per_unique_outbound_click,
    AdsInsights.Field.cpc,
    AdsInsights.Field.cpm,
    AdsInsights.Field.cpp,
    AdsInsights.Field.created_time,
    AdsInsights.Field.ctr,
    AdsInsights.Field.date_start,
    AdsInsights.Field.date_stop,
    AdsInsights.Field.dda_countby_convs,
    AdsInsights.Field.estimated_ad_recall_rate_lower_bound,
    AdsInsights.Field.estimated_ad_recall_rate_upper_bound,
    AdsInsights.Field.estimated_ad_recallers_lower_bound,
    AdsInsights.Field.estimated_ad_recallers_upper_bound,
    AdsInsights.Field.frequency,
    AdsInsights.Field.full_view_impressions,
    AdsInsights.Field.full_view_reach,
    AdsInsights.Field.gender_targeting,
    AdsInsights.Field.impressions,
    AdsInsights.Field.inline_link_click_ctr,
    AdsInsights.Field.inline_link_clicks,
    AdsInsights.Field.inline_post_engagement,
    AdsInsights.Field.instant_experience_clicks_to_open,
    AdsInsights.Field.instant_experience_clicks_to_start,
    AdsInsights.Field.instant_experience_outbound_clicks,
    AdsInsights.Field.interactive_component_tap,
    AdsInsights.Field.labels,
    AdsInsights.Field.location,
    AdsInsights.Field.mobile_app_purchase_roas,
    AdsInsights.Field.objective,
    AdsInsights.Field.outbound_clicks,
    AdsInsights.Field.outbound_clicks_ctr,
    AdsInsights.Field.place_page_name,
    AdsInsights.Field.purchase_roas,
    AdsInsights.Field.qualifying_question_qualify_answer_rate,
    AdsInsights.Field.reach,
    AdsInsights.Field.social_spend,
    AdsInsights.Field.spend,
    AdsInsights.Field.store_visit_actions,
    AdsInsights.Field.unique_actions,
    AdsInsights.Field.unique_clicks,
    AdsInsights.Field.unique_ctr,
    AdsInsights.Field.unique_inline_link_click_ctr,
    AdsInsights.Field.unique_inline_link_clicks,
    AdsInsights.Field.unique_link_clicks_ctr,
    AdsInsights.Field.unique_outbound_clicks,
    AdsInsights.Field.unique_outbound_clicks_ctr,
    AdsInsights.Field.unique_video_view_15_sec,
    AdsInsights.Field.updated_time,
    AdsInsights.Field.video_15_sec_watched_actions,
    AdsInsights.Field.video_30_sec_watched_actions,
    AdsInsights.Field.video_avg_time_watched_actions,
    AdsInsights.Field.video_continuous_2_sec_watched_actions,
    AdsInsights.Field.video_p100_watched_actions,
    AdsInsights.Field.video_p25_watched_actions,
    AdsInsights.Field.video_p50_watched_actions,
    AdsInsights.Field.video_p75_watched_actions,
    AdsInsights.Field.video_p95_watched_actions,
    AdsInsights.Field.video_play_actions,
    AdsInsights.Field.video_play_curve_actions,
    AdsInsights.Field.video_play_retention_0_to_15s_actions,
    AdsInsights.Field.video_play_retention_20_to_60s_actions,
    AdsInsights.Field.video_play_retention_graph_actions,
    AdsInsights.Field.video_time_watched_actions,
    AdsInsights.Field.website_ctr,
    AdsInsights.Field.website_purchase_roas,
    AdsInsights.Field.wish_bid,

]

dict_helper = {
    'dates': [],
    'account_currency': [],
    'account_id': [],
    'account_name': [],
    'action_values': [],
    'actions': [],
    'age_targeting': [],
    'auction_bid': [],
    'auction_competitiveness': [],
    'auction_max_competitor_bid': [],
    'buying_type': [],
    'campaign_id': [],
    'campaign_name': [],
    'canvas_avg_view_percent': [],
    'canvas_avg_view_time': [],
    'catalog_segment_actions': [],
    'catalog_segment_value': [],
    'catalog_segment_value_mobile_purchase_roas': [],
    'catalog_segment_value_omni_purchase_roas': [],
    'catalog_segment_value_website_purchase_roas': [],
    'clicks': [],
    'conversion_values': [],
    'conversions': [],
    'converted_product_quantity': [],
    'converted_product_value': [],
    'cost_per_15_sec_video_view': [],
    'cost_per_2_sec_continuous_video_view': [],
    'cost_per_action_type': [],
    'cost_per_ad_click': [],
    'cost_per_conversion': [],
    'cost_per_dda_countby_convs': [],
    'cost_per_inline_link_click': [],
    'cost_per_inline_post_engagement': [],
    'cost_per_one_thousand_ad_impression': [],
    'cost_per_outbound_click': [],
    'cost_per_store_visit_action': [],
    'cost_per_thruplay': [],
    'cost_per_unique_action_type': [],
    'cost_per_unique_click': [],
    'cost_per_unique_inline_link_click': [],
    'cost_per_unique_outbound_click': [],
    'cpc': [],
    'cpm': [],
    'cpp': [],
    'created_time': [],
    'ctr': [],
    'date_start': [],
    'date_stop': [],
    'dda_countby_convs': [],
    'estimated_ad_recall_rate_lower_bound': [],
    'estimated_ad_recall_rate_upper_bound': [],
    'estimated_ad_recallers_lower_bound': [],
    'estimated_ad_recallers_upper_bound': [],
    'frequency': [],
    'full_view_impressions': [],
    'full_view_reach': [],
    'gender_targeting': [],
    'impressions': [],
    'inline_link_click_ctr': [],
    'inline_link_clicks': [],
    'inline_post_engagement': [],
    'instant_experience_clicks_to_open': [],
    'instant_experience_clicks_to_start': [],
    'instant_experience_outbound_clicks': [],
    'interactive_component_tap': [],
    'labels': [],
    'location': [],
    'mobile_app_purchase_roas': [],
    'objective': [],
    'outbound_clicks': [],
    'outbound_clicks_ctr': [],
    'place_page_name': [],
    'purchase_roas': [],
    'qualifying_question_qualify_answer_rate': [],
    'reach': [],
    'social_spend': [],
    'spend': [],
    'store_visit_actions': [],
    'unique_actions': [],
    'unique_clicks': [],
    'unique_ctr': [],
    'unique_inline_link_click_ctr': [],
    'unique_inline_link_clicks': [],
    'unique_link_clicks_ctr': [],
    'unique_outbound_clicks': [],
    'unique_outbound_clicks_ctr': [],
    'unique_video_view_15_sec': [],
    'updated_time': [],
    'video_15_sec_watched_actions': [],
    'video_30_sec_watched_actions': [],
    'video_avg_time_watched_actions': [],
    'video_continuous_2_sec_watched_actions': [],
    'video_p100_watched_actions': [],
    'video_p25_watched_actions': [],
    'video_p50_watched_actions': [],
    'video_p75_watched_actions': [],
    'video_p95_watched_actions': [],
    'video_play_actions': [],
    'video_play_curve_actions': [],
    'video_play_retention_0_to_15s_actions': [],
    'video_play_retention_20_to_60s_actions': [],
    'video_play_retention_graph_actions': [],
    'video_time_watched_actions': [],
    'website_ctr': [],
    'website_purchase_roas': [],
    'wish_bid': [],
}


def fill_campaign_metrics(metrics_list, start_date, end_date):
    campaign_metrics_in = copy.deepcopy(dict_helper)

    list_of_required_dates = create_list_of_dates(start_date, end_date)
    date_index = 0

    # Enumeration of metrics by dates
    for dict_metric in metrics_list:

        # fills metrics by 0 if campaign for this day hadn't activity
        while dict_metric.get('date_start') != list_of_required_dates[date_index]:
            fill_metrics_with_zeros(campaign_metrics_in, list_of_required_dates, date_index)
            date_index += 1

        date_index += 1

        # Gets names of metrics and its empty values from ready dictionary to fill it
        for metric_name, list_value in campaign_metrics_in.items():

            if metric_name == 'dates':
                campaign_metrics_in.get('dates').append(dict_metric.get('date_start'))
                continue

            # Gets needs metric from dict_metrics
            metric = dict_metric.get(metric_name)

            # Check metric for type
            if metric is None:
                list_value.append(0)
            elif isinstance(metric, list):
                for item_dict in metric:
                    for key, value in item_dict.items():
                        item_dict[key] = str_or_number(value)
                list_value.append(metric)
            else:
                list_value.append(str_or_number(metric))

    # fills metrics by 0 if campaign for this day hadn't activity
    # (if the metrics in the response run out, and the dates from the requirements are not)
    while date_index < len(list_of_required_dates):
        fill_metrics_with_zeros(campaign_metrics_in, list_of_required_dates, date_index)
        date_index += 1

    return campaign_metrics_in


# fills metrics by 0 if campaign for this day hadn't activity
def fill_metrics_with_zeros(campaign_metrics_in, list_of_required_dates, date_index):
    for metric_name, list_value in campaign_metrics_in.items():
        if metric_name == 'dates':
            campaign_metrics_in.get('dates').append(list_of_required_dates[date_index])
        else:
            list_value.append(0)


def str_or_number(s: str):
    if s.isdigit():
        return int(s)
    elif s.find('.') != -1:
        return float(s)
    return s


def create_list_of_dates(start_date, end_date):
    if start_date == 'today': start_date = datetime.now().date()
    elif isinstance(start_date, str): start_date = (datetime.strptime(start_date, "%Y-%m-%d")).date()
    if end_date == 'today': end_date = datetime.now().date()
    elif isinstance(end_date, str): end_date = (datetime.strptime(end_date, "%Y-%m-%d")).date()

    dates = []
    base = start_date
    i = 0
    while base != end_date:
        dates.append(base.strftime('%Y-%m-%d'))
        i += 1
        base = (start_date + timedelta(days=i))
    dates.append(end_date.strftime('%Y-%m-%d'))

    return dates


