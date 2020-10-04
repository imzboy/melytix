import uuid

from Alerts.Alert import Alert

from user import append_list, query
# append_list(
#     {'email': 'email'},
#     'alert'
# )

def sessions_lower(metrics: dict):
    if metrics.get('ga_sessions')[len(metrics['ga_sessions'])] < metrics.get('ga_sessions')[len(metrics['ga_sessions']) - 1]:
        return True
    return False

def analyze(metrics, user_smth):
    """A function to check all the different cases of client tips and alerts"""

    lower_than_yesterday = Alert(
        id = str(uuid.uuid4()),
        category='idk',
        title='Your sessions are lover than yesterday',
        description='Your sessions are lover than yesterday',
        analytics_func=sessions_lower
    )

    alerts = [lower_than_yesterday]  # the array of all Alert objects

    for alert in alerts:
        if alert.analytics_func(metrics):
            append_list(
                {'user_smth': user_smth},
                {"Alerts": alert.generate()})
