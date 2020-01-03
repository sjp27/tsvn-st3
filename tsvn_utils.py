"""
Invoke useful TortoiseSVN GUI windows from Sublime Text

By Steve Pickford, https://github.com/tbd
"""

import os
import time
import sublime

import subprocess

svn_root_cache = {}
def svn_root(directory):
    """ This method lifted from https://github.com/kemayo/sublime-text-git """
    global svn_root_cache

    retval = False
    leaf_dir = directory

    if leaf_dir in svn_root_cache and svn_root_cache[leaf_dir]['expires'] > time.time():
        return svn_root_cache[leaf_dir]['retval']

    while directory:
        if os.path.exists(os.path.join(directory, '.svn')):
            retval = directory
            break
        parent = os.path.realpath(os.path.join(directory, os.path.pardir))
        if parent == directory:
            # /.. == /
            retval = False
            break
        directory = parent

    svn_root_cache[leaf_dir] = {
        'retval': retval,
        'expires': time.time() + 5
    }

    return retval

def is_svn_controlled(directory):
    return bool(svn_root(directory))

def run_tortoise_svn_command(command, args, path):
    settings = sublime.load_settings('TortoiseSVN Context.sublime-settings')
    tortoisesvn_path = settings.get('tortoisesvn_path')

    if tortoisesvn_path is None or not os.path.isfile(tortoisesvn_path):
        tortoisesvn_path = 'TortoiseProc.exe'

    cmd = u'{0} /command:"{1}" /path:"{2}" {3}'.format(
        tortoisesvn_path, 
        command,
        path, 
        u" ".join(args))

    try:
        print("Running {0}".format(cmd))
        with open(os.devnull, 'w') as devnull:
            proc = subprocess.Popen(cmd, 
                stdin=devnull, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                shell=False, 
                creationflags=subprocess.SW_HIDE)
    except IOError as ex:
        sublime.error_message("Failed to execute command: {}".format(
            str(ex)))
        raise
