from Tips.Tip import Tip


# TIPS version 0.01
# SC_TIP
def ctr_of_all_users(metrics: dict):
    all_ctr = metrics.get('sc_ctr')
    res = len([i for i in all_ctr if i < 1])
    return res/len(all_ctr) > 0.4


ctr_of_all_search_console_user = Tip(
    category='SEO',
    title = 'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
    description = 'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )',
    analytics_func=ctr_of_all_users,
    is_human_created=False
)


# TIPS version 0.02
# GA_TIPS
def grows_of_new_users_func(metrics:dict):
    new_users = metrics.get('ga_NewUser', [])[-7:]
    return new_users and sorted(new_users) == new_users


grows_of_new_users = Tip(
    category='Analytics',
    title='Приток новых уникальных пользователей на этой неделе сохранился и растёт последовательно!',
    description='На протяжении недели зафиксирован положительный прирост новых уникальных пользователей.'
                'Сохраните настройки каналов маркетинга для дальнейшего повышения роста новых пользователей. '
                'Сохраните настройки каналов маркетинга для дальнейшего повышения роста новых пользователей, который влияет но повышение показателя уникальной конверсии!',
    analytics_func=grows_of_new_users_func
)


def low_ga_page_views_per_session_func(metrics: dict):
    weekly_views = metrics.get('ga_pageViewsPerSession', [])[-7:]
    for item in weekly_views:
        if item < 1.5:
            return True

    return False


low_ga_page_views_per_session = Tip(
    category='Analytics',
    title='Ваш трафик не просматривает контент вовлеченно.',
    description='На протяжении недели пользователи не вовлеченно изучают контент главного домена. '
                'Данная проблема происходит на сайтах, который допускает такие ошибки, как: '
                '1.Неудобно расположено меню для пользователей. '
                '2. Пользователей направляют рекламой на не релевантную страницу. '
                '3. Контент на странице не интересен приходящему трафику. '
                'Советуем изменить страницы входа пользователя, проверить настройки меню и навигации на вашем сайте, пересмотреть настройки рекламы привлечения трафика.',
    analytics_func=low_ga_page_views_per_session_func
)


def low_ga_returning_user_func(metrics : dict):
    weekly_returning = metrics.get('ga_ReturningUser', [])[-7:]
    average = sum(weekly_returning)/7
    return 0.25 < average < 0.5


low_ga_returning_user = Tip(
    category='Analytics',
    title='Пользователи не активно возвращаются на главный домен.',
    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                'Проверьте настройки вашего ремаркетинга и ретаргетинга, увеличьте частоту показа вашей рекламы для возвраты трафика, '
                'а также просмотрите показатель “CTR” ваших объявлений для полного решения проблем в процессе возвращения вашего трафика.',
    analytics_func=low_ga_returning_user_func
)


def no_ga_returning_user_func(metrics:dict):
    weekly_returning = metrics.get('ga_ReturningUser', [])[-7:]
    average = sum(weekly_returning) / 7
    return average < 0.25


no_ga_returning_user = Tip(
    category='Analytics',
    title='Пользователи не возвращаются на главный домен.',
    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                'Более 55% онлайн бизнесов настраивают ремаркетинг и ретаргетинг для рекламы своего сайта. '
                'Это позволяет проекту быть всегда “на слуху” у пользователя!'
                'Используйте технологию ремаркетинга в Google Adwords или Yandex Direct, а также протестируйте ретаргетинг в социальных для возврата пользователей '
                'на сайт - это сможет повысить количество повторяющихся продаж, а также поднимет вашу конверсию.',
    analytics_func=no_ga_returning_user_func
)


def right_ga_returning_user_func(metrics: dict):
    weekly_returning = metrics.get('ga_ReturningUser', [])[-7:]
    average = sum(weekly_returning) / 7
    return average > 0.8


right_ga_returning_user = Tip(
    category='Analytics',
    title='Вы отлично возвращаете пользователей на ваш главный домен.',
    description='Вы отлично возвращаете пользователей на ваш сайт, это повышает показатель вашей конверсии и повторяющихся успехов в ваших бизнес - целях. '
                'Советуем повысить бюджет вашей ремаркетинговой или ретаргетинговой рекламы в целях усиление данного канала и повышения важных для бизнеса метрик!',
    analytics_func=right_ga_returning_user_func
)


def right_avg_session_duration_func(metrics: dict):
    session_duration = metrics.get('ga_avgSessionDuration', [])[-7:]
    average = sum(session_duration) / 7
    return average > 1.3


right_avg_session_duration = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы больше, чем 56% сайтов.',
    description='Вы отлично удерживаете внимание пользователя на вашем сайте, аудитория достаточно активно изучает'
                ' контент на странице - для повышения данного показателя постарайтесь добавить больше пунктов навигации'
                ' для дальнейшего продолжения “изучения” пользователя вашего сайта. Хорошая работа!',
    analytics_func=right_avg_session_duration_func
)


def low_avg_session_duration_func(metrics:dict):
    session_duration = metrics.get('ga_avgSessionDuration', [])[-7:]
    average = sum(session_duration) / 7
    return 1.0 < average < 1.5


low_avg_session_duration = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы меньше, чем 35% сайтов.',
    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего главного домена в поисковике.'
                ' Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше навигационных подсказок пути пользователя на вашей странице.',
    analytics_func=low_avg_session_duration_func
)


def no_avg_session_duration_func(metrics: dict):
    session_duration = metrics.get('ga_avgSessionDuration', [])[-7:]
    average = sum(session_duration) / 7
    return average < 1.0


no_avg_session_duration = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы меньше, чем 85% сайтов',
    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего главного домена в поисковике. '
                'Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше навигационных подсказок '
                'пути пользователя на вашей странице. А также проверьте настройки ваших маркетинговых каналов по привлечению трафика - релевантный ли трафик заходит к вам на сайт?',
    analytics_func=no_avg_session_duration_func
)


def loss_of_new_users_func(metrics:dict):
    new_users = metrics.get('ga_NewUser', [])[-7:]
    return new_users and sorted(new_users, reverse=True) == new_users


loss_of_new_users = Tip(
    category ='Analytics',
    title='Приток новых уникальных пользователей на этой неделе упал!',
    description='На протяжении недели зафиксировано падение новых уникальных пользователей. '
                'Проверьте состояние каналов маркетинга для исправления и повышения данной метрики для увеличения показателей ранжирования сайта и новой уникальной конверсии.',
    analytics_func=loss_of_new_users_func
)


def return_tips():
    return [grows_of_new_users, low_ga_page_views_per_session, low_ga_returning_user, no_ga_returning_user,
            right_ga_returning_user, right_avg_session_duration, low_avg_session_duration,
            no_avg_session_duration, loss_of_new_users]
