# -*- coding: utf-8 -*-
#
import os
import shutil
import tempfile

import gitfaces


def test_gitfaces():
    repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    temp_dir = tempfile.mkdtemp()
    # Don't check GitHub, their rate limits are too tight for frequent tests.
    gitfaces.fetch(repo_dir, temp_dir, github=False)
    shutil.rmtree(temp_dir)
    return


def test_cli():
    repo_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    temp_dir = tempfile.mkdtemp()
    gitfaces.cli.main([repo_dir, temp_dir])
    shutil.rmtree(temp_dir)
    return
