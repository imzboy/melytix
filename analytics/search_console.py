from analytics.base import MetricAnalyzer, MetricNotFoundException, Tip, Alert


class ScCtrAnalyzer(MetricAnalyzer):

    def init(self, metrics:dict):
        # super(MetricAnalyzer, self).__init__()
        self.metric = metrics.get('sc_ctr')
        if not self.metric:
            raise MetricNotFoundException('sc_ctr not found')

    def ctr_of_all_users(self, alg_id) -> Tip:
        all_ctr = self.metric[-7:]
        res = len([i for i in all_ctr if i < 1])
        if res/len(all_ctr) > 0.4:
            return Tip(_id=alg_id,category='SEO',
                title = 'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
                description = 'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте '
                            'заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )')
