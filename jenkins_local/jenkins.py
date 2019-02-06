import time
from jenkinsapi import jenkins
from prompt_toolkit import prompt

from gitlab_local.gitlab import Gitlab


class Jenkins:

    jk = None
    email = None

    def __init__(self, server, username, token, email):
        self.jk = jenkins.Jenkins(server, username=username, password=token, timeout=100, lazy=True)
        self.email = email

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
            time.sleep(5)
        print("Build " + build.get_status() + " - " + build.get_result_url()+"/console")

    def normal_build(self):
        project=prompt("Project path: ")
        self.build(project)

    def integrated_build(self, server, token):
        gitlab = Gitlab(server, token)
        project = gitlab.ask_project()
        branch = gitlab.ask_branch(gitlab.get_project_structure(project))
        self.build(project+"/"+branch)
