from Systems.Google.GoogleAuth import CLIENT_ID, CLIENT_SECRET
class GoogleReportsParser:
    """A class for parsing google analytics reports"""
    def __init__(self, reports: dict):
        self.reports = reports.get('reports')
        self.types = {
            'INTEGER': int,
            'FLOAT': float,
            'PERCENT': float,
            'CURRENCY': float,
            'TIME': str,
            'METRIC_TYPE_UNSPECIFIED': str
        }

    def create_helper_dict(self, report: dict):
        """Creates a helper dict for managing metrics inside the report
           Unique for every report
           helper dict = {
               1(index of the metric):{
                   'type': int/float
                   'name': ga_sessions(or similar)
                    }}
        """
        helper_dict = {}
        metric_entries = report.get('columnHeader').get('metricHeader').get('metricHeaderEntries')
        for i, metric in enumerate(metric_entries):
            helper_dict[i] = {
                'name' : metric.get('name').replace(':', "_"),
                'type': self.types.get(metric.get('type'))
            }

        return helper_dict


    def _parse_date(self, date: str):
        """formats a date to match YYYY-MM-DD format"""
        return date[0:4] + "-" + date[4:6] + "-" + date[6:8]


    def parse(self):

        metrics = {
            'ga_dates': []
        }

        for report in self.reports:
            helper_dict = self.create_helper_dict(report)
            names = (item.get('name') for item in helper_dict.values())
            metrics.update({k: [] for k in names})

            for row in report.get('data').get('rows'):
                metrics['ga_dates'].append(self._parse_date(row.get('dimensions')[0]))

                for i, metric in enumerate(row.get('metrics')[0].get('values')):
                    metrics[helper_dict[i].get('name')].append(helper_dict[i].get('type')(metric))

        return metrics


def prep_dash_metrics(ga_data: list = None, sc_data: list = None, yt_data: list = None) -> dict:
    metrics = {}
    # TODO: refactor
    if 'sc_clicks' in metrics:
        for x in sc_data['rows']:
            metrics['sc_dates'].append(x['keys'][0])
            metrics['sc_clicks'].append(x.get('clicks', 0))
            metrics['sc_impressions'].append(x.get('impressions', 0))
            metrics['sc_ctr'].append(x.get('ctr', 0))
            metrics['sc_position'].append(x.get('position', 0))

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
            metrics['ga_dates'] = (str(
                x['dimensions'][0][0:4] + "-" + x['dimensions'][0][4:6] + "-" +
                x['dimensions'][0][6:8]))
            metrics['ga_sessions'] = (int(x['metrics'][0]['values'][0]))
            metrics['ga_users'] = (int(x['metrics'][0]['values'][1]))
            metrics['ga_pageViews'] = (int(x['metrics'][0]['values'][2]))
            metrics['ga_pageViewsPerSession'] = (float(x['metrics'][0]['values'][3]))
            metrics['ga_avgSessionDuration'] = (float(x['metrics'][0]['values'][4]))
            metrics['ga_bounces'] = (int(x['metrics'][0]['values'][5]))
            metrics['ga_percentNewSessions'] = (float(x['metrics'][0]['values'][6]))

    if 'sc_clicks' in metrics:
        for x in sc_data['rows']:
            metrics['sc_dates'] = (x['keys'][0])
            metrics['clicks'] = (x['clicks'])
            metrics['impressions'] = (x['impressions'])
            metrics['ctr'] = (x['ctr'])
            metrics['position'] = (x['position'])

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



def find_start_and_end_date(dates, strart_date, end_date):
    start_date_index = 0
    end_date_index = len(dates) - 1

    for i, date in enumerate(dates):
        if strart_date == date:
            print(strart_date, date)
            start_date_index = i

        if end_date == date:
            end_date_index = i
            break

    return (start_date_index, end_date_index)