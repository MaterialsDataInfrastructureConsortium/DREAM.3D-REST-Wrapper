#!/bin/bash
# chown uwsgi /static
# chown uwsgi /media

# mkdir -p /var/log/uwsgi
#
# python manage.py collectstatic --noinput
# python manage.py migrate
# python manage.py createsu
# python manage.py generate_keys
# python manage.py generate_generic_forms
# python manage.py createcachetable

supervisord -n
