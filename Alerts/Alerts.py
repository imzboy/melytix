from Alerts.Alert import Alert


def sessions_lower(metrics: dict):
    if metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 1] < metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 2]:
        return True
    return False


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


def return_alerts():
    return [lower_than_yesterday, always_alert]
