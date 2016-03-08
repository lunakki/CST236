"""
Provides utilities to get information on files
"""
import logging
import subprocess
import os
from functools import wraps

GIT_LOGGER = logging.getLogger(__name__)


def check_valid_path(func):
    """Make sure the path is valid"""
    @wraps(func)
    def path_checker(path, *args, **kwargs):
        """Make sure the path is valid"""
        if not os.path.exists(path):
            raise Exception('Path {0} does not exist cannot get git file '
                            'info'.format(path))
        return func(path, *args, **kwargs)
    return path_checker


def is_file_in_repo(path):
    """Check if a file is in the repo"""
    # File must exist to be in the repo
    if not os.path.exists(path):
        GIT_LOGGER.debug('%s does not exist therefore not in repo', path)
        return 'No'
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    test_repo = os.path.dirname(path)
    print path
    print test_repo
    if(path in get_diff_files(test_repo) or
       path in get_untracked_files(test_repo)):
        GIT_LOGGER.debug('%s changed or is untracked in repo %s', path, test_repo)
        return 'No'
    return 'Yes'


@check_valid_path
def get_git_file_info(path):
    """
    Get file revision for the file in path

    :param path: path to the file
    :type path: str

    :returns: script filename, SHA1 hash, date, and author of last time path was modified
    :rtype: tuple
    """
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    test_repo = os.path.dirname(path)
    if path in get_diff_files(test_repo):
        GIT_LOGGER.warning('%s is modified locally', path)
        return '{} has been modified locally'.format(os.path.basename(path))
    elif path in get_untracked_files(test_repo):
        GIT_LOGGER.warning('%s is not checked in', path)
        return '{} has been not been checked in'.format(os.path.basename(path))
    elif is_repo_dirty(test_repo, include_untracked=True):
        GIT_LOGGER.warning('%s is contained in a dirty repo', path)
        return '{} is a dirty repo'.format(os.path.basename(path))

    return '{} is up to date'.format(os.path.basename(path))



@check_valid_path
def is_repo_dirty(path, include_untracked=False):
    """
    Determine if the given repo is dirty

    :param path: path to check
    :type path: str

    :param include_untracked: include untracked files in determination
    :type include_untracked: bool

    :return: True if dirty, False otherwise
    :rtype: bool
    """
    if has_diff_files(path=path) or (include_untracked and has_untracked_files(path)):
        return True

    return False


@check_valid_path
def has_diff_files(path):
    """
    Check for modified files

    :param path: path to the repo to check
    :type path: str

    :return: True if diff files exist
    :rtype: bool
    """
    if len(get_diff_files(path=path)) > 0:
        return True

    return False


@check_valid_path
def has_untracked_files(path):
    """
    Check for untracked files

    :param path: path to the repo to check
    :type path: str

    :return: True if untracked files exist
    :rtype: bool
    """
    if len(get_untracked_files(path=path)) > 0:
        return True

    return False


@check_valid_path
def get_file_info(path):
    """
    Get the last commit information for the file specified

    :param path: path to the file to check
    :type path: str

    :return: file info string
    :rtype: str
    """
    out_format = '--pretty=format:"%H,%cd,%an"'

    file_info = git_execute(['git', 'log', '-1', out_format, path], os.path.dirname(path))

    return file_info.strip('\'"')


@check_valid_path
def get_diff_files(path, include_staged=True):
    """
    Return a list of all modified files

    :param path: path to check
    :type path: str

    :return: list of files
    :rtype: list
    """
    file_list = []

    # Check for non committed diffs
    files = git_execute(['git', 'diff', '--name-only'], path)
    for filename in files.split('\n'):

        if filename != '':
            file_list.append(os.path.normpath(os.path.join(get_repo_root(path),
                                                           filename)))
    if include_staged:
        # Check for non committed staged files
        files = git_execute(['git', 'diff', '--cached', '--name-only'], path)

        for filename in files.split('\n'):
            if filename != '':
                file_list.append(os.path.normpath(os.path.join(get_repo_root(path),
                                                               filename)))

    return file_list


@check_valid_path
def get_untracked_files(path):
    """
    Return a list of all untracked files

    :param path: path to check
    :type path: str

    :return: list of files
    :rtype: list
    """
    file_list = []

    files = git_execute(['git', 'ls-files', '.', '--exclude-standard', '--others',
                         '--full-name'], path)

    for filename in files.split('\n'):
        if filename != '':
            file_list.append(os.path.normpath(os.path.join(get_repo_root(path), filename)))

    return file_list


@check_valid_path
def get_repo_root(path):
    """
    Determine the root of a repo

    :param path: path to a folder/file in the repo
    :type path: str

    :return: full path to the repo root
    :rtype: str
    """
    if os.path.isfile(path):
        path = os.path.dirname(path)

    return os.path.normpath(git_execute(['git', 'rev-parse', '--show-toplevel'], path))


@check_valid_path
def get_repo_branch(path):
    """
    Determine the current branch of the repo

    :param path: Path to repo
    :type path: str

    :return: Branch Name
    :rtype: str
    """
    if os.path.isfile(path):
        path = os.path.dirname(path)

    return git_execute(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], path)


@check_valid_path
def get_repo_url(path):
    """
    Determine the url of the repo

    :param path: Path to repo
    :type path: str
    :return: Branch Name
    :rtype: str
    """
    if os.path.isfile(path):
        path = os.path.dirname(path)

    return git_execute(['git', 'config', '--get', 'remote.origin.url'], path)


def git_execute(params=None, path=os.getcwd()):
    """
    Execute a git command

    :param params: list of parameters to execute git with
    :type params: list

    :param path: path to execute git command from
    :type path: str

    :return: The stdout from git
    :rtype: str
    """
    pop = subprocess.Popen(params,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, cwd=path,
                           universal_newlines=True)

    stdout, stderr = pop.communicate()
    if stderr:
        GIT_LOGGER.error('Error occurred when executing git command(%s): %s', params,
                         stderr.strip())
    return stdout.strip()

