from Alerts.Alert import Alert


def sessions_lower(metrics: dict):
    all_sessions = metrics.get('ga_sessions')
    return all_sessions[-1] < all_sessions[-2]


#Нужно ТЗ
def critical_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    min_ga_users = ga_users[0]
    for i in range(len(ga_users)):
        if min_ga_users+(min_ga_users/100*30)<ga_users[i]:
            min_ga_users=ga_users[i]

    if min_ga_users != ga_users[0]:
        return True
    else:
        return False


#Нужно ТЗ
def critical_high_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')
    max_ga_users = ga_users[0]
    for i in range(len(ga_users)):
        if max_ga_users+(max_ga_users/100*50)<ga_users[i]:
            max_ga_users=ga_users[i]

    if max_ga_users != ga_users[0]:
        return True
    else:
        return False

#Нужно ТЗ
def critical_day_ga_users(metrics: dict):
    pass


def path_to_grow_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')[-7:]
    for index in range(0, 6):
        if ga_users[index] > ga_users[index+1]:
            return False
    return True


def path_to_low_ga_users(metrics: dict):
    ga_users = metrics.get('ga_users')[-7:]
    for index in range(0, 6):
        if ga_users[index] < ga_users[index + 1]:
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


critical_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В "" день количество пользователей критически понизилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=critical_low_ga_users
)


critical_high_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В "" день количество пользователей повысилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=critical_high_ga_users
)


critical_day_ga_users_alert = Alert(
    category='Test',
    title='This is test alert',
    description='The test alert',
    analytics_func=critical_day_ga_users
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

def ga_bounces_crytical_func(metrics:dict):
    week_ga_bounces_list = metrics.get('ga_bounces')[-7:]
    weekly_sum = sum(week_ga_bounces_list)
    return weekly_sum/7 > 50


ga_bounces_crytical = Alert(
    category=' Analytics',
    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик при первом касании с клиентом.',
    analytics_func=ga_bounces_crytical_func
)


def ga_bounces_bad_func(metrics:dict):
    week_ga_bounces_list = metrics.get('ga_bounces')[-7:]
    weekly_sum = sum(week_ga_bounces_list)
    return 25 < weekly_sum/7 < 50


ga_bounces_bad = Alert(
    category=' Analytics',
    title='Средний показатель отказов по сайту больше, чем 25% что неприемлемо для ваших клиентов и поисковых систем Google и Yandex',
    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 25%. Ваше ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик при первом касании с клиентом, а так же скорость загрузки страницы и глубину просмотра страницы.',
    analytics_func=ga_bounces_bad_func
)

def test(metrics:dict):
    week_ga_bounces_list = metrics.get('ga_bounces')[-7:]
    for item in week_ga_bounces_list:
        if item > 50:
            return week_ga_bounces_list.index(item) + 1
    return 777

def ga_bounces_crytical_day_bad_func(metrics:dict):
    week_ga_bounces_list = metrics.get('ga_bounces')[-7:]
    for item in week_ga_bounces_list:
        if item > 50:
            return week_ga_bounces_list.index(item) + 1
    return False


ga_bounces_crytical_day_bad = Alert(
    category=' Analytics',
    title='Показатель отказов по сайту повысился больше, чем 50% в “N” ( N - день в котором произошёл критический момент )',
    description='В “N” день на вашем сайте был замечен показатель больше, чем 50% - это плохая новость для Вас, но с помощью неё можно проанализировать все маркетинговые каналы'
                ' и понять какой канал привёл нерелеватный трафик, которых не “зацепила” посадочная страница. Проведите анализ '
                'с помощью сводки Google Analytics - Источники трафика сравнивая показатель с “Bounce Rate” ( рус. Показатель Отказов ).',
    analytics_func=ga_bounces_crytical_day_bad_func
)


ga_bounces_crytical_day_bad.N = test



def ga_path_to_low_returning_user_func(metrics:dict):
    weekly_returning_users = metrics.get('ga_ReturningUser')[-7:]
    for i in range(0, 6):
        if weekly_returning_users[i] <= weekly_returning_users[i+1]:
            return False
    return True


ga_path_to_low_returning_user = Alert(
    category=' Analytics',
    title='Показатель возврата пользователей на сайт падает с каждым днём на протяжении последних 7 дней.',
    description='Похоже новые пользователи не возвращаются к Вам на сайт. Проверьте актуальность источников вашего ремаркетинга или ретаргетинга . Возврат пользователей это важная метрика Вашей конверсии и показатель ранжирования для поисковых систем. '
                'Обновите ваши креативы на ваших кампаниях нацеленных на возврат пользователей - скорее всего, они утратили актуальность.',
    analytics_func=ga_path_to_low_returning_user_func
)


def ga_path_to_grow_returning_user_func(metrics:dict):
    weekly_returning_users = metrics.get('ga_ReturningUser')[-7:]
    for i in range(0, 6):
        if weekly_returning_users[i] >= weekly_returning_users[i + 1]:
            return False
    return True


ga_path_to_grow_returning_user = Alert(
    category=' Analytics',
    title='Показатель возврата пользователей на сайт возрастает с каждым днём на протяжении последних 7 дней.',
    description='Отличная работа! Каналы вашего ремаркетинга показывают отличные показатели и растут за последние 7 дней возвращая'
                'всё больше и больше пользователей! Это позитивно складывается на вашей конверсии и ранжировании ваших сниппетов в поисковой системе.',
    analytics_func=ga_path_to_grow_returning_user_func
)


def return_alerts():
    return [lower_than_yesterday, always_alert, critical_low_ga_users_alert,
    critical_high_ga_users_alert, critical_day_ga_users_alert, path_to_grow_ga_users_alert,
    path_to_low_ga_users_alert,ga_bounces_crytical,ga_bounces_bad,ga_bounces_crytical_day_bad,ga_path_to_low_returning_user,
    ga_path_to_grow_returning_user]
