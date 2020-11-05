from Tips.Tip import Tip


def just_true(metrics: dict):
    return True


always_alert = Tip(
    category='Test',
    title='This is test tip',
    description='The test tip',
    analytics_func=just_true
)


def return_tips():
    return [always_alert]
