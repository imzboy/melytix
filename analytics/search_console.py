from analytics.base import MetricAnalyzer, MetricNotFoundException, Tip, Alert
from user.base import MetricsUserManager


class ScCtrAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: MetricsUserManager):
        self.metric = self.__get_metric(metrics, 'sc_ctr', 'search_console')
        if not self.metric:
            raise MetricNotFoundException('sc_ctr not found')

    def ctr_of_all_users(self, alg_id) -> Tip:
        all_ctr = self.metric[-7:]
        res = len([i for i in all_ctr if i < 0.1])
        if res >= 3:  # 40 % out of 7(days) = 2.8 ~ 3
            return Tip(
                _id=alg_id,
                category_en='SEO',
                title_en="CTR is less than 1 percent, people don't click on your snippet in the search!",
                description_en="Within a week, the CTR of all your ads reaches less than one percent - change the "
                               "title and description of the snippet in the search (by changing the <title> and "
                               "<description> of the page).",
                category='SEO',
                title='CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
                description='На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте '
                            'заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )')
