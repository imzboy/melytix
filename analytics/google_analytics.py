from functools import reduce
from analytics.base import MetricAnalyzer, MetricNotFoundException, Tip, Alert

import datetime


# class GaSessionsAnalyzer(MetricAnalyzer):

#     def __init__(self, metrics: dict):
#         self.metric = metrics.get('google_analytics', {}).get('ga_sessions')
#         if not self.metric:
#             raise MetricNotFoundException('ga_sessions not found')


class GaUsersAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_users')
        if not self.metric:
            raise MetricNotFoundException('ga_users not found')

    def critical_low_ga_users(self, alg_id) -> Alert:
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

    def critical_high_ga_users(self, alg_id) -> Alert:
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

    def path_to_grow_ga_users(self, alg_id) -> Alert:
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

    def path_to_low_ga_users(self, alg_id) -> Alert:
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

    def mobile_device_branding(self, alg_id) -> Tip:
        if (all_mobile_devices := self.metric.get('ga_mobileDeviceBranding')):
            all_mobile_devices.pop('total')
            all_mobile_devices.pop('(not set)', {})
            main_brand_tuple = max(all_mobile_devices.items(), key=lambda x: sum(x[1][-7:]))  # [0] - key (brand name), [1] - data list
            most_popular_brand = main_brand_tuple[0]
            return Tip(
                _id=alg_id,
                category_en='Analytics, The target audience',
                title_en=f'Your target audience uses the {most_popular_brand}',
                description_en=f'Your target audience uses the {most_popular_brand} device. Look carefully at the '
                               'design of your site for the model of mobile devices of this brand. Also, '
                               'when setting up advertising campaigns, direct the majority (60%) of the advertising '
                               'budget to devices of this type.',
                category='Analytics, Целевая Аудитория',
                title=f'Ваша целевая аудитория пользуется устройством {most_popular_brand}',
                description=f'Ваша целевая аудитория пользуется устройством {most_popular_brand}. Внимательно просмотрите дизайн вашего '
                            'сайта под модели мобильных устройств данного бренда. Так же, при настройках рекламных кампаний '
                            'направляйте большую часть ( 60% ) рекламного бюджета на устройства данного типа.')

    def browser_tip(self, alg_id) -> Tip:
        if (all_browsers := self.metric.get('ga_browser')):
            all_browsers.pop('total')
            all_browsers.pop('(not set)', {})
            main_browser_tuple = max(all_browsers.items(), key=lambda x: sum(x[1][-7:]))  # [0] - key (browser name), [1] - data list
            most_popular_browser = main_browser_tuple[0]
            return Tip(
                _id = alg_id,
                category_en='Analytics, The target audience',
                title_en=f'Your target audience uses a browser - {most_popular_browser}',
                description_en=f'Your target audience uses a browser - {most_popular_browser}. Carefully review the design of your site for this browser.',
                category='Analytics, Целевая Аудитория',
                title=f'Ваша целевая аудитория пользуется браузером - {most_popular_browser}',
                description=f'Ваша целевая аудитория пользуется браузером - {most_popular_browser}. Внимательно просмотрите дизайн вашего сайта под этот браузер.')

    def device_category_tip(self, alg_id) -> Tip:
        if (all_categories := self.metric.get('ga_deviceCategory')):
            all_categories.pop('total',{})
            all_categories.pop('(not set)',{})
            if(all_sizes := self.metric.get('ga_browserSize')):
                all_sizes.pop('total', {})
                all_sizes.pop('(not set)',{})

                main_categories_tuple = max(all_categories.items(), key=lambda x: sum(x[1][-7:]))  # [0] - key (category name), [1] - data list
                most_popular_category = main_categories_tuple[0] if main_categories_tuple[0] != 'total' else main_categories_tuple[1]

                main_device_size_tuple = max(all_sizes.items(), key=lambda x: sum(x[1][-7:]))  # [0] - key (size_str), [1] - data list
                most_popular_size = main_device_size_tuple[0]

                return Tip(
                    _id = alg_id,
                    category_en='Analytics, The target audience',
                    title_en=f'Your target audience uses the device - {most_popular_category}',
                    description_en=f'Your target audience uses the device - {most_popular_category}. Check the '
                                   'responsiveness of your site design for this type of device. Carefully check the '
                                   f'visibility and size of all items for a given device type size - {most_popular_size}. '
                                   'Note that even the size and color of the button can affect your conversion, '
                                   'so important elements of your site functionality should be highlighted and '
                                   'visible to the user on this type of device.',

                    category='Analytics, Целевая Аудитория',
                    title=f'Ваша целевая аудитория пользуется девайсом -  {most_popular_category}',
                    description=f'Ваша целевая аудитория пользуется девайсом -  {most_popular_category}. Проверьте адаптивность дизайна '
                                'вашего сайта под данный тип устройства. Внимательно проверьте видимость и размер всех элементов для '
                                f'данного размера типа устройства - {most_popular_size}. Заметьте, что на вашу конверсию может влиять, '
                                'даже размер и цвет кнопки поэтому важные элементы вашей функциональности сайты должны быть выделены '
                                'и видны для пользователя на данном типе устройства.')

    def language_tip(self, alg_id) -> Tip:
        if (all_languages := self.metric.get('ga_language')):
            main_language_tuple = max(all_languages.items(), key=lambda x: sum(x[1][-7:]))  # [0] - key (language name), [1] - data list
            total_sum = sum(sum(i[-7:]) for i in all_languages.values())
            if total_sum:  # to bypass ZeroDivisionError
                if float(sum(main_language_tuple[1]) / total_sum) > 0.8 :
                    set_of_languages = set(all_languages.keys())
                    set_of_languages.discard(main_language_tuple[0])
                    string_languages = str(set_of_languages)[1:-1]
                    str_main_language = main_language_tuple[0]
                    return Tip(
                        _id = alg_id,
                        category_en='Analytics, The target audience',
                        title_en=f'Your target audience speaks not only in the {str_main_language}',
                        description_en=f'Your target audience does not only communicate in the {str_main_language}.'
                                       f'Note that your main target audience uses not only {str_main_language} but also '
                                       f'{string_languages}. Create a multilingual version of the site or check its '
                                       'availability and correct translation. This affects your conversion!',
                        category='Analytics, Целевая Аудитория',
                        title=f'Ваша целевая аудитория общается не только на {str_main_language}',
                        description=f'Ваша целевая аудитория общается не только на {str_main_language}. '
                                    f'Заметьте, ваша основная целевая аудитория использует не только {str_main_language},'
                                    f' но ещё и {string_languages}. Создайте мультиязычную версию сайта или же проверьте '
                                    'её наличие и грамотный перевод. Это влияет на вашу конверсию!')

    def interest_other_category_tip(self, alg_id) -> Tip:
        if (all_interests := self.metric.get('ga_interestOtherCategory')):
            str_interests = str(all_interests.keys())[11:-2]
            return Tip(
                _id = alg_id,
                category_en='Analytics, The target audience',
                title_en='Use the interests of your audience in the settings of targeted advertising on Facebook, Instagram!',
                description_en='Melytix.ai has analyzed your users and identified important interests that relate to '
                               f'your target audience, namely: {str_interests}. Use exactly '
                               'these interests to accurately hit your target audience, and the system will analyze '
                               'the increase in your conversion after new advertising campaigns appear.',
                category='Analytics, Целевая Аудитория',
                title='Используйте интересы вашей аудитории в настройках таргетированной рекламы в Facebook, Instagram!',
                description='Melytix.ai провёл анализ Ваших пользователей и выявил важные интересы, которые относятся к вашей '
                            f'целевой аудитории, а именно: {str_interests}. Используйте именно эти '
                            'интересы для точного попадания в Вашу целевую аудиторию, а система проанализируют повышение Вашей '
                            'конверсии после появления новых рекламных кампаний.')

    def extra_city_tip(self, alg_id) -> Tip:
        if (all_cities := self.metric.get('ga_city')):
            all_cities.pop('total', {})
            all_cities.pop('(not set)', {})
            sorted_cities_dict = dict(sorted(all_cities.items(), key=lambda x: sum(x[1][-7:]), reverse=True))
            sorted_cities_names = list(sorted_cities_dict.keys())
            sorted_cities_names = sorted_cities_names[:3]
            str_cities = str(sorted_cities_names)[1:-1]
            return Tip(
                _id = alg_id,
                category_en='Analytics, The target audience',
                title_en=f'Major cities - {str_cities} gives you the most conversions!',
                description_en='Melytix analyzed your users and identified the most popular cities that give you the '
                               'most conversions! Set up targeted advertising campaigns from hyper - locations to '
                               'city data to reduce the cost per lead of your advertising campaign and increase your '
                               'conversions!',
                category='Analytics, Целевая Аудитория',
                title=f'Основные города - {str_cities} дают Вам больше всего конверсий!',
                description='Melytix.ai провёл анализ Ваших пользователей и выявил самые популярные города, которые дают Вам '
                            'больше всего конверсий! Настройте точечные рекламные кампании с гипер - локаций на данные города, '
                            'чтобы снизить стоимость лида вашей рекламной кампании и повысить ваши конверсии!')


class GaBouncesAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_bounces')
        if not self.metric:
            raise MetricNotFoundException('ga_bounces not found')

    def ga_bounces_crytical_func(self, alg_id) -> Alert:
        if (week_ga_bounces_list := self.metric.get('total')[-7:]):
            weekly_sum = sum(week_ga_bounces_list)
            if weekly_sum / 7 > 50:
                return Alert(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='The average site bounce rate increased by more than 50%, which is unacceptable for Google search engines.',
                    description_en='The average bounce rate on the site has grown and is now over 50%. Your search '
                                   'engine rankings go down and customers spend less time on the site than possible. '
                                   'Check the landing pages to which you drive traffic on the first touch with the '
                                   'client.',
                    category=' Analytics',
                    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
                    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше '
                                'ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на '
                                'сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик '
                                'при первом касании с клиентом.')

    def ga_bounces_bad_func(self, alg_id) -> Alert:
        if (week_ga_bounces_list := self.metric.get('total')[-7:]):
            weekly_sum = sum(week_ga_bounces_list)
            if 25 < weekly_sum / 7 < 50:
                return Alert(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='The average site bounce rate is greater than 25%, which is unacceptable for your customers and Google search engines.',
                    description_en='The average bounce rate on the site has grown and is now over 25%. Your search '
                                   'engine rankings go down and customers spend less time on the site than possible. '
                                   'Check the landing pages to which you attract traffic on the first touch with the '
                                   'client, as well as the page load speed and pageview depth.',
                    category=' Analytics',
                    title='Средний показатель отказов по сайту повысился больше, чем 50%, что неприемлемо для поисковых систем Google и Yandex',
                    description='Средний показатель отказов на сайте вырос и сейчас он больше, чем 50%. Ваше '
                                'ранжирование в поисковой системе понижается, а клиенты проводят меньше времени на '
                                'сайте, чем возможно. Проверьте посадочные страницы на которые вы привлекаете трафик '
                                'при первом касании с клиентом.')

    def ga_bounces_crytical_day_bad_func(self, alg_id) -> Alert:
        if (week_ga_bounces_list := self.metric.get('total')[-7:]):
            for item in week_ga_bounces_list:
                if item > 50:
                    day = week_ga_bounces_list.index(item) + 1
                    day = (datetime.datetime.now() - datetime.timedelta(days=7-day)).date().isoformat()
                    return Alert(
                        _id=alg_id,
                        category_en='Analytics',
                        title_en=f'The bounce rate for the site increased more than 50%  on {day} day',
                        description_en=f'On the {day} day, a bounce rate of more than 50% was noticed on your site - '
                                       'this is bad news for you, but you should analyze all marketing channels and '
                                       'understand which channel brought irrelevant traffic. Analyze with Google '
                                       'Analytics Dashboard - Traffic Sources comparing metric to “Bounce Rate”',
                        category=' Analytics',
                        title=f'Показатель отказов по сайту повысился больше, чем 50% в {day}',
                        description=f'В {day} день на вашем сайте был замечен показатель больше, чем 50% - это плохая новость для Вас, но с помощью неё можно проанализировать все маркетинговые каналы'
                                    ' и понять какой канал привёл нерелеватный трафик, которых не “зацепила” посадочная страница. Проведите анализ '
                                    'с помощью сводки Google Analytics - Источники трафика сравнивая показатель с “Bounce Rate” ( рус. Показатель Отказов ).')


