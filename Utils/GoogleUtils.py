
def checkedboxed_to_scope(checkedboxed: list) -> list:
    """Turns ['ga', 'sc','yt'] into a Auth.SCOPE list"""
    SCOPE = ['openid', 'email', 'profile']  # deafault scopes
    for system in checkedboxed:
        if system == 'ga':
            SCOPE.append('https://www.googleapis.com/auth/analytics.readonly')
        elif system == 'sc':
            SCOPE.append('https://www.googleapis.com/auth/webmasters.readonly')
        elif system == 'yt':
            SCOPE.append(
                'https://www.googleapis.com/auth/yt-analytics.readonly')
            SCOPE.append(
                'https://www.googleapis.com/auth/youtube.readonly'
            )
    return SCOPE