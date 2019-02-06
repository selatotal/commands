import time
from jenkinsapi import jenkins
from prompt_toolkit import prompt

from gitlab_local.gitlab import Gitlab
from slack_local.slack import Slack


class Jenkins:

    jk = None
    email = None
    integrate_slack = False
    slack_channel = None
    slack = None

    def __init__(self, server, username, token, email, integrate_slack=False, slack_channel=None, slack_token=None):
        self.jk = jenkins.Jenkins(server, username=username, password=token, timeout=100, lazy=True)
        self.email = email
        self.integrate_slack = integrate_slack
        self.slack_channel = slack_channel
        if integrate_slack:
            self.slack = Slack(slack_token)

    def build(self, project):
        build_params = {
            "buildRefresh": "1",
            "email": self.email,
            "replicas": "1"
        }
        print("Getting job info...")
        inst = self.jk.get_job(project).invoke(build_params=build_params, block=False)
        print("Build starting...")
        build = self.jk.get_job(project).get_build(inst.get_build_number())
        while build.is_running():
            print("Build is running...")
            time.sleep(10)
        message = '{} - {} - #{} - {}console'.format(
            self.jk.get_job(project).get_build(inst.get_build_number()).get_status(),
            project,
            inst.get_build_number(),
            build.get_build_url())
        print(message)
        if self.integrate_slack:
            self.slack.send_message(self.slack_channel, message)

    def normal_build(self):
        project = prompt("Project path: ")
        self.build(project)

    def integrated_gitlab_build(self, server, token):
        gitlab = Gitlab(server, token)
        project = gitlab.ask_project()
        branch = gitlab.ask_branch(gitlab.get_project_structure(project))
        self.build(project+"/"+branch)
