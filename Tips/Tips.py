from Tips.Tip import Tip


def ctr_of_all_users(metrics: dict):
    ctr = metrics.get('sc_ctr')
    if ctr:
        counter = 0;
        for item in ctr:
            if item < 1.0: # if 100.0 = 100% \ 1.0 = 1%
                counter += 1

        if float(len(ctr) / 100 * 40) < counter:
            return True

    return False


ctr_of_all_search_Console_user = Tip(
    category='SEO',
    title = 'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
    description = 'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )',
    analytics_func=ctr_of_all_users,
    is_human_created=False
)

def return_tips():
    return [ctr_of_all_search_Console_user]
