![Toto logo](logo.svg)

# Toto ![License Badge](https://img.shields.io/badge/license-GPL%203.0-blue)

An open source tool written in python to create imageboards

[Website](https://github.com/malinest/Toto) | [Download](https://github.com/malinest/Toto/releases) | [Source Code](https://github.com/malinest/Toto)

---

## Table of contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Report a bug/issue](#report-an-issue)

## Installation

### Cloning from github

First, clone the source code
	
	$ git https://github.com/malinest/Toto.git Toto

Then install the requirements

    $ pip3 install -r requirements.txt

Once the installation finished you can run Toto by typing this on your console

	waitress-serve --call 'flaskr:create_app'

## Configuration

Toto includes a [configuration file](https://github.com/malinest/Toto/blob/main/Toto/config.ini) that is used to modify some behaviour of the program:

| Name | Description | Example |
| :-: | :-: | :-: |
| **Database** | |
| URL | mongodb connection uri | [example](https://www.mongodb.com/docs/manual/reference/connection-string/)
| DATABASE_NAME | Full name of the database | TotoDB
| **Logging** | |
| LOG_LEVEL | Log level of the logger **on the terminal** | [DEBUG](https://docs.python.org/3/library/logging.html#logging-levels) |
| LOG_FILE | Name of the generated log file | Toto.log |
| LOG_FOLDER | Location where the logs will be stored | /var/log/Toto |

## Screenshots


## Contributing

All contributions are welcome, if you would like to contribute code please [open a pull request](https://github.com/malinest/Toto/pulls) and we will review it asap.

## Report an issue

Found an issue? Or maybe got a feature request? If so please [open an issue](https://github.com/malinest/Toto/issues) on our repository and we will have a look at it