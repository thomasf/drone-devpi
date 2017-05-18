#!/usr/bin/env python
"""
Everything needed to publish Python modules to a DevPi server.

Recommended reading: http://doc.devpi.net/latest/quickstart-releaseprocess.html
"""
import os
import subprocess
import sys
import urllib.parse

# devpi uses a 'clientdir' arg to determine where to store state. We make
# this overridable below to facilitate the integration test process.
DEFAULT_CLIENTDIR = '/tmp/devpi-clientdir'
VERBOSE = False


def devpi(devpi_command, devpi_args, *,
          verbose=VERBOSE, clientdir=None, **kwargs):
    if verbose:
        devpi_args = ['-v'] + devpi_args

    if clientdir is None:
        clientdir = DEFAULT_CLIENTDIR
    devpi_args = ['--clientdir', clientdir] + devpi_args
    p_args = ['devpi', devpi_command] + devpi_args
    if verbose:
        print(" ".join(p_args))
    cmd = subprocess.Popen(p_args, **kwargs)
    ret = cmd.wait()
    if ret != 0:
        sys.exit(ret)
    return ret


def select_server(server, **kwargs):
    """
    Before the devpi CLI can do much of anything, it has to be pointed at the
    root of a devpi server.

    :param str server: Absolute URI to the root of a devpi server (not an
        index within the devpi server).
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return devpi('use', [
        '--always-set-cfg', 'yes',
        server],
        **kwargs)


def login(username, password, **kwargs):
    """
    Uploading packages to a devpi server usually requires an authenticated
    account with write permissions.

    :param str username: The devpi username we'll be uploading as.
    :param str password: The devpi user's password.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return devpi('login',
                 ['--password', password,
                  username],
                 **kwargs)


def select_index(index, **kwargs):
    """
    Before we can upload a package to an index, we must select it since there's
    no one-shot select + upload command.

    :param str index: The index to upload to. For example, ``root/devpitest``.
        This gets appended to whatever ``server`` value gets passed into
        :py:func:`select_server`.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return devpi('use', [index], **kwargs)


def create_index(index, **kwargs):
    """
    Creates an index on the devpi server.

    :param str index: The index to create. For example, ``root/devpitest``.
        This gets appended to whatever ``server`` value gets passed into
        :py:func:`select_server`.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return devpi('index', ['-c', index], **kwargs)


def upload_package(path, **kwargs):
    """
    Upload the package residing at ``path`` to the currently selected devpi
    server + index.

    :param str path: An absolute or relative path to the directory containing
        the package you'd like to upload.
    :param str clientdir: Path to a directory for the devpi CLI to store state.
    :rtype: subprocess.CompletedProcess
    """
    return devpi('upload',
                 ['--from-dir', '--no-vcs'],
                 cwd=path, **kwargs)


def check_vargs(vargs):
    """
    Check over the args passed in to make sure that we have everything we
    need to get the upload done. Exit with code 1 if the input is bad.

    :param dict vargs: Contents of the 'vargs' JSON array in the
        the plugin input.
    """
    server_uri = vargs.get('server', '')
    parsed = urllib.parse.urlsplit(server_uri)
    if not all([parsed.scheme, parsed.netloc]):
        print(
            "You must specify the full, absolute URI to your devpi server "
            "(including protocol).")
        sys.exit(1)
    index = vargs.get('index')
    if not index:
        print("You must specify an index on your devpi server to upload to.")
        sys.exit(1)
    username = vargs.get('username')
    if not username:
        print("You must specify a username to upload packages as.")
        sys.exit(1)
    password = vargs.get('password')
    if password is None:
        print("You must specify a password.")
        sys.exit(1)


def extract_vargs(payload):
    vargs = {}
    for k in payload:
        if 'DEVPI_' in k:
            vargs[k.replace('DEVPI_', '').lower()] = payload[k]
        if 'PLUGIN_' in k:
            vargs[k.replace('PLUGIN_', '').lower()] = payload[k]
    return vargs


def main():
    payload = os.environ
    vargs = extract_vargs(payload)
    check_vargs(vargs)

    select_server(vargs['server'])
    login(vargs['username'], vargs['password'])
    select_index(vargs['index'])
    package_path = os.getcwd()
    if VERBOSE:
        print("package path: {}".format(package_path))
    upload_package(package_path)


if __name__ == "__main__":
    main()
