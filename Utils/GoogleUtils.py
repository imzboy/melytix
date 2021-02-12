
class GoogleReportsParser:
    """A class for parsing google analytics reports"""

    def __init__(self, reports: dict, time_range: dict):
        self.reports = reports.get('reports')
        self.time_range = time_range
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
                    }
           }
        """
        helper_dict = {}
        metric_entries = report.get('columnHeader').get('metricHeader').get('metricHeaderEntries')
        for i, metric in enumerate(metric_entries):
            helper_dict[i] = {
                'name': metric.get('name').replace(':', "_"),
                'type': self.types.get(metric.get('type'))
            }
        return helper_dict

    def create_metrics_dict(self):
        """ Create dict with all metrics """
        helper_dict = {}
        metric_entries = self.reports[0].get('columnHeader').get('metricHeader').get('metricHeaderEntries')

        for metric in metric_entries:
            metric_name = metric.get('name').replace(':', "_")
            helper_dict[metric_name] = {}

        return helper_dict

    def _parse_date(self, date: str):
        """ Formats a date to match YYYY-MM-DD format """
        return date[0:4] + "-" + date[4:6] + "-" + date[6:8]

    def fill_metrics_by_zero(self, report: dict):
        """ Initialize each unique dimension with a list with zeros in a range of dates """
        result = {}
        prev_dimension = report.get('data').get('rows')[0].get('dimensions')[0]
        result.update({prev_dimension: [0] * len(self.time_range)})

        for row in report.get('data').get('rows'):
            current_dimension = row.get('dimensions')[0]
            if current_dimension != prev_dimension:
                result.update({current_dimension: [0] * len(self.time_range)})
                prev_dimension = current_dimension

        return result

    def parse(self):
        result = self.create_metrics_dict()

        for report in self.reports:

            helper_dict = self.create_helper_dict(report)

            for i, data_of_metric in helper_dict.items():
                metric_name = data_of_metric.get('name')
                metric_type = data_of_metric.get('type')
                current_dimension = report.get('columnHeader').get('dimensions')[0].replace(':', "_")
                dimensions = self.fill_metrics_by_zero(report)

                for row in report.get('data').get('rows'):
                    dimension = row.get('dimensions')[0]
                    date = self._parse_date(row.get('dimensions')[1])
                    index_of_data = self.time_range.get(date)
                    (dimensions.get(dimension))[index_of_data] = metric_type(row.get('metrics')[0].get('values')[i])

                result[metric_name].update({current_dimension: dimensions})

        return result


def prep_dash_metrics(sc_data: list) -> dict:
    metrics = {
        'sc_dates': [],
        'sc_clicks': [],
        'sc_impressions': [],
        'sc_ctr': [],
        'sc_position': [],
    }
    # TODO: refactor
    for row in sc_data['rows']:
        metrics['sc_dates'].append(row['keys'][0])
        metrics['sc_clicks'].append(row.get('clicks', 0))
        metrics['sc_impressions'].append(row.get('impressions', 0))
        metrics['sc_ctr'].append(row.get('ctr', 0))
        metrics['sc_position'].append(row.get('position', 0))

    return metrics


def find_start_and_end_date(dates, strart_date, end_date):
    start_date_index = 0
    end_date_index = len(dates) - 1

    for i, date in enumerate(dates):
        if strart_date == date:
            start_date_index = i

        if end_date == date:
            end_date_index = i
            break

    return (start_date_index, end_date_index)