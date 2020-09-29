from Systems.Google.GoogleAuth import CLIENT_ID, CLIENT_SECRET

def prep_dash_metrics(ga_data: list = None, sc_data: list = None, yt_data: list = None) -> dict:
    metrics = {}
    # metrics = {
    #     'ga_sessions': [],
    #     'ga_users': [],
    #     'ga_pageViews': [],
    #     'ga_pageViewsPerSession': [],
    #     'ga_avgSessionDuration': [],
    #     'ga_bounces': [],
    #     'ga_percentNewSessions': [],
    #     'ga_user_dates': [],
    #     'ga_NewUser': [],
    #     'ga_ReturningUser': [],
    #     'ga_dates': [],
    #     'sc_clicks': [],
    #     'sc_impressions': [],
    #     'sc_ctr': [],
    #     'sc_position': [],
    #     'sc_dates': [],
    #     'yt_dates': [],
    #     'yt_estimatedMinutesWatched': [],
    #     'yt_views': [],
    #     'yt_likes': [],
    #     'yt_subscribersGained': [],
    #     'yt_dislikes': []
    # }

    if ga_data:
        metrics['ga_sessions'] = []
        metrics['ga_users'] = []
        metrics['ga_pageViews'] = []
        metrics['ga_pageViewsPerSession'] = []
        metrics['ga_avgSessionDuration'] = []
        metrics['ga_bounces'] = []
        metrics['ga_percentNewSessions'] = []
        # metrics['ga_user_dates'] = []
        # metrics['ga_NewUser'] = []
        # metrics['ga_ReturningUser'] = []
        metrics['ga_dates'] = []

    if sc_data:
        metrics['sc_clicks'] = []
        metrics['sc_impressions'] = []
        metrics['sc_ctr'] = []
        metrics['sc_position'] = []
        metrics['sc_dates'] = []

    if yt_data:
        metrics['yt_dates'] = []
        metrics['yt_estimatedMinutesWatched'] = []
        metrics['yt_views'] = []
        metrics['yt_likes'] = []
        metrics['yt_subscribersGained'] = []
        metrics['yt_dislikes'] = []

    if 'ga_sessions' in metrics:
        for x in ga_data['reports'][0]['data']['rows']:
            metrics['ga_dates'].append(str(
                x['dimensions'][0][0:4] + "-" + x['dimensions'][0][4:6] + "-" +
                x['dimensions'][0][6:8]))
            metrics['ga_sessions'].append(int(x['metrics'][0]['values'][0]))
            metrics['ga_users'].append(int(x['metrics'][0]['values'][1]))
            metrics['ga_pageViews'].append(int(x['metrics'][0]['values'][2]))
            metrics['ga_pageViewsPerSession'].append(float(x['metrics'][0]['values'][3]))
            metrics['ga_avgSessionDuration'].append(float(x['metrics'][0]['values'][4]))
            metrics['ga_bounces'].append(int(x['metrics'][0]['values'][5]))
            metrics['ga_percentNewSessions'].append(float(x['metrics'][0]['values'][6]))

    if 'sc_clicks' in metrics:
        for x in sc_data['rows']:
            metrics['sc_dates'].append(x['keys'][0])
            metrics['clicks'].append(x['clicks'])
            metrics['impressions'].append(x['impressions'])
            metrics['ctr'].append(x['ctr'])
            metrics['position'].append(x['position'])

    if 'yt_dates' in metrics:
        pass

    # TODO: This does not work
    # UsersTypesTemp = {
    #     'new_users_dates': [],
    #     'new_users': [],
    #     'ret_users_dates': [],
    #     'ret_users': []
    # }
    # for x in ga_data['reports'][1]['data']['rows']:
    #     if x['dimensions'][0] == 'New Visitor':
    #         UsersTypesTemp['new_users_dates'].append(int(x['dimensions'][1]))  # 20200403 - int
    #         UsersTypesTemp['new_users'].append(int(x['metrics'][0]['values'][0]))
    #     else:
    #         UsersTypesTemp['ret_users_dates'].append(int(x['dimensions'][1]))
    #         UsersTypesTemp['ret_users'].append(int(x['metrics'][0]['values'][0]))

    # metrics['ga_dates'] = UsersTypesTemp['new_users_dates'] + UsersTypesTemp['ret_users_dates']
    # metrics['ga_dates'].sort()  # sort by date
    # metrics['ga_dates'] = list(dict.fromkeys(metrics['ga_dates']))  # remove duplicates

    # for date in metrics['ga_dates']:
    #     for x in ga_data['reports'][0]['data']['rows']:
    #         if date == x['dimensions'][0]:  # looking for same dates
    #             if x['dimensions'][0] == 'New Visitors':
    #                 metrics['NewUser'].append(int(x['metrics'][0]['values'][0]))
    #             else:
    #                 metrics['NewUser'].append(0)
    #             if x['dimensions'][0] == "Returning Visitor":
    #                 metrics['ReturningUser'].append(int(x['metrics'][0]['values'][0]))
    #             else:
    #                 metrics['ReturningUser'].append(0)
    # print(UsersTypesTemp)
    # # TODO: make combine 4 lists into 3 lists

    return metrics


