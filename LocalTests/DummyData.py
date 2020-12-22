dummy = {
    "ga_sessions": [5,7,8,4,6,8,3],
    "ga_users": [5,7,8,4,6,8,3],
    "ga_pageViews": [5,7,8,4,6,8,3],
    "ga_pageViewsPerSession": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "ga_avgSessionDuration": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "ga_bounces": [5,7,8,4,6,8,3],
    "ga_percentNewSessions": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "ga_user_dates": ["2020-06-22", "2020-06-23", "2020-06-24", "2020-06-25", "2020-06-26", "2020-06-27", "2020-06-28"],
    "ga_NewUser": [5,0,8,0,6,8,3],
    "ga_ReturningUser": [0,7,0,4,6,0,3],
    "ga_dates": ["2020-06-22", "2020-06-23", "2020-06-24", "2020-06-25", "2020-06-26", "2020-06-27", "2020-06-28"],
    "sc_clicks": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "sc_impressions": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "sc_ctr": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "sc_position": [5.7,7.5,8.4,4.8,6.4,8.8,3.9],
    "sc_dates": ["2020-06-22", "2020-06-23", "2020-06-24", "2020-06-25", "2020-06-26", "2020-06-27", "2020-06-28"],
    "yt_dates": ["2020-06-22", "2020-06-23", "2020-06-24", "2020-06-25", "2020-06-26", "2020-06-27", "2020-06-28"],
    "yt_estimatedMinutesWatched": [5,7,8,4,6,8,3],
    "yt_views": [5,7,8,4,6,8,3],
    "yt_likes": [5,7,8,4,6,8,3],
    "yt_subscribersGained": [5,7,8,4,6,8,3],
    "yt_dislikes": [5,7,8,4,6,8,3]
}


#launch this file via typing in console "python LocalTest/DummyData.py"
#here are the import to algorithms to test
from Alerts.Alerts import sessions_lower


true_metrics = {1, 2, 3, 4, 5, 6, 0}  # here the last day is lower the pre-last day. The True condition
false_metrics = {1, 2, 3, 4, 5, 6, 7}  # here the metrics staidly go up

assert sessions_lower(true_metrics) == True

assert sessions_lower(false_metrics) == False
#if this does not throw AssertionError than the algorithm works
