#!/usr/bin/python3
"""
This module provides a function to create a .tgz archive from web_static folder
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""

    time = datetime.now()

    # obtain the current date and time
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'

    # use fabric function to create directory if it doesn't exist
    local('mkdir -p versions')

    # Construct path where archive will be saved
    create = local('tar -cvzf versions/{} web_static'.format(archive))

    # Check archive Creation Status
    if create is not None:
        return archive
    else:
        return None
