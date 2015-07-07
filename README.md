# Flask on Google App Engine

This project combines the ideas from multiple projects to create a working
example of running popular Flask extensions on Google App Engine.

## Installing Dependencies

App Dependencies are managed with zc.buildout. 

```sh
$ python bootstrap-buildout.py
$ ./bin/buildout
```

## Running the app

Running the application is simple using the included bash script.

```sh
$ ./run.sh
```

If you are not using an `sh` compatible shell you can use the following:

```sh
$ ./bin/dev_appserver
```

Flask installs an admin user on first launch with the `admin` role.


	Username: admin@example.org
	Password: password


## Testing the app

There are no tests yet but the runner is configured. Run it with:

```sh
$ ./bin/nosetests

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
```

## Based upon

* [Python Flask Skeleton for Google App Engine](https://github.com/GoogleCloudPlatform/appengine-python-flask-skeleton)
* [Flask-Security](https://github.com/mattupstate/flask-security)
* [Flask-Admin](https://github.com/flask-admin/flask-admin)
* [Flask-Security Example](https://github.com/mattupstate/flask-security-example)
* [Buildout](https://github.com/buildout/buildout)
