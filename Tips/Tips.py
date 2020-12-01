from Tips.Tip import Tip


def ctrOfAllSCUser(metrics: dict):
    ctr = metrics.get('sc_ctr')
    if ctr:
        counter = 0
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
    analytics_func=ctrOfAllSCUser
)


def growsOfNewUsers(metrics:dict):
    ctr = metrics.get('ga_NewUser')
    counter =0
    for item in range(len(ctr)):
        if ctr[item] >= ctr[item-1]:
            counter += 1
        elif  counter == 7:
            return True
        else:
            return False


GrowsOfNewUsersFunc = Tip(
    category='Analytics',
    title='Приток новых уникальных пользователей на этой неделе сохранился и растёт последовательно!',
    description='На протяжении недели зафиксирован положительный прирост новых уникальных пользователей.'
                'Сохраните настройки каналов маркетинга для дальнейшего повышения роста новых пользователей. '
                'Сохраните настройки каналов маркетинга для дальнейшего повышения роста новых пользователей, который влияет но повышение показателя уникальной конверсии!',
    analytics_func=growsOfNewUsers
)


def lowGAPageViewsPerSession(metrics:dict):
    ctr = metrics.get('ga_pageViewsPerSession')
    item=1
    for item in range(len(ctr)):
        if ctr[item]<1.5:
            return True

    return False


LowGAPageViewsPerSessionFunc = Tip(
    category='Analytics',
    title='Ваш трафик не просматривает контент вовлеченно.',
    description='На протяжении недели пользователи не вовлеченно изучают контент главного домена. '
                'Данная проблема происходит на сайтах, который допускает такие ошибки, как: '
                '1.Неудобно расположено меню для пользователей. '
                '2. Пользователей направляют рекламой на не релевантную страницу. '
                '3. Контент на странице не интересен приходящему трафику. '
                'Советуем изменить страницы входа пользователя, проверить настройки меню и навигации на вашем сайте, пересмотреть настройки рекламы привлечения трафика.',
    analytics_func=lowGAPageViewsPerSession
)


def LowGAReturingUser(metrics:dict):
    ctr = metrics.get('ga_ReturningUser')
    counter = 0
    for item in range(len(ctr)):
        if 0.25 < ctr[item] <0.5:
            counter += 1
        elif counter == 7:
            return True
        else:
            return False


LowGAReturningUserFunc = Tip(
    category='Analytics',
    title='Пользователи не активно возвращаются на главный домен.',
    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                'Проверьте настройки вашего ремаркетинга и ретаргетинга, увеличьте частоту показа вашей рекламы для возвраты трафика, '
                'а также просмотрите показатель “CTR” ваших объявлений для полного решения проблем в процессе возвращения вашего трафика.',
    analytics_func=LowGAReturingUser
)


def NoGAReturningUser(metrics:dict):
    ctr = metrics.get('ga_ReturningUser')
    counter = 0
    for item in range(len(ctr)):
        if ctr[item] < 0.25:
            counter += 1
        elif counter == 7:
            return True
        else:
            return False


NoGAReturningUserFunc = Tip(
    category='Analytics',
    title='Пользователи не возвращаются на главный домен.',
    description='На протяжении недели пользователи не возвращаются на вашу страницу. '
                'Более 55% онлайн бизнесов настраивают ремаркетинг и ретаргетинг для рекламы своего сайта. '
                'Это позволяет проекту быть всегда “на слуху” у пользователя!'
                'Используйте технологию ремаркетинга в Google Adwords или Yandex Direct, а также протестируйте ретаргетинг в социальных для возврата пользователей '
                'на сайт - это сможет повысить количество повторяющихся продаж, а также поднимет вашу конверсию.',
    analytics_func=NoGAReturningUser
)


def RightGAReturningUser(metrics:dict):
    ctr = metrics.get('ga_ReturningUser')
    counter = 0
    for item in range(len(ctr)):
        if ctr[item] > 0.8:
            counter += 1
        elif counter == 7:
            return True
        else:
            return False


