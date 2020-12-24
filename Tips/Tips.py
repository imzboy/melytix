from Tips.Tip import Tip


def ctrOfAllSCUser(metrics: dict):
    ctr = metrics.get('sc_ctr')
    if ctr:
        counter = 0;
        for item in ctr:
            if item < 1.0: # if 100.0 = 100% \ 1.0 = 1%
                counter += 1

        if float(len(ctr) / 100 * 40) < counter:
            return True

    return False


CtrOfAllSearchConsoleUser = Tip(
    category='SEO',
    title = 'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
    description = 'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )',
    analytics_func=ctrOfAllSCUser,
    is_human_created=False
)

def return_tips():
    return [CtrOfAllSearchConsoleUser]
