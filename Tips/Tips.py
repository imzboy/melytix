from Tips.Tip import Tip


# TIPS version 0.01
# SC_TIP
def ctr_of_all_users(metrics: dict):
    all_ctr = metrics.get('sc_ctr', [])[-7:]
    res = len([i for i in all_ctr if i < 1])
    return res/len(all_ctr) > 0.4


ctr_of_all_search_console_user = Tip(
    category='SEO',
    title = 'CTR меньше 1 процента, люди не кликают на ваш сниппет в поиске!',
    description = 'На протяжении недели CTR всех ваших объявлений достигает меньше одного процента - поменяйте '
                  'заголов и описание сниппета в поиске ( изменив <title> и <description> страницы )',
    analytics_func=ctr_of_all_users,
    is_human_created=False
)


# TIPS version 0.02
# GA_TIPS
def grows_of_new_users_func(metrics:dict):
    new_users = metrics.get('ga_NewUser', {}).get('total', [])[-7:]
    return new_users and sorted(new_users) == new_users


grows_of_new_users = Tip(
    category='Analytics',
    title='Приток новых уникальных пользователей на этой неделе сохранился и растёт последовательно!',
    description='На протяжении недели зафиксирован положительный прирост новых уникальных пользователей. Сохраните '
                'настройки каналов маркетинга для дальнейшего повышения роста новых пользователей, который влияет но '
                'повышение показателя уникальной конверсии!',
    analytics_func=grows_of_new_users_func
)


# GA_TIP
def low_ga_page_views_per_session_func(metrics: dict):
    weekly_views = metrics.get('ga_pageViewsPerSession', {}).get('total', [])[-7:]
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
                'Советуем изменить страницы входа пользователя, проверить настройки меню и навигации на вашем сайте, '
                'пересмотреть настройки рекламы привлечения трафика.',
    analytics_func=low_ga_page_views_per_session_func
)


# GA_TIP
def low_ga_returning_user_func(metrics : dict):
    weekly_returning = metrics.get('ga_ReturningUser', {}).get('total', [])[-7:]
    average = sum(weekly_returning)/7
    return 0.25 < average < 0.5


low_ga_returning_user = Tip(
    category='Analytics',
    title='Пользователи не активно возвращаются на главный домен.',
    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                'Проверьте настройки вашего ремаркетинга и ретаргетинга, увеличьте частоту показа вашей рекламы для '
                'возвраты трафика, а также просмотрите показатель “CTR” ваших объявлений для полного решения проблем '
                'в процессе возвращения вашего трафика.',
    analytics_func=low_ga_returning_user_func
)


# GA_TIP
def no_ga_returning_user_func(metrics:dict):
    weekly_returning = metrics.get('ga_ReturningUser', {}).get('total', [])[-7:]
    average = sum(weekly_returning) / 7
    return average < 0.25


no_ga_returning_user = Tip(
    category='Analytics',
    title='Пользователи не возвращаются на главный домен.',
    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                'Более 55% онлайн бизнесов настраивают ремаркетинг и ретаргетинг для рекламы своего сайта. '
                'Это позволяет проекту быть всегда “на слуху” у пользователя!'
                'Используйте технологию ремаркетинга в Google Adwords или Yandex Direct, а также протестируйте '
                'ретаргетинг в социальных для возврата пользователей '
                'на сайт - это сможет повысить количество повторяющихся продаж, а также поднимет вашу конверсию.',
    analytics_func=no_ga_returning_user_func
)


# GA_TIP
def right_ga_returning_user_func(metrics: dict):
    weekly_returning = metrics.get('ga_ReturningUser', {}).get('total', [])[-7:]
    average = sum(weekly_returning) / 7
    return average > 0.8


right_ga_returning_user = Tip(
    category='Analytics',
    title='Вы отлично возвращаете пользователей на ваш главный домен.',
    description='Вы отлично возвращаете пользователей на ваш сайт, это повышает показатель вашей конверсии и '
                'повторяющихся успехов в ваших бизнес - целях. Советуем повысить бюджет вашей ремаркетинговой или '
                'ретаргетинговой рекламы в целях усиление данного канала и повышения важных для бизнеса метрик!',
    analytics_func=right_ga_returning_user_func
)


