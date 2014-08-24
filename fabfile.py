# -*- coding: utf-8 -*-

import os

from fabric.api import env, local, sudo, settings, cd, lcd, task, run
from fabric.contrib import files

from fabtools import require, git, supervisor
from fabtools.python import virtualenv
from fabtools.service import restart
from fabtools.files import upload_template

env.project_name = 'divvy'
env.project_user = env.project_name

if not env.hosts:
    env.hosts = ['{env.project_user:s}@beta.divvy.travel'.format(env=env)]

env.db_name = '%s_db' % env.project_name
env.db_pass = '%s_dbpass' % env.project_name
env.db_user = '%s_dbuser' % env.project_name

env.repository_url = 'git@github.com:divvytravel/web.git'
env.branch = 'master'

env.project_path = '/srv/sites/{env.project_name:s}'.format(env=env)
env.venv_path = '/srv/venvs/{env.project_name:s}'.format(env=env)

env.manage_path = os.path.join(env.project_path, 'src')
env.settings_path = os.path.join(env.project_path, 'src', 'divvy', 'settings')

env.deploy_path = os.path.join(env.project_path, 'deploy')
env.log_path = os.path.join(env.project_path, 'log')
env.static_path = os.path.join(env.project_path, 'static')
env.media_path = os.path.join(env.project_path, 'media')

env.local_project_path = os.path.join(os.path.dirname(__file__), 'src')


@task
def create_translate_files():
    with lcd(env.local_project_path):
        local('python manage.py makemessages -l en')
        local('python manage.py makemessages -l ru')
        local('python manage.py compilemessages')


@task
def update_local():
    local('git pull')
    local('pip install -r requirements.txt')
    local('python ./src/manage.py syncdb')
    local('python ./src/manage.py migrate')
    local('python ./src/manage.py collectstatic --noinput')


@task
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


@task
def manage(command):
    """
    Run manage command.
    """
    with virtualenv(env.venv_path):
        run('{env.manage_path:s}/manage.py {command:s}'.format(env=env, command=command))


@task
def setup_server():
    """
    Setup project on clean Ubuntu server
    """

    sudo('apt-get update')

    require.deb.packages([
        'sudo',
        'mc',
        'git',
        'nginx',
        'supervisor',
        'uwsgi',
        'uwsgi-plugin-python',
        'libpq-dev',
    ])

    # Creating project paths
    sudo('mkdir {env.project_path:s} -p'.format(env=env))
    sudo('chown {env.project_user:s} {env.project_path:s}'.format(env=env))
    sudo('mkdir {env.venv_path:s} -p'.format(env=env))
    sudo('chown {env.project_user:s} {env.venv_path:s}'.format(env=env))

    git.clone(env.repository_url, path=env.project_path, use_sudo=False, user=env.project_user)
    git.checkout(path=env.project_path, branch=env.branch, use_sudo=False, user=env.project_user)

    require.python.virtualenv(env.venv_path, use_sudo=False)

    with virtualenv(env.venv_path):
        require.python.requirements(os.path.join(env.project_path, 'requirements.txt'))

    require.postgres.server()
    require.postgres.user(env.db_user, password=env.db_pass, createdb=False, createrole=True)
    require.postgres.database(env.db_name, env.db_user)

    upload_template(
        filename='conf/server_local.py',
        destination='%(settings_path)s/local.py' % env,
        context={
            'db_name': env.db_name,
            'db_pass': env.db_pass,
            'db_user': env.db_user,
        },
        use_jinja=True
    )

    with cd(env.manage_path):
        run('chmod ogu+x manage.py')

    uwsgi_setup()
    supervisor_setup()
    sudo('rm /etc/nginx/sites-enabled/default')
    nginx_setup()

    manage('syncdb')
    manage('migrate')
    manage('collectstatic --noinput')


@task
def nginx_setup():
    upload_template(
        filename='conf/nginx.conf',
        destination='%(deploy_path)s/nginx_%(project_name)s.conf' % env,
        context={
            'project_name': env.project_name,
            'static_path': env.static_path,
            'media_path':env.media_path,
            'log_path': env.log_path
        },
        use_jinja=True
    )

    sudo('ln -s -f %(deploy_path)s/nginx_%(project_name)s.conf '
         '/etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    restart('nginx')


@task
def uwsgi_setup():
    upload_template(
        filename='conf/uwsgi.ini',
        destination='%(deploy_path)s/uwsgi_%(project_name)s.ini' % env,
        context={
            'project_name': env.project_name,
            'project_path': env.project_path,
            'venv_path': env.venv_path,
        },
        use_jinja=True
    )


@task
def supervisor_setup():
    upload_template(
        filename='conf/supervisor.conf',
        destination='%(deploy_path)s/supervisor_%(project_name)s.conf' % env,
        context={
            'project_name': env.project_name,
            'deploy_path': env.deploy_path,
            'log_path': env.log_path,
        },
        use_jinja=True
    )

    sudo('ln -s -f %(deploy_path)s/supervisor_%(project_name)s.conf '
         '/etc/supervisor/conf.d/%(project_name)s.conf' % env)
    supervisor.update_config()
    supervisor.restart_process('all')
