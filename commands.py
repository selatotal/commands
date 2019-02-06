import click
from click import UsageError

from gitlab_local.gitlab import Gitlab
from config.config import Config
from jenkins_local.jenkins import Jenkins
from sonar.sonar import Sonar

__author__ = 'Tales Viegas'


config = Config('config.json')


@click.group()
def cli():
    """
    Simple CLI for devops tools
    """
    pass


@cli.command()
@click.option('--project', '-p', default=None, help="Project Name")
def sonar(project):
    """
    Run Sonar checks
    """
    sonar_client = Sonar(config.cfg['sonarqube']['url'], config.cfg['sonarqube']['token'])
    if project:
        return sonar_client.get_project(project)
    return sonar_client.get_favorites()


@cli.command()
@click.argument('command', default='')
def gitlab(command):
    """
    Gitlab Commands

    merge - Create Merge Request
    """
    gitlab_client = Gitlab(config.cfg['gitlab']['url'], config.cfg['gitlab']['token'])
    if command.lower() == 'merge':
        return gitlab_client.merge()
    raise UsageError("Invalid command")


@cli.command()
@click.argument('command', default='')
def jenkins(command):
    """
    Jenkins Commands

    hello - Print jenkins version
    """
    jenkins_client = Jenkins(config.cfg['jenkins']['url'],
                             config.cfg['jenkins']['username'],
                             config.cfg['jenkins']['token'],
                             config.cfg['jenkins']['email'])
    if command.lower() == 'build':
        if config.cfg['jenkins']['integratedBuild']:
            return jenkins_client.integrated_build(config.cfg['gitlab']['url'], config.cfg['gitlab']['token'])
        else:
            return jenkins_client.normal_build()
    raise UsageError("Invalid command")


if __name__ == "__main__":
    cli()
