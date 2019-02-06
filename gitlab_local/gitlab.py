from pprint import pprint

import gitlab
from click._unicodefun import click
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from slack_local.slack import Slack


class Gitlab:

    gl = None
    integrate_slack = False
    slack_channel = None
    slack = None

    def __init__(self, server, token, integrate_slack=False, slack_channel=None, slack_token=None):
        self.gl = gitlab.Gitlab(server, private_token=token)
        self.slack_token = slack_token
        self.integrate_slack = integrate_slack
        self.slack_channel = slack_channel
        if integrate_slack:
            self.slack = Slack(token)

    def get_all_projects(self):
        projects = []
        page = 0
        while True:
            next_list = self.gl.projects.list(per_page=1000, page=page)
            if not next_list:
                break
            projects.extend(next_list)
            page += 1
        return projects

    def get_project_structure(self, project_name):
        return self.gl.projects.list(search=project_name)[0]

    def get_projects(self):
        projects = self.get_all_projects()
        for project in projects:
            print(project)

    def get_project_choice(self):
        projects = self.get_all_projects()
        project_list = []
        for project in projects:
            project_list.append(project.name)
        return project_list

    def ask_project(self):
        completer = WordCompleter(self.get_project_choice(), sentence=True)
        answers = prompt("Choose project: ", completer=completer)
        return answers

    def ask_branch(self, project):
        completer = WordCompleter(self.get_project_branches(project), sentence=True)
        answers = prompt("Choose branch: ", completer=completer)
        return answers

    @staticmethod
    def get_project_branches(project):
        branches = []
        for branch in project.branches.list():
            branches.append(branch.name)
        return branches

    def merge(self):
        project_name = self.ask_project()
        project = self.get_project_structure(project_name)
        completer_branch = WordCompleter(self.get_project_branches(project), sentence=True)
        source_branch = prompt("Choose original branch: ", completer=completer_branch)
        target_branch = prompt("Choose final branch: ", completer=completer_branch)
        title = prompt("Title: ")
        code_review = click.confirm("Code Review", default=True)
        mr = project.mergerequests.create({
            'source_branch': source_branch,
            'target_branch': target_branch,
            'title': title})
        if not code_review:
            mr.merge()
        else:
            message = "Code review - {} - {}/diffs <!here> :top:".format(
                title,
                mr.web_url
            )
            pprint(mr.web_url)
            if self.integrate_slack:
                self.slack.send_message(self.slack_channel, message)
