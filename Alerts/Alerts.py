from Alerts.Alert import Alert


def sessions_lower(metrics: dict):
    if metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 1] < metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 2]:
        return True
    return False


def crytical_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    min_ga_users = ga_users[0]
    for i in range(len(ga_users)):
        if min_ga_users+(min_ga_users/100*30)<ga_users[i]:
            min_ga_users=ga_users[i]

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

def gaBouncecCryticalFunc(metrics:dict):
    ctr = metrics.get('ga_bounces')
    array = 0
    for i in range(len(ctr)):
        array +=ctr[i]
        if i==7:
            if array/7>50:
                return True
            else:
                return False


gaBouncecCrytical = Alert(
    category=' Analytics',
    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик при первом касании с клиентом.',
    analytics_func=gaBouncecCryticalFunc
)


def GABouncecBadFunc(metrics:dict):
    ctr = metrics.get('ga_bounces')
    array = 0
    for i in range(len(ctr)):
        array +=ctr[i]
        if i==7:
            if 50>array/7>25:
                return True
            else:
                return False


GABouncecBad = Alert(
    category=' Analytics',
    title='Средний показатель отказов по сайту больше, чем 25% что неприемлемо для ваших клиентов и поисковых систем Google и Yandex',
    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 25%. Ваше ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик при первом касании с клиентом, а так же скорость загрузки страницы и глубину просмотра страницы.',
    analytics_func=GABouncecBadFunc
)


def GABouncecCryticalDayBadFunc(metrics:dict):
    ctr = metrics.get('ga_bounces')
    count = 0
    day = 0
    for i in range(len(ctr)):
        day+=1
        if ctr[i]>50:
            count+=1
        elif day ==7:
            if count>0:
                return True
            else:
                return False


GABouncecCryticalDayBad = Alert(
    category=' Analytics',
    title='Показатель отказов по сайту повысился больше, чем 50% в “N” ( N - день в котором произошёл критический момент )',
    description='В “N” день на вашем сайте был замечен показатель больше, чем 50% - это плохая новость для Вас, но с помощью неё можно проанализировать все маркетинговые каналы'
                ' и понять какой канал привёл нерелеватный трафик, которых не “зацепила” посадочная страница. Проведите анализ '
                'с помощью сводки Google Analytics - Источники трафика сравнивая показатель с “Bounce Rate” ( рус. Показатель Отказов ).',
    analytics_func=GABouncecCryticalDayBadFunc
)

def GAPathToLowReturningUserFunc(metrics:dict):
    ctr = metrics.get('ga_ReturningUser')
    count = 0
    for i in range(len(ctr)):
        if ctr[i]<=ctr[i-1]:
            count+=1
            if count == 7:
                return True
        else:
            return False



GAPathToLowReturningUser = Alert(
    category=' Analytics',
    title='Показатель возврата пользователей на сайт падает с каждым днём на протяжении последних 7 дней.',
    description='Похоже новые пользователи не возвращаются к Вам на сайт. Проверьте актуальность источников вашего ремаркетинга или ретаргетинга . Возврат пользователей это важная метрика Вашей конверсии и показатель ранжирования для поисковых систем. '
                'Обновите ваши креативы на ваших кампаниях нацеленных на возврат пользователей - скорее всего, они утратили актуальность.',
    analytics_func=GAPathToLowReturningUserFunc
)


def GAPathToGrowReturningUserFunc(metrics:dict):
    ctr = metrics.get('ga_ReturningUser')
    count = 0
    for i in range(len(ctr)):
        if ctr[i]>=ctr[i-1]:
            count+=1
            if count == 7:
                return True
        else:
            return False


GAPathToGrowReturningUser = Alert(
    category=' Analytics',
    title='Показатель возврата пользователей на сайт возрастает с каждым днём на протяжении последних 7 дней.',
    description='Отличная работа! Каналы вашего ремаркетинга показывают отличные показатели и растут за последние 7 дней возвращая'
                'всё больше и больше пользователей! Это позитивно складывается на вашей конверсии и ранжировании ваших сниппетов в поисковой системе.',
    analytics_func=GAPathToGrowReturningUserFunc
)


def return_alerts():
    return [lower_than_yesterday, always_alert, crytical_low_ga_users_alert,
    crytical_high_ga_users_alert, crytical_day_ga_users_alert, path_to_grow_ga_users_alert,
    path_to_low_ga_users_alert,gaBouncecCrytical,GABouncecBad,GABouncecCryticalDayBad,GAPathToLowReturningUser,
    GAPathToGrowReturningUser]

from Alerts.Alert import Alert


def sessions_lower(metrics: dict):
    if metrics.get('ga_sessions')[-1] < metrics.get('ga_sessions')[-2]:
        return True
    return False


def crytical_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    min_ga_users = ga_users[0]
    for i in range(len(ga_users)):
        if min_ga_users+(min_ga_users/100*30)<ga_users[i]:
            min_ga_users=ga_users[i]

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
    for i, item in enumerate(ga_users):
        if item<ga_users[i-1]:
            return False

    return True


def path_to_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    i = 1
    for i in range(len(ga_users)):
        if ga_users[i]>ga_users[i-1]:
            return False

    return True


def just_true(metrics: dict):
    return True


lower_than_yesterday = Alert(
    category='idk',
    title='Your sessions are lover than yesterday',
    description='Your sessions are lover than yesterday',
    analytics_func=sessions_lower,
    is_human_created=False
)


always_alert = Alert(
    category='Test',
    title='This is test alert',
    description='The test alert',
    analytics_func=just_true,
    is_human_created=False
)


crytical_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В "" день количество пользователей критически понизилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=crytical_low_ga_users,
    is_human_created=False
)


crytical_high_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В "" день количество пользователей повысилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=crytical_high_ga_users,
    is_human_created=False
)


crytical_day_ga_users_alert = Alert(
    category='Test',
    title='This is test alert',
    description='The test alert',
    analytics_func=crytical_day_ga_users,
    is_human_created=False
)


path_to_grow_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='На протяжении последних 7 дней трафик последовательно растёт',
    description='Хорошие новости! Вы показываете отличный последовательный рост трафика на вашем сайте с помощью активных каналов привлечения. Задокументируйте план - действий, который был сделан в последние дни для того, чтобы повторить этот успех и усильте текущие активные маркетинговые каналы.',
    analytics_func=path_to_grow_ga_users,
    is_human_created=False
)


path_to_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='На протяжении последних 7 дней трафик последовательно падает',
    description='По данным сервиса Google Analytics количество пользователей главного домена падает на протяжении последних 7 дней. Обратите внимание на позиции сайта в поиске, выключенные или включенные рекламные каналы, а так же на показатель "Trust" вашего домена.',
    analytics_func=path_to_low_ga_users,
    is_human_created=False
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


def return_alerts():
    return [lower_than_yesterday, crytical_low_ga_users_alert,
    crytical_high_ga_users_alert, crytical_day_ga_users_alert, path_to_grow_ga_users_alert,
    path_to_low_ga_users_alert]
