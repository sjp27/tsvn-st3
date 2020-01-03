"""
Invoke useful TortoiseSVN GUI windows from Sublime Text

Steve Pickford, https://github.com/tbd
"""


import os
import time
import sublime, sublime_plugin

try:
    from .tsvn_utils import *
except ValueError:
    # We get `ValueError: Attempted relative import in non-package` in ST2.
    from tsvn_utils import *


class TortoiseSvnCommandBase(sublime_plugin.WindowCommand):
    def is_enabled(self):
        return is_svn_controlled(self._relevant_path())

    def _active_line_number(self):

        view = self.window.active_view()
        if view:
            (row,col) = view.rowcol(view.sel()[0].begin())
            return row
        else:
            return None

    def _active_file_path(self):
        view = self.window.active_view()
        if view and view.file_name() and len(view.file_name()) > 0:
            return view.file_name()

    def _active_repo_path(self):
        path = self._active_file_path()
        if not path:
            path = self.window.project_file_name()
        if not path:
            path = self.window.folders()[0]
        if path is None:
            return

        root = svn_root(path)

        if root is False:
            return
        else:
            return root

    def _active_file_or_repo_path(self):
        path = self._active_file_path()
        if path is not None:
            return path

        # If no active file, then guess the repo.
        return self._active_repo_path()

    def _selected_dir(self, dirs):
        if len(dirs):
            return dirs[0]
        else:
            return

    def _execute_command(self, command, path=None):
        args = []

        line_number = self._active_line_number()
        if line_number:
            args.append("/line:{}".format(line_number))

        if path is None:
            run_tortoise_svn_command(command, args, self._relevant_path())
        else:
            run_tortoise_svn_command(command, args, path)


class TsvnLogCommand(TortoiseSvnCommandBase):
    def run(self, edit=None, dirs=[]):
        self._execute_command('log', self._selected_dir(dirs))
    
    def _relevant_path(self):
        return self._active_file_or_repo_path()


class TsvnDiffCommand(TortoiseSvnCommandBase):
    def run(self, edit=None, dirs=[]):
        self._execute_command('diff', self._selected_dir(dirs))

    def _relevant_path(self):
        return self._active_file_or_repo_path()


class TsvnCommitCommand(TortoiseSvnCommandBase):
    def run(self, edit=None, dirs=[]):
        self._execute_command('commit', self._selected_dir(dirs))

    def _relevant_path(self):
        return self._active_file_or_repo_path()


class TsvnCommitRepoCommand(TortoiseSvnCommandBase):
    def run(self, edit=None):
        self._execute_command('commit')

    def _relevant_path(self):
        return self._active_repo_path()


class TsvnStatusCommand(TortoiseSvnCommandBase):
    def run(self, edit=None, dirs=[]):
        self._execute_command('repostatus', self._selected_dir(dirs))

    def _relevant_path(self):
        return self._active_file_or_repo_path()


class TsvnSyncCommand(TortoiseSvnCommandBase):
    def run(self, edit=None):
        self._execute_command('sync')

    def _relevant_path(self):
        return self._active_repo_path()


class TsvnBlameCommand(TortoiseSvnCommandBase):
    def run(self, edit=None):
        self._execute_command('blame')

    def _relevant_path(self):
        return self._active_file_path()

class TsvnAddCommand(TortoiseSvnCommandBase):
    def run(self, edit=None, dirs=[]):
        self._execute_command('add', self._selected_dir(dirs))

    def _relevant_path(self):
        return self._active_file_or_repo_path()

class TsvnRevertCommand(TortoiseSvnCommandBase):
    def run(self, edit=None, dirs=[]):
        self._execute_command('revert', self._selected_dir(dirs))

    def _relevant_path(self):
        return self._active_file_or_repo_path()
