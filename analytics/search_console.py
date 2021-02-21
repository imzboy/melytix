from analytics.base import MetricAnalyzer, Tip, Alert


class ScCtrAnalyzer(MetricAnalyzer):

    def init(self, metrics:dict):
        self.metric = metrics.get('sc_ctr')

    def ctr_of_all_users(metrics: dict, alg_id):
        all_ctr = metrics.get('sc_ctr', [])[-7:]
        res = len([i for i in all_ctr if i < 1])
        if res/len(all_ctr) > 0.4:
            return Tip(_id=alg_id,category='SEO',
                title = 'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
                description = 'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте '
                            'заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )')
