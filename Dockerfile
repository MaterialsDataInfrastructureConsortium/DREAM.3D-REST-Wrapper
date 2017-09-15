############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:16.04

# Set the file maintainer (your name - the file's author)
MAINTAINER James Fourman

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=.
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/flask

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
        python \
        python-pip \
        python-dev \
        libmysqlclient-dev \
        git \
        nginx \
        supervisor \
        tofrodos \
        wget


# Create application subdirectories
WORKDIR $DOCKYARD_SRVHOME
RUN mkdir logs dream3d
VOLUME ["$DOCKYARD_SRVHOME/logs/"]

RUN wget http://dream3d.bluequartz.net/binaries/DREAM3D-6.4.78-Linux-x86_64.tar.gz
RUN tar xvfz DREAM3D-6.4.78-Linux-x86_64.tar.gz
RUN mv DREAM3D-6.4.78-Linux-x86_64.tar.gz dream3d

# Install Python dependencies
RUN pip install --upgrade pip
# RUN pip install gunicorn

# RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisor.conf /etc/supervisor/conf.d/

COPY $DOCKYARD_SRC/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

# Port to expose
EXPOSE 5000

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
RUN chmod +x /srv/flask/entrypoint.sh
RUN fromdos /srv/flask/entrypoint.sh
ENTRYPOINT ["/srv/flask/entrypoint.sh"]
