# -*- coding: utf-8 -*-
#
from __future__ import print_function

import datetime
import hashlib
from io import BytesIO
import os
import re
import time

from gitfaces.__about__ import (
    __author__,
    __email__,
    __copyright__,
    __license__,
    __version__,
    __maintainer__,
    __status__
    )

import git
from PIL import Image
import requests

import pipdated
if pipdated.needs_checking(__name__):
    msg = pipdated.check(__name__, __version__)
    if msg:
        print(msg)

_GITHUB_API_URL = 'https://api.github.com'


def fetch(local_repo, out_dir, gravatar=True, github=True):
    repo = git.Repo(local_repo)

    # get all author and full names emails from the log
    log_names_emails = repo.git.log('--format=%an;%ae').split('\n')
    names_emails = set([
        tuple(name_email.split(';')) for name_email in log_names_emails
        ])

    # check for gravatar
    if gravatar:
        _fetch_gravatar(names_emails, out_dir)

    # check for github avatar
    if github:
        gh_repo = _get_github_repo(repo.remote('origin'))
        if gh_repo is not None:
            git_names = set([name_email[0] for name_email in names_emails])
            _fetch_github(git_names, gh_repo, out_dir)
    return


def _wait_for_rate_limit(resource='core'):
    while True:
        r = requests.get(_GITHUB_API_URL + '/rate_limit')
        if not r.ok:
            raise RuntimeError(
                'Failed request to %s (code: %s)' % (r.url, r.status_code)
                )
        data = r.json()

        if data['resources'][resource]['remaining'] > 0:
            break

        reset_time = datetime.datetime.fromtimestamp(
            data['resources'][resource]['reset']
            )
        diff = reset_time - datetime.datetime.now()
        print(
            'GitHub rate limit reached! (reset at %s). Waiting...' % reset_time
            )
        time.sleep(diff.total_seconds())
    return


def _get_github_repo(remote):
    # git@github.com:trilinos/Trilinos.git
    # https://github.com/trilinos/Trilinos.git
    pattern = 'github\\.com.([^\\.]*)\\.git'
    for url in remote.urls:
        res = re.search(pattern, url)
        try:
            return res.group(1)
        except (IndexError, AttributeError):
            pass
    return None


def _fetch_gravatar(names_emails, out_dir):
    gravatar_url = 'https://www.gravatar.com'
    for name, email in names_emails:
        print('Check Gravatar for %s...' % email)

        email_str = email.strip().lower()
        try:
            gravatar_hash = hashlib.md5(email_str).hexdigest()
        except TypeError:
            # TypeError: Unicode-objects must be encoded before hashing
            gravatar_hash = hashlib.md5(
                str(email_str).encode('utf-8')
                ).hexdigest()

        url = gravatar_url + '/avatar/' + gravatar_hash
        # get gravatar
        # fail if no gravatar is found
        params = {'d': 404, 'size': 200}
        r = requests.get(url, params=params)
        if r.ok:
            # save the image as png
            i = Image.open(BytesIO(r.content))
            filename = os.path.join(out_dir, '%s.png' % name)
            print('    Saving %s...' % filename)
            i.save(filename)
    return


def _fetch_github(git_names, github_repo, out_dir):
    assert os.path.isdir(out_dir)

    endpoint = '/repos/%s/contributors' % github_repo
    # https://developer.github.com/v3/#pagination
    max_per_page = 100

    k = 1
    while True:
        _wait_for_rate_limit()

        params = {'page': k, 'per_page': max_per_page}
        r = requests.get(_GITHUB_API_URL + endpoint, params=params)
        if not r.ok:
            raise RuntimeError(
                'Failed request to %s (code: %s)' % (r.url, r.status_code)
                )
        data = r.json()

        for user in data:
            avatar_url = user['avatar_url']

            print('GitHub user %s...' % user['login'])
            # get name
            r = requests.get(_GITHUB_API_URL + '/users/%s' % user['login'])
            user_data = r.json()
            try:
                name = user_data['name']
            except KeyError:
                name = None

            if name is None:
                continue
            if name not in git_names:
                print(
                    '    Name \'%s\' does not appear in Git log. Skip.' % name
                    )
                continue

            filename = os.path.join(out_dir, '%s.png' % name)
            if os.path.exists(filename):
                print('    File %s already exists.' % filename)
            else:
                # get avatar
                r = requests.get(avatar_url)
                if not r.ok:
                    raise RuntimeError(
                        'Failed request to %s (code: %s)'
                        % (avatar_url, r.status_code)
                        )
                # save the image as png
                i = Image.open(BytesIO(r.content))
                print('    Saving %s...' % filename)
                i.save(filename)

        if len(data) < max_per_page:
            break
        k += 1

    return