RightGAReturningUserFunc = Tip(
    category='Analytics',
    title='Вы отлично возвращаете пользователей на ваш главный домен.',
    description='Вы отлично возвращаете пользователей на ваш сайт, это повышает показатель вашей конверсии и повторяющихся успехов в ваших бизнес - целях. '
                'Советуем повысить бюджет вашей ремаркетинговой или ретаргетинговой рекламы в целях усиление данного канала и повышения важных для бизнеса метрик!',
    analytics_func=RightGAReturningUser
)


def RightAVGSessionDuration(metrics:dict):
    ctr = metrics.get('ga_avgSessionDuration')
    counter =0
    for item in range(len(ctr)):
        counter += 1
        general = + ctr[item]
        if counter == 7:
            if general/7 > 1.30:
                return True
            else:
                return False


RightAVGSessionDurationFunc = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы больше, чем 56% сайтов.',
    description='Вы отлично удерживаете внимание пользователя на вашем сайте, аудитория достаточно активно изучает'
                ' контент на странице - для повышения данного показателя постарайтесь добавить больше пунктов навигации'
                ' для дальнейшего продолжения “изучения” пользователя вашего сайта. Хорошая работа!',
    analytics_func=RightAVGSessionDuration
)


def LowAVGSessionDuration(metrics:dict):
    ctr = metrics.get('ga_avgSessionDuration')
    counter =0
    for item in range(len(ctr)):
        counter += 1
        general = + ctr[item]
        if counter == 7:
            if 1 < general/7 < 1.5:
                return True
            else:
                return False


LowAVGSessionDurationFunc = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы меньше, чем 35% сайтов.',
    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего главного домена в поисковике.'
                ' Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше навигационных подсказок пути пользователя на вашей странице.',
    analytics_func=LowAVGSessionDuration
)


def NoAVGSessionDuration(metrics:dict):
    ctr = metrics.get('ga_avgSessionDuration')
    counter =0
    for item in range(len(ctr)):
        counter += 1
        general = + ctr[item]
        if counter == 7:
            if general/7 < 1:
                return True
            else:
                return False


NoAVGSessionDurationFunc = Tip(
    category='Analytics',
    title='В показателе средней продолжительности сеанса вы меньше, чем 85% сайтов',
    description='Средняя продолжительность сеансов - один из главных поведенческих факторов ранжирования вашего главного домена в поисковике. '
                'Постарайтесь удержать внимание Вашего пользователя на сайте дольше, чем есть сейчас - добавив больше навигационных подсказок '
                'пути пользователя на вашей странице. А также проверьте настройки ваших маркетинговых каналов по привлечению трафика - релевантный ли трафик заходит к вам на сайт?',
    analytics_func=NoAVGSessionDuration
)


def LossOfNewUsers(metrics:dict):
    ctr = metrics.get('ga_NewUser')
    counter =0
    for item in range(len(ctr)):
        if ctr[item] <= ctr[item-1]:
            counter += 1
        elif  counter == 7:
            return True
        else:
            return False


LossOfNewUsersFunc = Tip(
    category='Analytics',
    title='Приток новых уникальных пользователей на этой неделе упал!',
    description='На протяжении недели зафиксировано падение новых уникальных пользователей. '
                'Проверьте состояние каналов маркетинга для исправления и повышения данной метрики для увеличения показателей ранжирования сайта и новой уникальной конверсии.',
    analytics_func=LossOfNewUsers
)


def return_tips():
    return [CtrOfAllSearchConsoleUser,GrowsOfNewUsersFunc,LowGAPageViewsPerSessionFunc,LowGAReturningUserFunc,NoGAReturningUserFunc,
            RightGAReturningUserFunc,RightAVGSessionDurationFunc,LowAVGSessionDurationFunc,NoAVGSessionDurationFunc,LossOfNewUsersFunc]
