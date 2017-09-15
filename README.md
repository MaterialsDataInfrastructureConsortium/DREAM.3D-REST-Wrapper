## DREAM.3D Flask Rest Wrapper

### Requirements

* Python 3.5+
* Pip
* DREAM.3D
* Flask

### Installation

```
pip install -r requirements.txt
```

### Configuration
The following should be added to your `settings.ini` file.

```
[defaults]
FLASK_RUN_DIRECTORY: /srv/flask
DREAM3D_DIRECTORY: /srv/dream3d
TEMPORARY_PIPELINE_FILE_LOCATION: /srv/fask/test_pipeline.json

```

Replace the locations with whichever directory path you wish. 

### Execution

`FLASK_APP=pipeline_runner.py flask run`

This will run the flask app on localhost.  If you need to run the flask run `FLASK_APP=pipeline_runner.py flask run --host=0.0.0.0`

### Further Documentation

http://flask.pocoo.org/docs/0.12/

http://dream3d.bluequartz.net/binaries/Help/DREAM3D/index.html
