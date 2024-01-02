#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers using the function do_deploy
"""

from fabric.api import local, env, put, run
from os import path

env.hosts = ['100.25.220.49', '18.206.192.41']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]

        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/<archive_no_ext>/
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
                .format(archive_name, archive_no_ext))

        # Delete the archive from the web servers
        run('sudo rm /tmp/{}'.format(archive_name))

        run('sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
                .format(archive_no_ext, archive_no_ext))

        # Delete the symbolic links
        run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(archive_no_ext))
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
                .format(archive_no_ext))

        print("New Version deployed!")

        return True
    except:
        return False
