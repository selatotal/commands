import click
from config.config import Config
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
def main():
    pass


@cli.command()
@click.option('--project', '-p', default=None)
def sonar(project):
    """
    Run Sonar checks
    """
    sonar_client = Sonar(config.cfg['sonarqube']['url'], config.cfg['sonarqube']['token'])
    if project:
        return sonar_client.get_project(project)
    return sonar_client.get_favorites()


if __name__ == "__main__":
    cli()