class GaReturningUserAnalyzer(MetricAnalyzer):

    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_returningUser')
        if not self.metric:
            raise MetricNotFoundException('ga_ReturningUser not found')

    def ga_path_to_low_returning_user_func(self, alg_id) -> Alert:
        if (returning_users := self.metric.get('total')[-7:]):
            if sorted(returning_users, reverse=True) == returning_users:
                return Alert(
                    _id = alg_id,
                    category_en='Analytics',
                    title_en='The rate of return of users to the site has been falling every day for the last 7 days.',
                    description_en='It looks like new users are not returning to your site. Check the relevance of '
                                   'your remarketing or retargeting sources. User return is an important metric for '
                                   'your conversion rate and ranking for search engines. Refresh your creatives in '
                                   'your return campaigns - they are most likely outdated.',
                    category=' Analytics',
                    title='Показатель возврата пользователей на сайт падает с каждым днём на протяжении последних 7 дней.',
                    description='Похоже новые пользователи не возвращаются к Вам на сайт. Проверьте актуальность источников вашего ремаркетинга или ретаргетинга . Возврат пользователей это важная метрика Вашей конверсии и показатель ранжирования для поисковых систем. '
                                'Обновите ваши креативы на ваших кампаниях нацеленных на возврат пользователей - скорее всего, они утратили актуальность.')

    def ga_path_to_grow_returning_user_func(self, alg_id) -> Alert:
        if (returning_users := self.metric.get('total')[-7:]):
            if sorted(returning_users) == returning_users:
                return Alert(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='The rate of return of users to the site has been increasing every day over the past 7 days.',
                    description_en="Great job! Your remarketing channels are showing great performance and growth over the past 7 days, returning more and more users! This positively adds up to your conversion rate and your snippets' search engine rankings.",
                    category=' Analytics',
                    title='Показатель возврата пользователей на сайт возрастает с каждым днём на протяжении последних 7 дней.',
                    description='Отличная работа! Каналы вашего ремаркетинга показывают отличные показатели и растут за последние 7 дней возвращая'
                                'всё больше и больше пользователей! Это позитивно складывается на вашей конверсии и ранжировании ваших сниппетов в поисковой системе.')

    def low_ga_returning_user_func(self, alg_id) -> Tip:
        if(weekly_returning := self.metric.get('total', [])[-7:]):
            average = sum(weekly_returning) / 7
            if 0.25 < average < 0.5:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='Users are slowly returning to the main domain.',
                    description_en="During a week, users do not return to your page. Check your remarketing and "
                                   "retargeting settings, increase the frequency of your ad for traffic bounces, "
                                   "and view your ads' CTRs for a complete solution to your traffic return process.",
                    category='Analytics',
                    title='Пользователи не активно возвращаются на главный домен.',
                    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                                'Проверьте настройки вашего ремаркетинга и ретаргетинга, увеличьте частоту показа вашей рекламы для '
                                'возвраты трафика, а также просмотрите показатель “CTR” ваших объявлений для полного решения проблем '
                                'в процессе возвращения вашего трафика.')

    def no_ga_returning_user_func(self, alg_id) -> Tip:
        if(weekly_returning := self.metric.get('total', [])[-7:]):
            average = sum(weekly_returning) / 7
            if average < 0.25:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='Users are not returned to the main domain.',
                    description_en='During a week, users do not return to your page. Over 55% of online businesses '
                                   'set up remarketing and retargeting to advertise their website. This allows the '
                                   'project to always be “in the public eye”! Use remarketing technology in Google '
                                   'Adwords, as well as test social retargeting to bring users back to the site - '
                                   'this can increase the number of repeat sales, as well as increase your '
                                   'conversion.',
                    category='Analytics',
                    title='Пользователи не возвращаются на главный домен.',
                    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                                'Более 55% онлайн бизнесов настраивают ремаркетинг и ретаргетинг для рекламы своего сайта. '
                                'Это позволяет проекту быть всегда “на слуху” у пользователя!'
                                'Используйте технологию ремаркетинга в Google Adwords или Yandex Direct, а также протестируйте '
                                'ретаргетинг в социальных для возврата пользователей '
                                'на сайт - это сможет повысить количество повторяющихся продаж, а также поднимет вашу конверсию.')

    def right_ga_returning_user_func(self, alg_id) -> Tip:
        if(weekly_returning := self.metric.get('total', [])[-7:]):
            average = sum(weekly_returning) / 7
            if average > 0.8:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='You are great at returning users to your main domain.',
                    description_en='You are excellent at returning users to your site, it increases your conversion '
                                   'rate and the repeat success rate for your business goals. We advise you to '
                                   'increase your remarketing or retargeting ad budget to strengthen this channel and '
                                   'increase business-critical metrics!',
                    category='Analytics',
                    title='Вы отлично возвращаете пользователей на ваш главный домен.',
                    description='Вы отлично возвращаете пользователей на ваш сайт, это повышает показатель вашей конверсии и '
                                'повторяющихся успехов в ваших бизнес - целях. Советуем повысить бюджет вашей ремаркетинговой или '
                                'ретаргетинговой рекламы в целях усиление данного канала и повышения важных для бизнеса метрик!')


class GaNewUserAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_newUser')
        if not self.metric:
            raise MetricNotFoundException('ga_NewUser not found')

    def grows_of_new_users_func(self, alg_id) -> Tip:
        if(new_users := self.metric.get('total', [])[-7:]):
            if sorted(new_users) == new_users:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en = 'The influx of new unique users has been continuing since the start of the week and still is growing!',
                    description_en='During the week, a positive increase in new unique users was recorded. Save your '
                                   'marketing channel settings to further drive new user growth, which translates '
                                   'into higher Unique Conversion Rates!',
                    category='Analytics',
                    title='Приток новых уникальных пользователей на этой неделе сохранился и растёт последовательно!',
                    description='На протяжении недели зафиксирован положительный прирост новых уникальных пользователей. Сохраните '
                                'настройки каналов маркетинга для дальнейшего повышения роста новых пользователей, который влияет но '
                                'повышение показателя уникальной конверсии!')

    def loss_of_new_users_func(self, alg_id) -> Tip:
        if(new_users := self.metric.get('total', [])[-7:]):
            if sorted(new_users, reverse=True) == new_users:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='There are fewer new unique users this week!',
                    description_en='During this week decline of new unique users was detected. Check the health of '
                                   'your marketing channels to correct and improve this metric to increase site '
                                   'rankings and new unique conversions.',
                    category='Analytics',
                    title='Приток новых уникальных пользователей на этой неделе упал!',
                    description='На протяжении недели зафиксировано падение новых уникальных пользователей. '
                                'Проверьте состояние каналов маркетинга для исправления и повышения данной метрики для увеличения '
                                'показателей ранжирования сайта и новой уникальной конверсии.')

class GaPageViewsPerSessionAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_pageviewsPerSession')
        if not self.metric:
            raise MetricNotFoundException('ga_pageviewsPerSession not found')

    def low_ga_page_views_per_session_func(self, alg_id) -> Tip:
        if(weekly_views := self.metric.get('total', [])[-7:]):
            for item in weekly_views:
                if item < 1.5:
                    return Tip(
                        _id = alg_id,
                        category_en='Analytics',
                        title_en='Your traffic is not engaging in viewing content.',
                        description_en='For a week, users are not engaged in exploring the content of the main '
                                       'domain. This problem occurs on sites that make such mistakes, '
                                       'namely 1. Inconveniently located menu for users. 2. Users are directed by '
                                       'advertising to an inappropriate page. 3. The content on the page is not '
                                       'interesting to the incoming traffic. We advise you to change the user login '
                                       'pages, check the menu and navigation settings on your site, revise the '
                                       'settings for advertising traffic attraction.',
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
        self.metric = metrics.get('google_analytics', {}).get('ga_avgSessionDuration')
        if not self.metric:
            raise MetricNotFoundException('ga_avgSessionDuration not found')

    def right_avg_session_duration_func(self, alg_id) -> Tip:
        if(session_duration := self.metric.get('total', [])[-7:]):
            average = reduce(lambda x, y: float(x) + float(y), session_duration) / 7
            if average > 1.3:
                return Tip(
                    _id = alg_id,
                    category_en='Analytics',
                    title_en='In terms of average session duration, you are less than 35% of sites.',
                    description_en="Average session length is one of the top behavioral factors for ranking your main "
                                   "domain in search engines. Try to keep your user's attention on the site longer "
                                   "than you have now - by adding more user path navigation cues on your page.",
                    category='Analytics',
                    title='В показателе средней продолжительности сеанса вы больше, чем 56% сайтов.',
                    description='Вы отлично удерживаете внимание пользователя на вашем сайте, аудитория достаточно активно изучает'
                                ' контент на странице - для повышения данного показателя постарайтесь добавить больше пунктов навигации'
                                ' для дальнейшего продолжения “изучения” пользователя вашего сайта. Хорошая работа!')

    def low_avg_session_duration_func(self, alg_id) -> Tip:
        if(session_duration := self.metric.get('total', [])[-7:]):
            average = reduce(lambda x, y: float(x) + float(y), session_duration) / 7
            if 1.0 < average < 1.5:
                return Tip(
                    _id = alg_id,
                    category_en='Analytics',
                    title_en=' In terms of average session duration, you are less than 35% of sites.',
                    description_en= "Average session length is one of the top behavioral factors for ranking your "
                                    "main domain in search engines. Try to keep your user's attention on the site "
                                    "longer than you have now - by adding more user path navigation cues on your "
                                    "page.",
                    category='Analytics',
                    title='В показателе средней продолжительности сеанса вы меньше, чем 35% сайтов.',
                    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего '
                                'главного домена в поисковике.Постарайтесь удержать внимание Вашего пользователя на сайте дольше, '
                                'чем есть сейчас - добавив больше навигационных подсказок пути пользователя на вашей странице.')

    def no_avg_session_duration_func(self, alg_id) -> Tip:
        if(session_duration := self.metric.get('total', [])[-7:]):
            average = reduce(lambda x, y: float(x) + float(y),  session_duration) / 7
            if average < 1.0:
                return Tip(
                    _id = alg_id,
                    category_en='Analytics',
                    title_en='In terms of average session duration, you are less than 85% of sites.',
                    description_en="Average session length is one of the top behavioral factors for ranking your main "
                                   "domain in search engines. Try to keep your user's attention on the site longer "
                                   "than you have now - by adding more user path navigation cues on your page. And "
                                   "also check the settings of your marketing channels for driving traffic - is the "
                                   "relevant traffic coming to your site?",
                    category='Analytics',
                    title='В показателе средней продолжительности сеанса вы меньше, чем 85% сайтов',
                    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего '
                                'главного домена в поисковике. '
                                'Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше '
                                'навигационных подсказок пути пользователя на вашей странице. '
                                'А также проверьте настройки ваших маркетинговых каналов по привлечению трафика - релевантный ли трафик заходит к вам на сайт?')


class GaAvgPageLoadTimeAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_avgPageLoadTime')
        if not self.metric:
            raise MetricNotFoundException('ga_avgPageLoadTime not found')

    def critical_load_time(self, alg_id) -> Tip:
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if item > 3:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='Page loading speed is not optimized!',
                    description_en="The loading speed of your site pages is not optimized. At the moment, the average "
                                   "indicator is more than 3 seconds, which is unacceptable for search engines, "
                                   "and most importantly, your user behavioral indicators. This metric negatively "
                                   "affects your rankings and conversions. Try to shorten unnecessary code on the "
                                   "site, as well as cache images on your site to improve this indicator.",
                    category='Analytics',
                    title='Скорость загрузки страницы не оптимизирована!',
                    description='Скорость загрузки ваших страниц сайта не оптимизирована. В данный момент средний показатель '
                                'составляет больше 3-ёх секунд, что недопустимо для поисковых систем, а главное Ваших поведенческих '
                                'показателей пользователей. Данная метрика отрицательно влияет на ваши показатели в ранжировании и '
                                'конверсии. Постарайтесь сократить ненужный код на сайте, а так же кэшировать изображения на вашем '
                                'сайте для улучшения данного показателя.')

    def avg_load_time(self, alg_id) -> Tip:
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if item > 2:
                return Tip(
                    _id=alg_id,
                    category_en='Analytics',
                    title_en='The download speed is not optimized enough.',
                    description_en="The loading speed of your website pages is not fully optimized. At the moment, "
                                   "the average indicator is more than 2 seconds, which does not give maximum "
                                   "efficiency for search engines, and most importantly, your user behavioral "
                                   "indicators. This metric negatively affects your rankings and conversions. Try to "
                                   "shorten unnecessary code on the site, as well as cache images on your site to "
                                   "improve this indicator.",
                    category='Analytics',
                    title='Скорость загрузки оптимизирована недостаточно.',
                    description='Скорость загрузки ваших страниц сайта не оптимизирована в полной мере. В данный момент средний '
                                'показатель составляет больше 2-ёх секунд, что не даёт максимальной эффективности для поисковых '
                                'систем, а главное Ваших поведенческих показателей пользователей. Данная метрика отрицательно влияет '
                                'на ваши показатели в ранжировании и конверсии. Постарайтесь сократить ненужный код на сайте, '
                                'а так же кэшировать изображения на вашем сайте для улучшения данного показателя.')


