from Systems.Google.GoogleAuth import CLIENT_ID, CLIENT_SECRET


class GoogleReportsParser:
    # TODO: redo to handle multiple dimesions
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

        for row in self.reports[0].get('rows'):
            metrics['ga_dates'].append(self._parse_date(row.get('dimensions')[0]))

        for i, report in enumerate(self.reports):
            helper_dict = self.create_helper_dict(report)
            names = (item.get('name') for item in helper_dict.values())
            metrics.update({k: [] for k in names})

            for row in report.get('data').get('rows'):
                for i, metric in enumerate(row.get('metrics')[0].get('values')):
                    metrics[helper_dict[i].get('name')].append(helper_dict[i].get('type')(metric))

        return metrics


def prep_dash_metrics(sc_data: list) -> dict:
    metrics = {
        'sc_dates': [],
        'sc_clicks': [],
        'sc_impressions': [],
        'sc_ctr': [],
        'sc_position': [],
    }
    # TODO: refactor
    for x in sc_data['rows']:
        metrics['sc_dates'].append(x['keys'][0])
        metrics['sc_clicks'].append(x.get('clicks', 0))
        metrics['sc_impressions'].append(x.get('impressions', 0))
        metrics['sc_ctr'].append(x.get('ctr', 0))
        metrics['sc_position'].append(x.get('position', 0))

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