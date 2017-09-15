import subprocess
import os
import json
from zipfile import ZipFile
from flask import Flask, jsonify, render_template, request, send_file
from flask.views import MethodView
from werkzeug.contrib.fixers import ProxyFix
from configparser import RawConfigParser


app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition
config = RawConfigParser()
config.read(os.path.join(BASE_DIR,'settings.ini'))

if config.has_section('defaults'):
    if config.has_option(section='defaults', option='FLASK_RUN_DIRECTORY'):
        FLASK_RUN_DIRECTORY=os.path.expanduser(config.get('defaults', 'FLASK_RUN_DIRECTORY'))
    if config.has_option(section='defaults', option='DREAM3D_DIRECTORY'):
        DREAM3D_DIRECTORY=os.path.expanduser(config.get('defaults', 'DREAM3D_DIRECTORY'))
    if config.has_option(section='defaults', option='TEMPORARY_PIPELINE_FILE_LOCATION'):
        TEMPORARY_PIPELINE_FILE_LOCATION=os.path.expanduser(config.get('defaults', 'TEMPORARY_PIPELINE_FILE_LOCATION'))

class PipelineRunnerAPI(MethodView):
    """
    @Creator: James Fourman
    @Date: 9/14/2017

    """
    def post(self):
        # We need to make sure the request is json otherwise the script will not work properly
        if request.is_json:
            # This section creates a temporary file on the system to send to DREAM.3D CLI
            pipeline_filepath = TEMPORARY_PIPELINE_FILE_LOCATION

            request_json = request.get_json()
            output_file_path = request_json['9']['OutputPath']

            # Write out the pipeline data payload to feed into DREAM.3D
            with open(pipeline_filepath, 'w+') as f:
                f.write(json.dumps(request_json))

            # Run DREAM.3D
            result = subprocess.run(
                [DREAM3D_DIRECTORY + '/bin/PipelineRunner',
                 '-p',
                 pipeline_filepath
                ],
                stdout=subprocess.PIPE
            )

            # Test to make sure the output file path exists to send the files back to the requester
            if output_file_path:
                try:
                    output_filename = next(os.walk(output_file_path))[2][0]
                    return send_file(os.path.join(output_file_path, output_filename), attachment_filename=output_filename)
                except Exception as e:
                    return str(e)

        return jsonify({'message': 'The data payload was not in JSON format'})

class PipelineRunnerArchiveAPI(MethodView):
    """
    @Creator: James Fourman
    @Date: 9/14/2017

    """
    def post(self):
        # We need to make sure the request is json otherwise the script will not work properly
        if request.is_json:
            # This section creates a temporary file on the system to send to DREAM.3D CLI
            pipeline_filepath = TEMPORARY_PIPELINE_FILE_LOCATION

            request_json = request.get_json()
            output_file = request_json['9']['OutputPath']

            # Write out the pipeline data payload to feed into DREAM.3D
            with open(pipeline_filepath, 'w+') as f:
                f.write(json.dumps(request_json))

            # Run DREAM.3D
            result = subprocess.run([DREAM3D_DIRECTORY + '/bin/PipelineRunner', '-p', pipeline_filepath], stdout=subprocess.PIPE)

            # Test to make sure the output file path exists to send the files back to the requester
            if output_file:
                try:
                    # This is the default DREAM.3D output directory
                    outfiles = FLASK_RUN_DIRECTORY + '/Data/Output'

                    filenames = [] # Filenames and locations to add to zip archive
                    # Add files to the list to add to the zip archive from the default DREAM.3D output directory
                    for root, dir, files in os.walk(outfiles):
                        for filename in files:
                            filenames.append(os.path.join(root, filename))

                    # Add files to the list from the specified output directories in the filter configuration
                    for root, dir, files in os.walk(output_file):
                        for filename in files:
                            filenames.append(os.path.join(FLASK_RUN_DIRECTORY, root, filename))

                    # Create zip file name and path
                    zip_filename = os.path.join(FLASK_RUN_DIRECTORY, 'my_python_files.zip')
                    with ZipFile(zip_filename,'w') as zip:
                        # writing each file one by one and store in archive all
                        #  in one level versus absolute paths
                        for file in filenames:
                            zip.write(file, os.path.basename(file))

                    return send_file(zip_filename, attachment_filename='my_python_files.zip')
                except Exception as e:
                    return str(e)


        return jsonify({'message': 'The data payload was not in JSON format'})


# Add the new classes to disect the url string for routing
app.add_url_rule('/pipeline_runner/', view_func=PipelineRunnerAPI.as_view('pipeline_runner'))
app.add_url_rule('/pipeline_runner_archive/', view_func=PipelineRunnerArchiveAPI.as_view('pipeline_runner_archive'))

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
