#!/usr/bin/python3
"""
This Fabric script is based on file 2-do_deploy_web_static.py
it creates and distributes an archive to my web server,
using the function 'deploy'
"""


from fabric.api import env, put, run, local
from datetime import datetime
import os


env.hosts = ['100.25.220.49', '18.206.192.41']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name-split('.')[0]
        file_path = "/data/web_static/releases/"

        # Upload the archive to /tmp/directory on the web servers
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/<archive_no_ext>/
        run('mkdir -p {}{}'.format(file_path, archive_no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'
            .format(archive_name, file_path, archive_no_ext))

        # Delete the archive from the web servers
        run('rm /tmp/{}'.format(archive_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Move contents and create a new symbolic link /data/web_static/current
        run('mv {0}{1}/web_static/* {0}{1}/'.format(file_path, archive_no_ext))
        run('rm -rf {}{}/web_static'.format(file_path, archive_no_ext))
        run('ln -s {}{}/ /data/web_static/current'
            .format(file_path, archive_no_ext))

        print("New version deployed!")

        return True
    except Exception as e:
        return False


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