# GA_TIP
def right_avg_session_duration_func(metrics: dict):
    session_duration = metrics.get('ga_avgSessionDuration', {}).get('total', [])[-7:]
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


# GA_TIP
def low_avg_session_duration_func(metrics:dict):
    session_duration = metrics.get('ga_avgSessionDuration', {}).get('total', [])[-7:]
    average = sum(session_duration) / 7
    return 1.0 < average < 1.5


low_avg_session_duration = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы меньше, чем 35% сайтов.',
    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего '
                'главного домена в поисковике.Постарайтесь удержать внимание Вашего пользователя на сайте дольше, '
                'чем есть сейчас - добавив больше навигационных подсказок пути пользователя на вашей странице.',
    analytics_func=low_avg_session_duration_func
)


# GA_TIP
def no_avg_session_duration_func(metrics: dict):
    session_duration = metrics.get('ga_avgSessionDuration', {}).get('total', [])[-7:]
    average = sum(session_duration) / 7
    return average < 1.0


no_avg_session_duration = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы меньше, чем 85% сайтов',
    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего '
                'главного домена в поисковике. '
                'Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше '
                'навигационных подсказок пути пользователя на вашей странице. '
                'А также проверьте настройки ваших маркетинговых каналов по привлечению трафика - релевантный ли трафик заходит к вам на сайт?',
    analytics_func=no_avg_session_duration_func
)


# GA_TIP
def loss_of_new_users_func(metrics:dict):
    new_users = metrics.get('ga_NewUser', {}).get('total', [])[-7:]
    return new_users and sorted(new_users, reverse=True) == new_users


loss_of_new_users = Tip(
    category ='Analytics',
    title='Приток новых уникальных пользователей на этой неделе упал!',
    description='На протяжении недели зафиксировано падение новых уникальных пользователей. '
                'Проверьте состояние каналов маркетинга для исправления и повышения данной метрики для увеличения '
                'показателей ранжирования сайта и новой уникальной конверсии.',
    analytics_func=loss_of_new_users_func
)


#TIPS version 0.03
# GA_TIP
def critical_load_time(metrics: dict):
    week_slice = metrics.get('ga_avgPageLoadTime', {}).get('total', [])[-7:]
    for item in week_slice:
        if item > 3:
            return True
    return False


crytical_ga_avg_page_load_time = Tip(
    category='Analytics',
    title='Скорость загрузки страницы не оптимизирована!',
    description='Скорость загрузки ваших страниц сайта не оптимизирована. В данный момент средний показатель '
                'составляет больше 3-ёх секунд, что недопустимо для поисковых систем, а главное Ваших поведенческих '
                'показателей пользователей. Данная метрика отрицательно влияет на ваши показатели в ранжировании и '
                'конверсии. Постарайтесь сократить ненужный код на сайте, а так же кэшировать изображения на вашем '
                'сайте для улучшения данного показателя.',
    analytics_func=critical_load_time
)


# GA_TIP
def avg_load_time(metrics: dict):
    week_slice = metrics.get('ga_avgPageLoadTime', {}).get('total', [])[-7:]
    for item in week_slice:
        if item > 2:
            return True
    return False


avg_ga_avg_page_load_time = Tip(
    category='Analytics',
    title='Скорость загрузки оптимизирована недостаточно.',
    description='Скорость загрузки ваших страниц сайта не оптимизирована в полной мере. В данный момент средний '
                'показатель составляет больше 2-ёх секунд, что не даёт максимальной эффективности для поисковых '
                'систем, а главное Ваших поведенческих показателей пользователей. Данная метрика отрицательно влияет '
                'на ваши показатели в ранжировании и конверсии. Постарайтесь сократить ненужный код на сайте, '
                'а так же кэшировать изображения на вашем сайте для улучшения данного показателя.',
    analytics_func=avg_load_time
)


# GA_TIP
def critical_time_on_page(metrics: dict):
    week_slice = metrics.get('ga_timeOnPage', {}).get('total', [])[-7:]
    for item in week_slice:
        if item < 10:
            return True
    return False


