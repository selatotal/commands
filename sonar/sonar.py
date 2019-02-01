import json

import requests
from termcolor import colored


class Sonar:

    ENDPOINT_FAVORITES = '/api/favorites/search'
    ENDPOINT_COMPONENT_MEASURES = '/api/measures/component?' + \
                                  'metricKeys=coverage,blocker_violations,critical_violations,major_violations,' + \
                                  'duplicated_blocks&component='
    ENDPOINT_PROJECT_SEARCH = '/api/components/search?qualifiers=TRK&q='

    def __init__(self, server, token):
        self.token = token
        self.server = server

    def get_favorites(self):
        output = self.__do_request__(self.ENDPOINT_FAVORITES)
        for project in output['favorites']:
            self.get_project_info(project)

    def get_project(self, project):
        output = self.__do_request__(self.ENDPOINT_PROJECT_SEARCH + project)
        for project in output['components']:
            self.get_project_info(project)

    def get_project_info(self, project):
        analyse = self.get_project_analyses(project['key'])
        results = {}
        for metric in analyse['component']['measures']:
            results[metric['metric']] = metric['value']
        error_duplicated = error_bugs = error_coverage = False
        if int(results['duplicated_blocks']) > 0:
            error_duplicated = True
        total_bugs = (int(results['major_violations']) + int(results['blocker_violations']) + int(
            results['critical_violations']))
        if total_bugs > 0:
            error_bugs = True
        if float(results['coverage']) < 75.0:
            error_coverage = True
        print("Project: ", project['name'], ' - ', end='')
        if error_bugs:
            print(colored('Bugs: ' + str(total_bugs), "red"), ' - ', end='')
        else:
            print("Bugs: " + str(total_bugs), ' - ', end='')
        if error_coverage:
            print(colored("Coverage: " + results['coverage'], 'red'), ' - ', end='')
        else:
            print("Coverage: " + results['coverage'], ' - ', end='')
        if error_duplicated:
            print(colored("Duplicate Code: " + results['duplicated_blocks'], 'red'))
        else:
            print("Duplicate Code: " + results['duplicated_blocks'])

    def get_project_analyses(self, project):
        return self.__do_request__(self.ENDPOINT_COMPONENT_MEASURES + project)

    def __do_request__(self, url):
        request_url = self.server + url
        session = requests.Session()
        session.auth = self.token, ''
        call = getattr(session, 'get')
        res = call(request_url)
        binary = res.content
        return json.loads(binary)
