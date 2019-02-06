# Commands

Some CLI commands to integrate with DevOps tools

## Installation

```bash
$ pip3 install -r requirements.txt
```

## Configuration

Create config.json file with following data:

```json
{
  "sonarqube" : {
    "url" : "SONARQUBE URL",
    "token": "SONAR USER TOKEN"
  },
  "gitlab" : {
    "url" : "GITLAB URL",
    "token": "GITLAB USER TOKEN",
    "integrateSlack": true,
    "slackChannel": "SLACK CHANNEL TO CODE REVIEWS"
  },
  "jenkins" : {
    "url" : "JENKINS URL",
    "username" : "JENKINS USERNAME",
    "token": "JENKINS USER TOKEN OR PASSWORD",
    "email": "email@tosend.result",
    "integrateGitlab": true,
    "integrateSlack": true,
    "slackChannel": "SLACK CHANNEL TO BUILD RESULTS"
  },
  "slack" : {
    "token": "SLACK USER TOKEN"
  }
}

```
Set jenkins.integrateGitlab to true to integrate Gitlab/Jenkins projects

Sample:
```json
{
  "sonarqube" : {
    "url" : "http://sonarqube.mydomain.com",
    "token": "1231241419831g123123"
  },
  "gitlab" : {
    "url" : "https://gitlab.com",
    "token": "1231241419831g123123",
    "integrateSlack": true,
    "slackChannel": "slack-channel"
  },
  "jenkins" : {
    "url" : "http://jenkins.com",
    "username" : "username",
    "token": "1231241419831g123123",
    "email": "email@tosend.result",
    "integrateGitlab": true,
    "integrateSlack": true,
    "slackChannel": "usa-build-jenkins"
  },
  "slack" : {
    "token": "1231241419831g123123"
  }
}
```

## Usage

### Sonar

List Sonar status of user favorite projects

```bash
$ python3 commands.py sonar
```

### Gitlab

Gitlab commands

```bash
$ python3 commands.py gitlab [COMMAND]

List of Commands
  - merge - Create merge request
``` 

### Jenkins

Jenkins commands

# License

```bash
$ python3 commands.py jenkins [COMMAND]

List of Commands
  - build - Build a job
``` 

[MIT](http://en.wikipedia.org/wiki/MIT_License)