crytical_ga_time_on_page = Tip(
    category='Analytics',
    title='Пользователи не задерживаются на вашем сайте.',
    description='Пользователи не задерживаются на вашем сайте. Причиной ухудшения данной метрики может быть несколько '
                'событий: на сайт приводится нерелевантный трафик, страницы сайта долго прогружаются, интуитивно '
                'пользователю не понравился дизайн вашего сайта. Постарайтесь исправить хотя бы одно из этих событий, '
                'а Melytix.ai в автоматическом режиме снова измерит Ваши показатели!',
    analytics_func=critical_time_on_page
)


# GA_TIP
def low_time_on_page(metrics: dict):
    week_slice = metrics.get('timeOnPage', {}).get('total', [])[-7:]
    for item in week_slice:
        if item < 30:
            return True
    return False


low_ga_time_on_page = Tip(
    category='Analytics',
    title='Пользователи задерживаются на вашем сайте слишком мало.',
    description='Пользователи задерживаются на вашем сайте слишком мало. Причиной ухудшения данной метрики может быть '
                'несколько событий: на сайт приводится нерелевантный трафик, страницы сайта долго прогружаются. '
                'Постарайтесь исправить хотя бы одно из этих событий, а Melytix.ai в автоматическом режиме снова '
                'измерит Ваши показатели!',
    analytics_func=low_time_on_page
)

# ------------------------------

def mobile_device_branding(metrics: dict):
    all_mobile_devices = metrics.get('mobileDeviceBranding')
    if all_mobile_devices:
        name_of_popular_device = ''
        max_result = 0
        for name, data in all_mobile_devices:
            weekly_sum = sum(data[-7:])
            if max_result < weekly_sum:
                max_result = weekly_sum
                name_of_popular_device = name
        return name_of_popular_device
    return None


mobileDeviceBrandingTip = Tip(
    category='Analytics, Целевая Аудитория',
    title='Ваша целевая аудитория пользуется устройством “mobilDevice”',  # Как вписать сюда название устройства?
    description='Ваша целевая аудитория пользуется устройством “mobilDevice”. Внимательно просмотрите дизайн вашего сайта под модели мобильных устройств данного бренда. Так же, при настройках рекламных кампаний направляйте большую часть ( 60% ) рекламного бюджета на устройства данного типа.',
    analytics_func=mobile_device_branding
)


def popular_browser(metrics: dict):
    ga_analytics = metrics.get('google_analytics')
    if ga_analytics:
        all_browsers = ga_analytics.get('browser')
        name_of_popular_browser = ''
        if all_browsers:
            max_result = 0
            for name, data in all_browsers:
                weekly_sum = sum(data[-7:])
                if max_result < weekly_sum:
                    max_result = weekly_sum
                    name_of_popular_browser = name
        else:
            return None
        all_versions = ga_analytics.get('browserVersion')
        version_of_browser = ''
        if all_versions:
            max_counter = 0
            list_of_versions = list(all_versions[name_of_popular_browser])
            set_of_versions = set(list_of_versions)
            for version in set_of_versions:
                if list_of_versions.count(version) > max_counter:
                    max_counter = list_of_versions.count(version)
                    version_of_browser = version
        else:
            return None
        return [name_of_popular_browser, version_of_browser]
    return None


browserTip = Tip(
    category='Analytics, Целевая Аудитория',
    title='Ваша целевая аудитория пользуется браузером - “browser”',    # Как вместо "browser" написать название популярного браузера (переменную)?
    description='Ваша целевая аудитория пользуется браузером - “browser”. Внимательно просмотрите дизайн вашего сайта под этот браузер. Внимательно осмотрите вывод всех ваших элементов сайта на данную версию браузера - “ga_browserVersion”', #Как вместо ga_browserVersion вывести версию браузера?
    analytics_func=popular_browser
)


# Что из себя представляет ga_browserSize
def popular_device(metrics: dict):
    ga_analytics = metrics.get('google_analytics')
    if ga_analytics:
        all_devices = ga_analytics.get('deviceCategory')
        name_of_popular_device = ''
        if all_devices:
            max_result = 0
            for name, data in all_devices:
                weekly_sum = sum(data[-7:])
                if max_result < weekly_sum:
                    max_result = weekly_sum
                    name_of_popular_device = name
            return name_of_popular_device
    return None


