from Alerts.Alert import Alert


def sessions_lower(metrics: dict):
    if metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 1] < metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 2]:
        return True
    return False

# New alerts Vova 24.10.2020
#
#

def crytical_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    min_ga_users = ga_users[0]
    for i in range(len(ga_users)):
        if min_ga_users+(min_ga_users/100*30)<ga_users[i]:
            min_fga_users=ga_users[i]

    if min_ga_users != ga_users[0]:
        return True
    else:
        return False


def crytical_high_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    max_ga_users = ga_users[0]
    for i in range(len(ga_users)):
        if max_ga_users+(max_ga_users/100*50)<ga_users[i]:
            max_ga_users=ga_users[i]

    if max_ga_users != ga_users[0]:
        return True
    else:
        return False


def crytical_day_ga_users(metrics: dict):
    pass


def path_to_grow_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    i = 1
    for i in range(len(ga_users)):
        if ga_users[i]<ga_users[i-1]:
            return False

    return True


def path_to_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    i = 1
    for i in range(len(ga_users)):
        if ga_users[i]>ga_users[i-1]:
            return False

    return True
#
#
# Cancel of new alerts Vova 24.10.2020

def just_true(metrics: dict):
    return True


lower_than_yesterday = Alert(
    category='idk',
    title='Your sessions are lover than yesterday',
    description='Your sessions are lover than yesterday',
    analytics_func=sessions_lower
)


always_alert = Alert(
    category='Test',
    title='This is test alert',
    description='The test alert',
    analytics_func=just_true
)


# New alerts Vova 24.10.2020
#
#

crytical_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В "" день количество пользователей критически понизилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=crytical_low_ga_users
)

crytical_high_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В "" день количество пользователей повысилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=crytical_high_ga_users
)

crytical_day_ga_users_alert = Alert(
    category='Test',
    title='This is test alert',
    description='The test alert',
    analytics_func=crytical_day_ga_users
)

path_to_grow_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='На протяжении последних 7 дней трафик последовательно растёт',
    description='Хорошие новости! Вы показываете отличный последовательный рост трафика на вашем сайте с помощью активных каналов привлечения. Задокументируйте план - действий, который был сделан в последние дни для того, чтобы повторить этот успех и усильте текущие активные маркетинговые каналы.',
    analytics_func=path_to_grow_ga_users
)

path_to_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='На протяжении последних 7 дней трафик последовательно падает',
    description='По данным сервиса Google Analytics количество пользователей главного домена падает на протяжении последних 7 дней. Обратите внимание на позиции сайта в поиске, выключенные или включенные рекламные каналы, а так же на показатель "Trust" вашего домена.',
    analytics_func=path_to_low_ga_users
)

# path_to_low_position_keywords_gsc = Alert(
#     category='Test',
#     title='This is test alert',
#     description='The test alert',
#     analytics_func=path_to_low_position_keywords_gsc
# )

# path_to_grow_position_keywords_gsc = Alert(
#     category='Test',
#     title='This is test alert',
#     description='The test alert',
#     analytics_func=path_to_grow_position_keywords_gsc
# )

# noncritical_alert_with_errors_pages_index_gsc = Alert(
#     category='Test',
#     title='This is test alert',
#     description='The test alert',
#     analytics_func=noncritical_alert_with_errors_pages_index_gsc
# )

# critical_alert_with_errors_pages_index_gsc = Alert(
#     category='Test',
#     title='This is test alert',
#     description='The test alert',
#     analytics_func=critical_alert_with_errors_pages_index_gsc
# )



#
#
# Cancel of new alerts Vova 24.10.2020


# New alerts Borya 19.11.2020
#
#
def CtrOfAllSCuser(metrics:dict):
    ctr = metrics.get('sc_ctr')
    i = 1
    for i in range(len(ctr)):
        if ctr != ctr[i]:
            return False
        return True

ctrOfAllSearchConsoleUser = Alert(
    category='SEO',
    title = f'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
    description = f'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )',
    analytics_func=CtrOfAllSCuser
)
#
#
# Cancel of new alerts Borya 19.11.2020



def return_alerts():
    return [lower_than_yesterday, always_alert, crytical_low_ga_users_alert,
    crytical_high_ga_users_alert, crytical_day_ga_users_alert, path_to_grow_ga_users_alert,
    path_to_low_ga_users_alert,ctrOfAllSearchConsoleUser]
