[![Codacy Badge](https://app.codacy.com/project/badge/Grade/85bed3f075f64c8c9f8566376af4ca14)](https://app.codacy.com?utm_source=bb&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/85bed3f075f64c8c9f8566376af4ca14)](https://app.codacy.com?utm_source=bb&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

# Python Service Sample Application #

This repository provides a working example of a Python System, using the [Zyrous Python Framework](https://backstage.zyrous.com/docs/default/component/python-service/).

## What is this repository for? ##

* Learning about the framework
* Getting boilerplate code

## How do I get set up? ##

The fastest way to get up and running is by using [VDEs](https://backstage.zyrous.com/docs/default/component/vde-documentation). Create a new VDE using this repository's URL (```git@bitbucket.org:zyrous/python-service-sample.git```) first.

## Running the solution ##

From the root code folder (```/python-service-sample```), run the following command:

```bash
$ docker compose up
```

This should build a new Docker container and start the solution automatically. The API will be exposed at ```http://localhost:8000/graphql```. You can interact with the API using any GraphQL client (we recommend [Altair](https://altairgraphql.dev/), although you can also use Postman for queries and mutations).

## Installing dependencies ##

In order to start development, you'll want to install all of the dependencies of the solution. From the ```src/``` directory, use pipenv to install:

```bash
$ pipenv shell
$ pipenv install
$ pipenv install --dev
```

## What's in the solution? ##

The sample System contains two Services:

* An Order Service, for creating and manipulating Order objects
* A Shipping Service, for maintaining information about shipping events (updates).

The following infrastructure is used:

* DynamoDB for inter-service notifications (see [here](https://backstage.zyrous.com/docs/default/component/python-service/messaging-patterns/notify-observe/) for more information).
* DynamoDB for storing Order and Shipping domain objects (see [here](https://backstage.zyrous.com/docs/default/component/python-service/repositories/dynamodb/) for more information).

## Running tests ##

First, ensure that you have installed dependencies (see above). From the ```/src``` directory, use the built-in pipenv command to run tests:

```bash
$ pipenv run test-unit
```

To generate coverage reports, use this command:

```bash
$ pipenv run test-unit-coverage
```

**NOTE:** Only unit tests have been added to the project so far. Integration tests will be added at a future time.

## Getting Support ##

Reach out to your Line Leader or the [Python Component Team](https://backstage.zyrous.com/catalog/default/group/python-component-team) for assitance.