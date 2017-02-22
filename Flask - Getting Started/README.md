# Installation
- assuming you have virtualenv/pyvenv, use `virtualenv env` or `python3 -m venv env`
- use `deactivate` to leave the virtual environment
```
      $ mkdir myproject
      $ cd myproject
      $ virtualenv env
...
      $ . env/bin/activate
(env) $  pip install Flask
... (Collecting Flask ... etc)
      $
```

# Running Apps
In the virtual environment (hello is the name of your app)
- flask
```
(env) $ export FLASK_APP=hello.py
(env) $ flask run
* Serving Flask app "hello"
* Running on http://127.0.0.1:5000/ (localhost:5000)
```

- python
```
(env) $ export FLASK_APP=hello.py
(env) $ python -m flask run
```

## Externally Visible Server
If you have debugged disabled or trust users on your network
```
flask run --host=0.0.0.0
```

## Debug Mode
- To activate the debugger, auto reloader, enabling debug mode
```
(env) $ export FLASK_DEBUG=1
```

# Support
- [Python 3 Support](http://flask.pocoo.org/docs/0.12/python3/#python3-support)
- [Installation](http://flask.pocoo.org/docs/0.12/installation/#installation)
- [Flask Admin](https://flask-admin.readthedocs.io/en/latest/)