class GaTimeOnPageAnalyzer(MetricAnalyzer):
    def __init__(self, metrics: dict):
        self.metric = metrics.get('google_analytics', {}).get('ga_timeOnPage')
        if not self.metric:
            raise MetricNotFoundException('ga_timeOnPage not found')

    def critical_time_on_page(self, alg_id) -> Tip:
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if float(item) < 10:
                return Tip(
                    _id = alg_id,
                    category_en='Analytics',
                    title_en='Users stay on your site too little',
                    description_en='Users stay on your site too little. The reason for the deterioration of this '
                                   'metric can be several events: irrelevant traffic is sent to the site, site pages '
                                   'take a long time to load. Try to correct at least one of these events, '
                                   'and Melytix.ai will automatically measure your performance again!',
                    category='Analytics',
                    title='Пользователи не задерживаются на вашем сайте.',
                    description='Пользователи не задерживаются на вашем сайте. Причиной ухудшения данной метрики может быть несколько '
                                'событий: на сайт приводится нерелевантный трафик, страницы сайта долго прогружаются, интуитивно '
                                'пользователю не понравился дизайн вашего сайта. Постарайтесь исправить хотя бы одно из этих событий, '
                                'а Melytix.ai в автоматическом режиме снова измерит Ваши показатели!')

    def low_time_on_page(self, alg_id) -> Tip:
        week_slice = self.metric.get('total', [])[-7:]
        for item in week_slice:
            if float(item) < 30:
                return Tip(
                    _id = alg_id,
                    category_en='Analytics',
                    title_en='Users stay on your site too little.',
                    description_en='Users stay on your site too little. The reason for the deterioration of this '
                                   'metric can be several events: irrelevant traffic is sent to the site, site pages '
                                   'take a long time to load. Try to correct at least one of these events, '
                                   'and Melytix.ai will automatically measure your performance again!',
                    category='Analytics',
                    title='Пользователи задерживаются на вашем сайте слишком мало.',
                    description='Пользователи задерживаются на вашем сайте слишком мало. Причиной ухудшения данной метрики может быть '
                                'несколько событий: на сайт приводится нерелевантный трафик, страницы сайта долго прогружаются. '
                                'Постарайтесь исправить хотя бы одно из этих событий, а Melytix.ai в автоматическом режиме снова '
                                'измерит Ваши показатели!')

