from Alerts.Alert import Alert


# TEST_ALERT
def sessions_lower(metrics: dict):
    if(all_sessions := metrics.get('ga_sessions', {}).get('total')):
        if (len(all_sessions) > 1):
            return all_sessions[-1] < all_sessions[-2]
    return False


lower_than_yesterday = Alert(
    category='idk',
    title='Your sessions are lover than yesterday',
    description='Your sessions are lover than yesterday',
    analytics_func=sessions_lower
)


# TEST_ALERT
def critical_low_ga_users(metrics: dict):
    if(ga_users := metrics.get('ga_users', {}).get('total')):
        ga_users = ga_users[-7:]
        min_ga_users = min(ga_users)
        average_users = sum(ga_users) - min_ga_users
        average_users = average_users / 6
        return min_ga_users < average_users*0.7
    return False


def day_low_ga_users(metrics: dict):
    if(ga_users := metrics.get('ga_users', {}).get('total')):
        ga_users = ga_users[-7:]
        return ga_users.index(min(ga_users)) + 1


critical_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В {day} день количество пользователей критически понизилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=critical_low_ga_users
)
critical_low_ga_users_alert.day = day_low_ga_users


# TEST_ALERT
def critical_high_ga_users(metrics: dict):
    if(ga_users := metrics.get('ga_users', {}).get('total')):
        ga_users = ga_users[-7:]
        max_ga_users = max(ga_users)
        average_users = sum(ga_users) - max_ga_users
        average_users = average_users / 6
        return max_ga_users > average_users * 1.5


def day_high_ga_users(metrics: dict):
    if(ga_users := metrics.get('ga_users', {}).get('total')):
        ga_users = ga_users[-7:]
        return ga_users.index(max(ga_users)) + 1


critical_high_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='В {day} день количество пользователей повысилось по сравнению с другими днями этой недели',
    description='The test alert',
    analytics_func=critical_high_ga_users
)
critical_high_ga_users_alert.day = day_high_ga_users


# ALERTS 0.02
# GA_ALERT
def path_to_grow_ga_users(metrics: dict):
    if (ga_users := metrics.get('ga_users', {}).get('total')):
        ga_users = ga_users[-7:]
        return sorted(ga_users) == ga_users


path_to_grow_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='На протяжении последних 7 дней трафик последовательно растёт',
    description='Хорошие новости! Вы показываете отличный последовательный рост трафика на вашем сайте с помощью активных каналов привлечения. Задокументируйте план - действий, который был сделан в последние дни для того, чтобы повторить этот успех и усильте текущие активные маркетинговые каналы.',
    analytics_func=path_to_grow_ga_users
)


# GA_ALERT
def path_to_low_ga_users(metrics: dict):
    if (ga_users := metrics.get('ga_users', {}).get('total')):
        ga_users = ga_users[-7:]
        return sorted(ga_users, reverse=True) == ga_users


path_to_low_ga_users_alert = Alert(
    category='Аналитика ( Google Analytics )',
    title='На протяжении последних 7 дней трафик последовательно падает',
    description='По данным сервиса Google Analytics количество пользователей главного домена падает на протяжении последних 7 дней. Обратите внимание на позиции сайта в поиске, выключенные или включенные рекламные каналы, а так же на показатель "Trust" вашего домена.',
    analytics_func=path_to_low_ga_users
)


# TEST_ALERT
def just_true(metrics: dict):
    return True


always_alert = Alert(
    category='Test',
    title='This is test alert',
    description='The test alert',
    analytics_func=just_true
)


# GA_ALERT
def ga_bounces_crytical_func(metrics:dict):
    if(week_ga_bounces_list := metrics.get('ga_bounces', {}).get('total')):
        week_ga_bounces_list = week_ga_bounces_list[-7:]
        weekly_sum = sum(week_ga_bounces_list)
        return weekly_sum/7 > 50


ga_bounces_crytical = Alert(
    category=' Analytics',
    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик при первом касании с клиентом.',
    analytics_func=ga_bounces_crytical_func
)


