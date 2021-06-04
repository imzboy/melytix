import sys

import requests
from jira import JIRA
from jira.client import GreenHopper

from config.settings import JiraConfig

AUTH = (JiraConfig.LOGIN, JiraConfig.API_KEY)

jira_options = {'server': 'https://melytix-ai.atlassian.net'}
jira = JIRA(options=jira_options, basic_auth=AUTH)


def get_description():
    ex_info = sys.exc_info()
    ex = ex_info[2]
    description = ''
    while ex := ex.tb_next:
        description += f"File {ex.tb_frame.f_code.co_filename}, code {ex.tb_frame.f_code.co_name}," \
                       f" line {ex.tb_frame.f_code.co_firstlineno}\n"
    return description


def create_issue(description: str, summary: str):
    issue_data = {
        "fields": {
            "project": {
                "key": "DEV"
            },
            'summary': summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": description,
                                "type": "text"
                            },
                            {
                                "type": "mention",
                                "attrs": {
                                    "id": "5fce822ecb350d0068250b93",
                                    "text": "@nicknamebos0",
                                },
                            },
                            {
                                "type": "mention",
                                "attrs": {
                                    "id": "5fce83f64d2179006e8c7534",
                                    "text": "@Vlad Magdysh",
                                }
                            },
                            {
                                "type": "mention",
                                "attrs": {
                                    "id": "5e33fac76bd5c40ca395d0ca",
                                    "text": "@Max Teslya",
                                }
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                'name': 'Task'
            }
        }
    }
    issue = requests.post("https://melytix-ai.atlassian.net/rest/api/3/issue",
                          json=issue_data, auth=AUTH)
    return issue.json().get('id')


def create_and_setup_issue(description: str, summary: str):
    if not issue_exist(summary):
        issue_id = create_issue(description, summary)

        # Set transition
        able_transitions = get_able_transition_for_issue(issue_id)
        for transition in able_transitions:
            if transition.get('name') == JiraConfig.TRANSITION_NAME:
                transition_id = transition.get('id')
                set_transition_for_issue(issue_id, transition_id)
                break

        # Set sprint
        board_id = get_board_id(JiraConfig.BOARD_NAME)
        sprint_id = get_sprint_id(JiraConfig.SPRINT_NAME, board_id)
        move_issue_to_sprint(issue_id, sprint_id)


def issue_exist(summary: str):
    issues = jira.search_issues(jql_str="project=Melytix AND status=\"To Do\"")
    for issue in issues:
        if summary == issue.fields.summary:
            return True
    return False


def get_board_id(board_name: str):
    gh = GreenHopper(jira_options, basic_auth=AUTH)
    boards = gh.boards()
    for board in boards:
        if board.name == board_name:
            return board.id


def get_sprint_id(sprint_name: str, board_id: str):
    get_sprints_url = f"https://melytix-ai.atlassian.net/rest/agile/1.0/board/{board_id}/sprint"
    sprints = requests.get(get_sprints_url, auth=AUTH)
    for sprint in sprints.json().get('values'):
        if sprint.get('name') == sprint_name:
            return sprint.get('id')


def get_able_transition_for_issue(issue_id: str):
    url = f"https://melytix-ai.atlassian.net/rest/api/3/issue/{issue_id}/transitions"
    response = requests.get(url, auth=AUTH)
    return response.json().get('transitions')


def set_transition_for_issue(issue_id: str, transition_id: str):
    transition = {
        "transition": {
            "id": transition_id
        }
    }
    response = requests.post(f"https://melytix-ai.atlassian.net/rest/api/3/issue/{issue_id}/transitions",
                             json=transition, auth=AUTH)
    return response.status_code


def move_issue_to_sprint(issue_id: str, sprint_id: str):
    payload = {
        "issues": [issue_id]
    }
    move_to_sprint_url = f"https://melytix-ai.atlassian.net/rest/agile/1.0/sprint/{sprint_id}/issue"
    response = requests.post(move_to_sprint_url, json=payload, auth=AUTH)
    return response.status_code
