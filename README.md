# relayer

[![Build Status](https://travis-ci.org/wizeline/relayer.svg)](https://travis-ci.org/wizeline/relayer)


## Contents


1. [About](#about)
2. [Install](#install)
3. [Usage](#usage)
    1. [RPC](#flask)
    2. [RPC](#rpc)
4. [Hacking](#hacking)
    1. [Setup](#setup)
    2. [Testing](#testing)
    3. [Coding conventions](#coding-conventions)


## About

Relayer is a library to emit kafka messages and group logs to relay them to kafka for log aggregation.


## Install

Just do:

```
$ pip install git+ssh://git@github.com/wizeline/relayer.git
```


## Usage

Relayer supports two different clients, RPC and Flask, depending on which client do you need the initialization steps differ, but once you have a `relayer` object the usage is identical, the relayer object provides two methods:

`relayer.emit(event_type, event_subtype, payload, partition_key=None)`: This method writes directly to a kafka topic, the kafka topic is defined by the `event_type` argument, if `partition_key` is provided all messages sent to that specific `partition_key` are guaranteed to get written to the same partition and the `key` of the message will be the binary representation of that key, the partition key can only be a string, a bytes string or a uuid. The message written is the json encoding of a dictionary containing `event_type`, `event_subtype` and `payload` keys, if the message is not json serializable the exception `NonJSONSerializableMessageError` will be raised.

`relayer.log(log_level, message)`: This method logs a message, all the messages logged gets written to a specific topic at the end of the request (or RPC call), more on this later.

When you do a `relayer.emit` the message gets sent immediatly to kafka, but also a copy gets saved for the purpose of log aggregation. When you create the relayer a `logging_topic` needs to be provided, this argument represents a kafka topic where log information gets written, all the messages written by `relayer.emit` and `relayer.log` gets aggregated for every request (or RPC call) and gets written to the specified `logging_topic` on kafka, so it can later be piped to an ELK stack or similar systems. This special log message also contains metadata related to the request, such as the timestamp and how long did it take to process the request.


### Flask

The Flask relay is a Flask extension, it works by wrapping your Flask application in a middleware so it can aggregate al events and logs emitted by request and flush them out at the end of the request.

__How to use:__

You first need to create the FlaskRelayer extension inside your `extensions.py`, for instance:

```python
from relayer.flask import FlaskRelayer


relayer = FlaskRelayer()
```

After creating it you need to initialize it on your `app.py`

```python
from flask import Flask

from .extensions import relayer

def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_extensions(app):
    relayer.init_app(app, 'logging_topic', kafka_hosts='kafka')
```

Once you've done that you can import `extensions.relayer` from anywhere on your Flask application and use `relayer.emit` and `relayer.log`

### RPC

The RPC relay is intended to be used on RPC services, it works by creating a decorator which handles the connection to the kafka host and aggregates all the emitted events and log messages sent during the lifetime of the decorated method, even when the approach is not dependant on rpc methods it's named like that since it's the most common usage.

When using the rpc relay decorator every method invocation uses its own producer, this is intended so this can be included on multi threaded servers without any hassle.

__How to use:__

First you need to create the relayer decorator invoking `relayer.rpc.make_rpc_relayer`

```python
from relayer.rpc import make_rpc_relayer
rpc_relayer = make_rpc_relayer(logging_topic, kafka_hosts=kafka_hosts)
```

`rpc_relayer` now needs to be accesible to the rpc service methods, imagine you have the following service:

```python
class RPCHandler(object):

    def service_method(self, some_argument):
        pass
```

To make the relayer accesible you need to decorate your service method like:

```python
class RPCHandler(object):

    @rpc_relayer
    def service_method(self, some_argument, relayer=None):
        pass
```

Every method decorated by the `rpc_relayer` needs to take a `relayer` kwarg where the relayer instance will be injected, this relayed argument is then used by the service to either log messages or emit events (persisted on kafka). Besides this the log message emitted will contain information such as how long did the service took to complete, the name of the method (`RPCHandler.service_method`) and the date where the service invokation took place.

#### How to make rpc_relayer accesible to the service definition

Creating `rpc_relayer` by calling `relayer.rpc.make_rpc_relayer` it's usually done inside a method which is in charge of
initializing the service, this makes hard for the decorator to be accesible on the service class definition, to help to achieve that we recommend the following project structure:

```
|_ your_project
\
 |_ rcp_app.py
 |_ rpc_handler.py
 |_ extensions.py
```

Let's examine those files and how they probably look

__rpc_app.py__:

This is your application entry point, imagine it looks like


```python
from .rpc_handler import RPCHandler

def init():
    # Somehow create RPC server serving RPCHandler
    pass

if __name__ == '__main__':
    init()

```

__rpc_handler.py__:

This is where you actually implement your service, it probably looks like

```python

class RPCHandler(object):
    def service_method(self, some_argument):
        # TODO: Actually implement the service
        pass
```

To integrate the RPC relayer you'll need to have the following file

__extensions.py__: 

This file is intended to load any extension needed on the service handler, like the rpc handler, it should look like:

```python
from relayer.rpc import make_rpc_relayer

rpc_relayer = None

def init_relayer(logging_topic, kafka_hosts=None):
    global rpc_relayer
    rpc_relayer = make_rpc_relayer(logging_topic, kafka_hosts=kafka_hosts)
```

Once you have done this, you'll need to update your `rpc_app.py` so it calls `extensions.init_relayer`, since the `rpc_relayer` will be imported and used by `rpc_handler.py` it is important that `init_relayer` is called **before** importing `rpc_handler.py`

```python
from .extensions import init_relayer

def init():
    init_relayer('logging_topic', kafka_hosts='kafka:9092')
    from .rpc_handler import RPCHandler # This should be imported after init_relayer gets invoked
    # Somehow create RPC server serving RPCHandler
    pass

if __name__ == '__main__':
    init()
```

And finally you can actually use the `rpc_relayer` from your `rpc_handler.py`:

```python
from .extensions import rpc_relayer

@rpc_relayer
class RPCHandler(object):
    def service_method(self, some_argument):
        # TODO: Actually implement the service
        pass
```



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
