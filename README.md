# Social-Media-API
An API for a social media application built in Flask.

You can either use the hosted API: https://social-media-api-503f.onrender.com or run by installing it locally.

## Local Installation Instructions

Pull down the source code by cloning the git repository:

```
> git clone https://github.com/HarshitNTiwari/Social-Media-Api.git
```


Navigate to the project directory, create a fresh virtual environment and activate it:

```
> cd Social-Media-Api

> pip install virtualenv

> virtualenv venv

> call venv/Scripts/activate
```

Install the python packages specified in requirements.txt:

```
(venv) > pip install -r requirements.txt
```

Finally, run the app, using the `run.py` file present in the project directory:

```
> python run.py
```

This will run the application on the Flask development server in debug mode.

## Key Dependencies

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [PyMongo](https://pymongo.readthedocs.io/en/stable/)
* [Flask-JWT](https://pythonhosted.org/Flask-JWT/)