Upgrade guide
#############

The upgrade commands are executed as ``ponytracker`` user::

  # su ponytracker
  $ cd /srv/www/ponytracker

Activate the virtualenv::

  $ source env/bin/activate

Enter in the repository directory::

  $ cd ponytracker # we are now in /srv/www/ponytracker/ponytracker

Upgrade the files using ``git``::

  $ git pull -u master release

Install all new dependencies and upgrade previous ones::

  $ pip install -r requirements.txt --upgrade

Be sure to use the correct configuration file each time you run the
``manage.py`` script by setting the ``DJANGO_SETTING_MODULE`` environment
variable::

  $ export DJANGO_SETTINGS_MODULE=ponytracker.local_settings

Collect static files to the ``STATIC_DIR``::

  $ python manage.py collectstatic

Apply database migrations::

  $ python manage.py migrate

You can now restart ponytracker by restarting ``gunicorn`` or ``uwsgi``
depending of your installation.
Do not forget to restart the celery worker too if you have installed it.
