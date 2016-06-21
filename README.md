# relayer

[![Build Status](https://travis-ci.org/wizeline/relayer.svg)](https://travis-ci.org/wizeline/relayer)


## Contents


1. [About](#about)
2. [Install](#install)
3. [Usage](#usage)
4. [Hacking](#hacking)
    1. [Setup](#setup)
    2. [Testing](#testing)
    3. [Coding conventions](#coding-conventions)


## About

Relayer is a library to emit kafka message and group logs to relay them to kafka for log aggregation.


## Install

Just do:

```
$ pip install git+ssh://git@github.com/wizeline/relayer.git
```


## Usage

TODO

## Hacking

### Setup

First install Python 3 from [Homebrew](http://brew.sh/) and virtualenvwrapper:

```
brew install python3
pip3 install virtualenv virtualenvwrapper
```

After installing virtualenvwrapper please add the following line to your shell startup file (e.g. ~/.zshrc):

```
source /usr/local/bin/virtualenvwrapper.sh
```

Then reset your terminal.

Clone this respository and create the virtual environment:

```
$ git clone https://github.com/wizeline/relayer
$ cd relayer
$ mkvirtualenv relayer
$ workon relayer
$ pip install -r requirements-dev.txt
$ pip install tox
```

### Testing

To run the tests, you just do:

```
$ tox
```


### Coding conventions

We use `editorconfig` to define our coding style. Please [add editorconfig](http://editorconfig.org/#download)
to your editor of choice.

When running `tox` linting will also be run along with the tests. You can also run linting only by doing:

```
$ tox -e flake8
```