# GA_ALERT
def ga_bounces_bad_func(metrics:dict):
    if(week_ga_bounces_list := metrics.get('ga_bounces',{}).get('total')):
        week_ga_bounces_list = week_ga_bounces_list[-7:]
        weekly_sum = sum(week_ga_bounces_list)
        return 25 < weekly_sum/7 < 50


ga_bounces_bad = Alert(
    category=' Analytics',
    title='Средний показатель отказов по сайту больше, чем 25% что неприемлемо для ваших клиентов и поисковых систем Google и Yandex',
    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 25%. Ваше ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик при первом касании с клиентом, а так же скорость загрузки страницы и глубину просмотра страницы.',
    analytics_func=ga_bounces_bad_func
)

# GA_ALERT
def ga_bounces_crytical_day_bad_func(metrics: dict):
    if(week_ga_bounces_list := metrics.get('ga_bounces', {}).get('total')):
        week_ga_bounces_list = week_ga_bounces_list[-7:]
        for item in week_ga_bounces_list:
            if item > 50:
                return True
    return False


def day_ga_bounces_crytical(metrics: dict):
    if (week_ga_bounces_list := metrics.get('ga_bounces', {}).get('total', [])[-7:]):
        for item in week_ga_bounces_list:
            if item > 50:
                return week_ga_bounces_list.index(item) + 1
    return ""


ga_bounces_crytical_day_bad = Alert(
    category=' Analytics',
    title='Показатель отказов по сайту повысился больше, чем 50% в {day} ( {day} - день в котором произошёл критический момент )',
    description='В {day} день на вашем сайте был замечен показатель больше, чем 50% - это плохая новость для Вас, но с помощью неё можно проанализировать все маркетинговые каналы'
                ' и понять какой канал привёл нерелеватный трафик, которых не “зацепила” посадочная страница. Проведите анализ '
                'с помощью сводки Google Analytics - Источники трафика сравнивая показатель с “Bounce Rate” ( рус. Показатель Отказов ).',
    analytics_func=ga_bounces_crytical_day_bad_func
)
ga_bounces_crytical_day_bad.day = day_ga_bounces_crytical


# GA_ALERT
def ga_path_to_low_returning_user_func(metrics:dict):
    if(returning_users := metrics.get('ga_ReturningUser', {}).get('total')):
        returning_users = returning_users[-7:]
        return sorted(returning_users, reverse=True) == returning_users


ga_path_to_low_returning_user = Alert(
    category=' Analytics',
    title='Показатель возврата пользователей на сайт падает с каждым днём на протяжении последних 7 дней.',
    description='Похоже новые пользователи не возвращаются к Вам на сайт. Проверьте актуальность источников вашего ремаркетинга или ретаргетинга . Возврат пользователей это важная метрика Вашей конверсии и показатель ранжирования для поисковых систем. '
                'Обновите ваши креативы на ваших кампаниях нацеленных на возврат пользователей - скорее всего, они утратили актуальность.',
    analytics_func=ga_path_to_low_returning_user_func
)


#GA_ALERT
def ga_path_to_grow_returning_user_func(metrics:dict):
    if(returning_users := metrics.get('ga_ReturningUser', {}).get('total')):
        returning_users = returning_users[-7:]
        return sorted(returning_users) == returning_users


ga_path_to_grow_returning_user = Alert(
    category=' Analytics',
    title='Показатель возврата пользователей на сайт возрастает с каждым днём на протяжении последних 7 дней.',
    description='Отличная работа! Каналы вашего ремаркетинга показывают отличные показатели и растут за последние 7 дней возвращая'
                'всё больше и больше пользователей! Это позитивно складывается на вашей конверсии и ранжировании ваших сниппетов в поисковой системе.',
    analytics_func=ga_path_to_grow_returning_user_func
)


def return_alerts():
    return [lower_than_yesterday, always_alert, critical_low_ga_users_alert, critical_high_ga_users_alert,
            path_to_grow_ga_users_alert, path_to_low_ga_users_alert, ga_bounces_crytical,
            ga_bounces_bad,ga_bounces_crytical_day_bad,ga_path_to_low_returning_user, ga_path_to_grow_returning_user]
