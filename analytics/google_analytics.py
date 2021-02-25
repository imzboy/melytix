from analytics.base import MetricAnalyzer, MetricNotFoundException, Tip, Alert

import datetime

class GaSessionsAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_sessions')
        if not self.metric:
            raise MetricNotFoundException('ga_sessions not found')

    def sessions_lower(self, alg_id):
        if (all_sessions := self.metric.get('total')):
            if len(all_sessions) > 1:
                if all_sessions[-1] < all_sessions[-2]:
                    return Alert(
                        _id=alg_id,
                        category='idk',
                        title='Your sessions are lover than yesterday',
                        description='Your sessions are lover than yesterday')


class GaUsersAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_users')
        if not self.metric:
            raise MetricNotFoundException('ga_users not found')

    def critical_low_ga_users(self, alg_id):
        if (ga_users := self.metric.get('total', [])[-7:]):
            min_ga_users = min(ga_users)
            average_users = sum(ga_users) - min_ga_users
            average_users = average_users / 6
            if min_ga_users < average_users * 0.7:
                day = 7 - ga_users.index(min_ga_users) - 1
                day = (datetime.datetime.now() - datetime.timedelta(days=day)).date().isoformat()
                return Alert(
                    _id=alg_id,
                    category='Аналитика ( Google Analytics )',
                    title=f'В {day} день количество пользователей критически понизилось по сравнению с другими днями этой недели',
                    description='The test alert')

    def critical_high_ga_users(self, alg_id):
        if (ga_users := self.metric.get('total',[])[-7:]):
            max_ga_users = max(ga_users)
            average_users = sum(ga_users) - max_ga_users
            average_users = average_users / 6
            if max_ga_users > average_users * 1.5:
                day = 7 - ga_users.index(max_ga_users) - 1
                day = (datetime.datetime.now() - datetime.timedelta(days=day)).date().isoformat()
                return Alert(
                    _id=alg_id,
                    category='Аналитика ( Google Analytics )',
                    title=f'В {day} день количество пользователей повысилось по сравнению с другими днями этой недели',
                    description='The test alert')

    def path_to_grow_ga_users(self, alg_id):
        if (ga_users := self.metric.get('total',[])[-7:]):
            if sorted(ga_users) == ga_users:
                return Alert(
                    _id=alg_id,
                    category='Аналитика ( Google Analytics )',
                    title='На протяжении последних 7 дней трафик последовательно растёт',
                    description='Хорошие новости! Вы показываете отличный последовательный рост трафика на вашем '
                                'сайте с помощью активных каналов привлечения. Задокументируйте план - действий, '
                                'который был сделан в последние дни для того, чтобы повторить этот успех и усильте '
                                'текущие активные маркетинговые каналы.')

    def path_to_low_ga_users(self, alg_id):
        if (ga_users := self.metric.get('total')[-7:]):
            if sorted(ga_users, reverse=True) == ga_users:
                return Alert(
                    _id=alg_id,
                    category='Аналитика ( Google Analytics )',
                    title='На протяжении последних 7 дней трафик последовательно падает',
                    description='По данным сервиса Google Analytics количество пользователей главного домена падает '
                                'на протяжении последних 7 дней. Обратите внимание на позиции сайта в поиске, '
                                'выключенные или включенные рекламные каналы, а так же на показатель "Trust" вашего '
                                'домена.')


class GaBouncesAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_bounces')
        if not self.metric:
            raise MetricNotFoundException('ga_bounces not found')

    def ga_bounces_crytical_func(self, alg_id):
        if (week_ga_bounces_list := self.metric.get('total')[-7:]):
            weekly_sum = sum(week_ga_bounces_list)
            if weekly_sum / 7 > 50:
                return Alert(
                    _id=alg_id,
                    category=' Analytics',
                    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
                    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше '
                                'ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на '
                                'сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик '
                                'при первом касании с клиентом.')

    def ga_bounces_bad_func(self, alg_id):
        if (week_ga_bounces_list := self.metric.get('total')[-7:]):
            weekly_sum = sum(week_ga_bounces_list)
            if 25 < weekly_sum / 7 < 50:
                return Alert(
                    _id=alg_id,
                    category=' Analytics',
                    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
                    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше '
                                'ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на '
                                'сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик '
                                'при первом касании с клиентом.')

    def ga_bounces_crytical_day_bad_func(self, alg_id):
        if (week_ga_bounces_list := self.metric.get('total')[-7:]):
            for item in week_ga_bounces_list:
                if item > 50:
                    day = week_ga_bounces_list.index(item) + 1
                    return Alert(
                        _id=alg_id,
                        category=' Analytics',
                        title='Показатель отказов по сайту повысился больше, чем 50% в {day} ( {day} - день в котором произошёл критический момент )',
                        description=f'В {day} день на вашем сайте был замечен показатель больше, чем 50% - это плохая новость для Вас, но с помощью неё можно проанализировать все маркетинговые каналы'
                                    ' и понять какой канал привёл нерелеватный трафик, которых не “зацепила” посадочная страница. Проведите анализ '
                                    'с помощью сводки Google Analytics - Источники трафика сравнивая показатель с “Bounce Rate” ( рус. Показатель Отказов ).')


class GaReturningUserAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_returningUser')
        if not self.metric:
            raise MetricNotFoundException('ga_ReturningUser not found')

    def ga_path_to_low_returning_user_func(self, alg_id):
        if (returning_users := self.metric.get('total')[-7:]):
            if sorted(returning_users, reverse=True) == returning_users:
                return Alert(
                    _id = alg_id,
                    category=' Analytics',
                    title='Показатель возврата пользователей на сайт падает с каждым днём на протяжении последних 7 дней.',
                    description='Похоже новые пользователи не возвращаются к Вам на сайт. Проверьте актуальность источников вашего ремаркетинга или ретаргетинга . Возврат пользователей это важная метрика Вашей конверсии и показатель ранжирования для поисковых систем. '
                                'Обновите ваши креативы на ваших кампаниях нацеленных на возврат пользователей - скорее всего, они утратили актуальность.')

    def ga_path_to_grow_returning_user_func(self, alg_id):
        if (returning_users := self.metric.get('total')[-7:]):
            if sorted(returning_users) == returning_users:
                return Alert(
                    _id=alg_id,
                    category=' Analytics',
                    title='Показатель возврата пользователей на сайт возрастает с каждым днём на протяжении последних 7 дней.',
                    description='Отличная работа! Каналы вашего ремаркетинга показывают отличные показатели и растут за последние 7 дней возвращая'
                                'всё больше и больше пользователей! Это позитивно складывается на вашей конверсии и ранжировании ваших сниппетов в поисковой системе.')

    def low_ga_returning_user_func(self, alg_id):
        if(weekly_returning := self.metric.get('total', [])[-7:]):
            average = sum(weekly_returning) / 7
            if 0.25 < average < 0.5:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Пользователи не активно возвращаются на главный домен.',
                    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                                'Проверьте настройки вашего ремаркетинга и ретаргетинга, увеличьте частоту показа вашей рекламы для '
                                'возвраты трафика, а также просмотрите показатель “CTR” ваших объявлений для полного решения проблем '
                                'в процессе возвращения вашего трафика.')

    def no_ga_returning_user_func(self, alg_id):
        if(weekly_returning := self.metric.get('total', [])[-7:]):
            average = sum(weekly_returning) / 7
            if average < 0.25:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Пользователи не возвращаются на главный домен.',
                    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                                'Более 55% онлайн бизнесов настраивают ремаркетинг и ретаргетинг для рекламы своего сайта. '
                                'Это позволяет проекту быть всегда “на слуху” у пользователя!'
                                'Используйте технологию ремаркетинга в Google Adwords или Yandex Direct, а также протестируйте '
                                'ретаргетинг в социальных для возврата пользователей '
                                'на сайт - это сможет повысить количество повторяющихся продаж, а также поднимет вашу конверсию.')

    def right_ga_returning_user_func(self, alg_id):
        if(weekly_returning := self.metric.get('total', [])[-7:]):
            average = sum(weekly_returning) / 7
            if average > 0.8:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Вы отлично возвращаете пользователей на ваш главный домен.',
                    description='Вы отлично возвращаете пользователей на ваш сайт, это повышает показатель вашей конверсии и '
                                'повторяющихся успехов в ваших бизнес - целях. Советуем повысить бюджет вашей ремаркетинговой или '
                                'ретаргетинговой рекламы в целях усиление данного канала и повышения важных для бизнеса метрик!')


class GaNewUserAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_newUser')
        if not self.metric:
            raise MetricNotFoundException('ga_NewUser not found')

    def grows_of_new_users_func(self, alg_id):
        if(new_users := self.metric.get('total', [])[-7:]):
            if sorted(new_users) == new_users:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Приток новых уникальных пользователей на этой неделе сохранился и растёт последовательно!',
                    description='На протяжении недели зафиксирован положительный прирост новых уникальных пользователей. Сохраните '
                                'настройки каналов маркетинга для дальнейшего повышения роста новых пользователей, который влияет но '
                                'повышение показателя уникальной конверсии!')

    def loss_of_new_users_func(self, alg_id):
        if(new_users := self.metric.get('total', [])[-7:]):
            if sorted(new_users, reverse=True) == new_users:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Приток новых уникальных пользователей на этой неделе упал!',
                    description='На протяжении недели зафиксировано падение новых уникальных пользователей. '
                                'Проверьте состояние каналов маркетинга для исправления и повышения данной метрики для увеличения '
                                'показателей ранжирования сайта и новой уникальной конверсии.')

class GaPageViewsPerSessionAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_pageviewsPerSession')
        if not self.metric:
            raise MetricNotFoundException('ga_pageviewsPerSession not found')

    def low_ga_page_views_per_session_func(self, alg_id):
        if(weekly_views := self.metric.get('total', [])[-7:]):
            for item in weekly_views:
                if item < 1.5:
                    return Tip(
                        _id = alg_id,
                        category='Analytics',
                        title='Ваш трафик не просматривает контент вовлеченно.',
                        description='На протяжении недели пользователи не вовлеченно изучают контент главного домена. '
                                    'Данная проблема происходит на сайтах, который допускает такие ошибки, как: '
                                    '1.Неудобно расположено меню для пользователей. '
                                    '2. Пользователей направляют рекламой на не релевантную страницу. '
                                    '3. Контент на странице не интересен приходящему трафику. '
                                    'Советуем изменить страницы входа пользователя, проверить настройки меню и навигации на вашем сайте, '
                                    'пересмотреть настройки рекламы привлечения трафика.')


class GaAvgSessionDurationAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_avgSessionDuration')
        if not self.metric:
            raise MetricNotFoundException('ga_avgSessionDuration not found')

    def right_avg_session_duration_func(self, alg_id):
        if(session_duration := self.metric.get('total', [])[-7:]):
            average = sum(session_duration) / 7
            if average > 1.3:
                return Tip(
                    _id = alg_id,
                    category='Analytics',
                    title='В показателе средней продолжительности сеанса вы больше, чем 56% сайтов.',
                    description='Вы отлично удерживаете внимание пользователя на вашем сайте, аудитория достаточно активно изучает'
                                ' контент на странице - для повышения данного показателя постарайтесь добавить больше пунктов навигации'
                                ' для дальнейшего продолжения “изучения” пользователя вашего сайта. Хорошая работа!')

    def low_avg_session_duration_func(self, alg_id):
        if(session_duration := self.metric.get('total', [])[-7:]):
            average = sum(session_duration) / 7
            if 1.0 < average < 1.5:
                return Tip(
                    _id = alg_id,
                    category='Analytics',
                    title='В показателе средней продолжительности сеанса вы меньше, чем 35% сайтов.',
                    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего '
                                'главного домена в поисковике.Постарайтесь удержать внимание Вашего пользователя на сайте дольше, '
                                'чем есть сейчас - добавив больше навигационных подсказок пути пользователя на вашей странице.')

    def no_avg_session_duration_func(self, alg_id):
        if(session_duration := self.metric.get('total', [])[-7:]):
            average = sum(session_duration) / 7
            if average < 1.0:
                return Tip(
                    _id = alg_id,
                    category='Analytics',
                    title='В показателе средней продолжительности сеанса вы меньше, чем 85% сайтов',
                    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего '
                                'главного домена в поисковике. '
                                'Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше '
                                'навигационных подсказок пути пользователя на вашей странице. '
                                'А также проверьте настройки ваших маркетинговых каналов по привлечению трафика - релевантный ли трафик заходит к вам на сайт?')


class GaAvgPageLoadTimeAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_avgPageLoadTime')
        if not self.metric:
            raise MetricNotFoundException('ga_avgPageLoadTime not found')

    def critical_load_time(self, alg_id):
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if item > 3:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Скорость загрузки страницы не оптимизирована!',
                    description='Скорость загрузки ваших страниц сайта не оптимизирована. В данный момент средний показатель '
                                'составляет больше 3-ёх секунд, что недопустимо для поисковых систем, а главное Ваших поведенческих '
                                'показателей пользователей. Данная метрика отрицательно влияет на ваши показатели в ранжировании и '
                                'конверсии. Постарайтесь сократить ненужный код на сайте, а так же кэшировать изображения на вашем '
                                'сайте для улучшения данного показателя.')

    def avg_load_time(self, alg_id):
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if item > 2:
                return Tip(
                    _id=alg_id,
                    category='Analytics',
                    title='Скорость загрузки оптимизирована недостаточно.',
                    description='Скорость загрузки ваших страниц сайта не оптимизирована в полной мере. В данный момент средний '
                                'показатель составляет больше 2-ёх секунд, что не даёт максимальной эффективности для поисковых '
                                'систем, а главное Ваших поведенческих показателей пользователей. Данная метрика отрицательно влияет '
                                'на ваши показатели в ранжировании и конверсии. Постарайтесь сократить ненужный код на сайте, '
                                'а так же кэшировать изображения на вашем сайте для улучшения данного показателя.')


class GaTimeOnPageAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('ga_timeOnPage')
        if not self.metric:
            raise MetricNotFoundException('ga_timeOnPage not found')

    def critical_time_on_page(self, alg_id):
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if item < 10:
                return Tip(
                    _id = alg_id,
                    category='Analytics',
                    title='Пользователи не задерживаются на вашем сайте.',
                    description='Пользователи не задерживаются на вашем сайте. Причиной ухудшения данной метрики может быть несколько '
                                'событий: на сайт приводится нерелевантный трафик, страницы сайта долго прогружаются, интуитивно '
                                'пользователю не понравился дизайн вашего сайта. Постарайтесь исправить хотя бы одно из этих событий, '
                                'а Melytix.ai в автоматическом режиме снова измерит Ваши показатели!')

    def low_time_on_page(self, alg_id):
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if item < 30:
                return Tip(
                    _id = alg_id,
                    category='Analytics',
                    title='Пользователи задерживаются на вашем сайте слишком мало.',
                    description='Пользователи задерживаются на вашем сайте слишком мало. Причиной ухудшения данной метрики может быть '
                                'несколько событий: на сайт приводится нерелевантный трафик, страницы сайта долго прогружаются. '
                                'Постарайтесь исправить хотя бы одно из этих событий, а Melytix.ai в автоматическом режиме снова '
                                'измерит Ваши показатели!')
