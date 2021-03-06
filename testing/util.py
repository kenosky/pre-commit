from __future__ import unicode_literals

import os
import os.path
import shutil

import jsonschema
import pytest

from pre_commit.util import cmd_output
from pre_commit.util import cwd


TESTING_DIR = os.path.abspath(os.path.dirname(__file__))


def get_resource_path(path):
    return os.path.join(TESTING_DIR, 'resources', path)


def copy_tree_to_path(src_dir, dest_dir):
    """Copies all of the things inside src_dir to an already existing dest_dir.

    This looks eerily similar to shutil.copytree, but copytree has no option
    for not creating dest_dir.
    """
    names = os.listdir(src_dir)

    for name in names:
        srcname = os.path.join(src_dir, name)
        destname = os.path.join(dest_dir, name)

        if os.path.isdir(srcname):
            shutil.copytree(srcname, destname)
        else:
            shutil.copy(srcname, destname)


def get_head_sha(dir):
    with cwd(dir):
        return cmd_output('git', 'rev-parse', 'HEAD')[1].strip()


def is_valid_according_to_schema(obj, schema):
    try:
        jsonschema.validate(obj, schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False


def skipif_slowtests_false(func):
    return pytest.mark.skipif(
        os.environ.get('slowtests') == 'false',
        reason='slowtests=false',
    )(func)
