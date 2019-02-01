# Commands

Some CLI commands to integrate with DevOps tools

## Installation

```bash
$ pip install -r requirements.txt
```

## Configuration

Create config.json file with following data:

```json
{
  "sonarqube" : {
    "url" : "SONARQUBE URL",
    "token": "SONAR USER TOKEN"
  }
}
```

Sample:
```json
{
  "sonarqube" : {
    "url" : "http://sonarqube.mydomain.com",
    "token": "1231241419831g123123"
  }
}
```

## Usage

### Sonar

List Sonar status of user favorite projects

```bash
$ python commands sonar
```

# License

[MIT](http://en.wikipedia.org/wiki/MIT_License)
