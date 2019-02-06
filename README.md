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
    "token": "GITLAB USER TOKEN"
  }
}
```

Sample:
```json
{
  "sonarqube" : {
    "url" : "http://sonarqube.mydomain.com",
    "token": "1231241419831g123123"
  },
  "gitlab" : {
    "url" : "https://gitlab.com",
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

# License

[MIT](http://en.wikipedia.org/wiki/MIT_License)
