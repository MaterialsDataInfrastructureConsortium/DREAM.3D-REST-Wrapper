### DREAM.3D Flask Rest Wrapper ###

## Requirements

* Python 3.5+
* Pip
* DREAM.3D
* Flask

## Installation

```
pip install -r requirements.txt
```

## configuration ##

```
FLASK_RUN_DIRECTORY=os.path.expanduser('~/flask-dream3d')
DREAM3D_DIRECTORY=os.path.expanduser('~/dream3d')
TEMPORARY_PIPELINE_FILE_LOCATION=os.path.expanduser('~/test_pipeline.json')
```

Replace the locations with whichever directory path you wish.  You can keep the os.path.expanduser even if the directory is not pointing to a home directory in linux or a userprofile directory in windows.

## Execution

`FLASK_APP=pipeline_runner.py flask run`

This will run the flask app on localhost.  If you need to run the flask run `FLASK_APP=pipeline_runner.py flask run --host=0.0.0.0`

## Further Documentation

http://flask.pocoo.org/docs/0.12/

http://dream3d.bluequartz.net/binaries/Help/DREAM3D/index.html
