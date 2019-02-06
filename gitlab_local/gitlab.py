from pprint import pprint

import gitlab
from click._unicodefun import click
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter


class Gitlab:

    gl = None

    def __init__(self, server, token):
        self.gl = gitlab.Gitlab(server, private_token=token)

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
        projlist = []
        for project in projects:
            projlist.append(project.name)
        return projlist

    def ask_project(self):
        completer = WordCompleter(self.get_project_choice(), sentence=True)
        answers = prompt("Choose project: ", completer=completer)
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
            pprint(mr.web_url)
