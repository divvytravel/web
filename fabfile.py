# -*- coding: utf-8 -*-

import os

from fabric.api import env, local, sudo, settings, cd, lcd
from fabric.contrib import files

from fabtools import require

env.project_name = 'divvy'
env.project_user = env.project_name

env.db_name = '%s_db' % env.project_name
env.db_pass = ''
env.db_user = '%s_dbuser' % env.project_name

if not env.hosts:
    env.hosts = ['%(project_user)s@beta.divvy.travel' % env]

env.path = '/srv/sites/%(project_name)s' % env
env.venv_path = '/srv/venvs/%(project_name)s' % env

env.local_project_path = os.path.join(os.path.dirname(__file__), 'src')


def create_translate_files():
    with lcd(env.local_project_path):
        local('python manage.py makemessages -l en')
        local('python manage.py makemessages -l ru')
        local('python manage.py compilemessages')


def update_local():
    local('git pull')
    local('pip install -r requirements.txt')
    local('python ./src/manage.py syncdb')
    local('python ./src/manage.py migrate')
    local('python ./src/manage.py collectstatic --noinput')


def create_project_user(pub_key_file, username=None):
    """
    Creates linux account, setups ssh access.

    Example::

        fab create_project_user:"/home/indieman/.ssh/id_rsa.pub"

    """
    require.deb.packages(['sudo'])

    with open(os.path.normpath(pub_key_file), 'rt') as f:
        ssh_key = f.read()

    username = username or env.project_user

    with (settings(warn_only=True)):
        sudo('adduser %s --disabled-password --gecos ""' % username)

    if username == 'root':
        home_dir = '/root/'
    else:
        home_dir = '/home/%s/' % username

    with cd(home_dir):
        sudo('mkdir -p .ssh')
        files.append('.ssh/authorized_keys', ssh_key, use_sudo=True)
        sudo('chown -R %s:%s .ssh' % (username, username))

    line = '%s ALL=(ALL) NOPASSWD: ALL' % username
    files.append('/etc/sudoers', line)


def setup_server():
    """
    Setup project on clean Ubuntu server
    """
    require.deb.packages([
        'sudo',
        'mc',
        'git',
        'nginx',
    ])

    require.postgres.server()
