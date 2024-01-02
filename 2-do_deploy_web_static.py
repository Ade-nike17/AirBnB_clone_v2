#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers using the function do_deploy
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.25.220.49', '18.206.192.41']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        no_ext = archive_name.split('.')[0]
        file_path = "/data/web_static/releases/"

        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/<archive_no_ext>/
        run('sudo mkdir -p {}{}/'.format(file_path, no_ext))
        run('sudo tar -xzf /tmp/{} -C {}{}/'
            .format(archive_name, file_path, no_ext))

        # Delete the archive from the web servers
        run('sudo rm /tmp/{}'.format(archive_name))

        # Move contents of web_static directory
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(file_path, no_ext))

        # Delete the symbolic links
        run('sudo rm -rf {}{}/web_static'.format(file_path, no_ext))
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('sudo ln -s {}{}/ /data/web_static/current'
            .format(file_path, no_ext))

        print("New Version deployed!")

    except Exception as e:
        return False

    # On success
    return True