def prep_db_metrics(ga_data: list = None, sc_data: list = None, yt_data: list = None) -> dict:
    metrics = {}
    # metrics = {
    #     'ga_sessions': int,
    #     'ga_users': int,
    #     'ga_pageViews': int,
    #     'ga_pageViewsPerSession': int,
    #     'ga_avgSessionDuration': int,
    #     'ga_bounces': int,
    #     'ga_percentNewSessions': int,
    #     'ga_user_dates': string,
    #     'ga_NewUser': int,
    #     'ga_ReturningUser': int,
    #     'ga_dates': string,
    #     'sc_clicks': int,
    #     'sc_impressions': int,
    #     'sc_ctr': int,
    #     'sc_position': int,
    #     'sc_dates': string,
    #     'yt_dates': string,
    #     'yt_estimatedMinutesWatched': int,
    #     'yt_views': int,
    #     'yt_likes': int,
    #     'yt_subscribersGained': int,
    #     'yt_dislikes': int
    # }

    if ga_data:
        metrics['ga_sessions'] = 0
        metrics['ga_users'] = 0
        metrics['ga_pageViews'] = 0
        metrics['ga_pageViewsPerSession'] = 0
        metrics['ga_avgSessionDuration'] = 0
        metrics['ga_bounces'] = 0
        metrics['ga_percentNewSessions'] = 0
        # metrics['ga_user_dates'] = 0
        # metrics['ga_NewUser'] = 0
        # metrics['ga_ReturningUser'] = 0
        metrics['ga_dates'] = 0

    if sc_data:
        metrics['sc_clicks'] = 0
        metrics['sc_impressions'] = 0
        metrics['sc_ctr'] = 0
        metrics['sc_position'] = 0
        metrics['sc_dates'] = 0

    if yt_data:
        metrics['yt_dates'] = 0
        metrics['yt_estimatedMinutesWatched'] = 0
        metrics['yt_views'] = 0
        metrics['yt_likes'] = 0
        metrics['yt_subscribersGained'] = 0
        metrics['yt_dislikes'] = 0

    if 'ga_sessions' in metrics:
        for x in ga_data['reports'][0]['data']['rows']:
            metrics['ga_dates'].append(str(
                x['dimensions'][0][0:4] + "-" + x['dimensions'][0][4:6] + "-" +
                x['dimensions'][0][6:8]))
            metrics['ga_sessions'].append(int(x['metrics'][0]['values'][0]))
            metrics['ga_users'].append(int(x['metrics'][0]['values'][1]))
            metrics['ga_pageViews'].append(int(x['metrics'][0]['values'][2]))
            metrics['ga_pageViewsPerSession'].append(float(x['metrics'][0]['values'][3]))
            metrics['ga_avgSessionDuration'].append(float(x['metrics'][0]['values'][4]))
            metrics['ga_bounces'].append(int(x['metrics'][0]['values'][5]))
            metrics['ga_percentNewSessions'].append(float(x['metrics'][0]['values'][6]))

    if 'sc_clicks' in metrics:
        for x in sc_data['rows']:
            metrics['sc_dates'].append(x['keys'][0])
            metrics['clicks'].append(x['clicks'])
            metrics['impressions'].append(x['impressions'])
            metrics['ctr'].append(x['ctr'])
            metrics['position'].append(x['position'])

    if 'yt_dates' in metrics:
        pass

    # TODO: This does not work
    # UsersTypesTemp = {
    #     'new_users_dates': 0,
    #     'new_users': 0,
    #     'ret_users_dates': 0,
    #     'ret_users': 0
    # }
    # for x in ga_data['reports'][1]['data']['rows']:
    #     if x['dimensions'][0] == 'New Visitor':
    #         UsersTypesTemp['new_users_dates'].append(int(x['dimensions'][1]))  # 20200403 - int
    #         UsersTypesTemp['new_users'].append(int(x['metrics'][0]['values'][0]))
    #     else:
    #         UsersTypesTemp['ret_users_dates'].append(int(x['dimensions'][1]))
    #         UsersTypesTemp['ret_users'].append(int(x['metrics'][0]['values'][0]))

    # metrics['ga_dates'] = UsersTypesTemp['new_users_dates'] + UsersTypesTemp['ret_users_dates']
    # metrics['ga_dates'].sort()  # sort by date
    # metrics['ga_dates'] = list(dict.fromkeys(metrics['ga_dates']))  # remove duplicates

    # for date in metrics['ga_dates']:
    #     for x in ga_data['reports'][0]['data']['rows']:
    #         if date == x['dimensions'][0]:  # looking for same dates
    #             if x['dimensions'][0] == 'New Visitors':
    #                 metrics['NewUser'].append(int(x['metrics'][0]['values'][0]))
    #             else:
    #                 metrics['NewUser'].append(0)
    #             if x['dimensions'][0] == "Returning Visitor":
    #                 metrics['ReturningUser'].append(int(x['metrics'][0]['values'][0]))
    #             else:
    #                 metrics['ReturningUser'].append(0)
    # print(UsersTypesTemp)
    # # TODO: make combine 4 lists into 3 lists

    return metrics