deviceCategory = Tip(
    category='Analytics, Целевая Аудитория',
    title='Ваша целевая аудитория пользуется девайсом -  “deviceCategory” ( переменная )',
    description='Ваша целевая аудитория пользуется девайсом -  “deviceCategory”. Проверьте адаптивность дизайна '
                'вашего сайта под данный тип устройства. Внимательно проверьте видимость и размер всех элементов для '
                'данного размера типа устройства - “ga_browserSize”. Заметьте, что на вашу конверсию может влиять, '
                'даже размер и цвет кнопки поэтому важные элементы вашей функциональности сайты должны быть выделены '
                'и видны для пользователя на данном типе устройства.',
    analytics_func=popular_device
)


def minor_languages(metrics: dict):
    ga_analytics = metrics.get('google_analytics')
    if ga_analytics:
        all_languages = ga_analytics.get('language')
        if all_languages:
            main_language = ''
            max_data = 0.0
            total = 0.0
            for language, data in all_languages:
                current_lang_data = sum(data[-7:])
                total += current_lang_data
                if current_lang_data > max_data:
                    main_language = language
                    max_data = current_lang_data
            if max_data / total > 0.8:
                result = ''
                set_of_languages = set(all_languages.keys())
                set_of_languages.discard(main_language)
                for lang in set_of_languages:
                    result += lang
                    result += ', '
                result = result[:-2]
                return [main_language, result]  # Возвращаю 2 строки
            else:
                return [main_language, None]


languageTip = Tip(
    category='Analytics, Целевая Аудитория',
    title=' Ваша целевая аудитория общается не только на “основном языке” ( переменная основного языка )',
    description='Ваша целевая аудитория общается не только на “основном языке” ( переменная основного языка ). Заметьте, ваша основная целевая аудитория использует не только “основной язык”, но ещё и “другие языки” ( переменные названий других языков ). Создайте мультиязычную версию сайта или же проверьте её наличие и грамотный перевод. Это влияет на вашу конверсию!',
    analytics_func=minor_languages
)


def public_interests(metrics: dict):
    ga_analytics = metrics.get('google_analytics')
    if ga_analytics:
        all_interests = ga_analytics.get('interestOtherCategory')
        if all_interests:
            set_of_interests = set(all_interests.keys())
            result = ''
            for item in set_of_interests:
                result += item
                result += ', '
            result = result[:-2]
            return result    # Возвращаю 1 строку, где все категории
    return None


interestOtherCategoryTip = Tip(
    category='Analytics, Целевая Аудитория',
    title='Используйте интересы вашей аудитории в настройках таргетированной рекламы в Facebook, Instagram!',
    description='Melytix.ai провёл анализ Ваших пользователей и выявил важные интересы, которые относятся к вашей целевой аудитории, а именно - (перечисление переменных названий  интересов ). Используйте именно эти интересы для точного попадания в Вашу целевую аудиторию, а система проанализируют повышение Вашей конверсии после появления новых рекламных кампаний.',
    analytics_func=public_interests
)


def popular_cities(metrics: dict):
    ga_analytics = metrics.get('google_analytics')
    if ga_analytics:
        all_cities = ga_analytics.get('city')
        if all_cities:
            dict_of_cities = {}
            for city, data in all_cities:
                sum_data = sum(data[-7:])
                if sum_data in dict_of_cities:
                    dict_of_cities[sum_data].append(city)
                else:
                    dict_of_cities[sum_data] = [city, ]
            result = ''
            counter = 0
            reversed_sorted_keys = sorted(dict_of_cities, reverse=True)
            for key in reversed_sorted_keys:
                counter += len(dict_of_cities[key])
                for name in dict_of_cities[key][:3]:
                    result += name
                    result += ', '
                if counter >= 3:
                    return result
    return  None


extraCityTip = Tip(
    category='Analytics, Целевая Аудитория',
    title='Основные города - ( список городов из переменных ) дают Вам больше всего конверсий!',
    description='Melytix.ai провёл анализ Ваших пользователей и выявил самые популярные города, которые дают Вам больше всего конверсий! Настройте точечные рекламные кампании с гипер - локаций на данные города, чтобы снизить стоимость лида вашей рекламной кампании и повысить ваши конверсии!',
    analytics_func=popular_cities
)


def return_tips():
    return [grows_of_new_users, low_ga_page_views_per_session, low_ga_returning_user, no_ga_returning_user,
            right_ga_returning_user, right_avg_session_duration, low_avg_session_duration,
            no_avg_session_duration, loss_of_new_users]
