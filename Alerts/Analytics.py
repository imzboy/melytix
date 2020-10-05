from Alerts.Alerts import return_alerts


from user import append_list, query
# append_list(
#     {'email': 'email'},
#     'alert'
# )


def analyze(metrics, user_email):
    """A function to check all the different cases of client tips and alerts"""

    for alert in return_alerts():
        if alert.analytics_func(metrics):
            append_list(
                {'email': user_email},
                {"Alerts": alert.generate()})
