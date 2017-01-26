# -*- coding: utf-8 -*-
#

from gitfaces.__about__ import (
        __author__,
        __email__,
        __copyright__,
        __license__,
        __version__,
        __maintainer__,
        __status__
        )

import datetime
import git
import hashlib
from io import BytesIO
import os
from PIL import Image
import requests
import time

# import pipdated
# if pipdated.needs_checking(__name__):
#     msg = pipdated.check(__name__, __version__)
#     if msg:
#         print(msg)

_GITHUB_API_URL = 'https://api.github.com'


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


def fetch(local_repo, out_dir):
    _fetch_gravatar(local_repo, out_dir)
    # _fetch_github(local_repo)
    return


def _fetch_gravatar(directory, out_dir):
    repo = git.Repo(directory)
    # get all author and full names emails from the log
    log_names_emails = repo.git.log('--format=%an;%ae').split('\n')
    names_emails = set([
        tuple(name_email.split(';')) for name_email in log_names_emails
        ])

    gravatar_url = 'https://www.gravatar.com'
    for name, email in names_emails:
        print('Check Gravatar for %s...' % email)
        gravatar_hash = hashlib.md5(email.strip().lower()).hexdigest()
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


def _fetch_github(github_repo, out_dir):

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
            print(user)

            print('User %s...' % user['login'])
            # get name and avatar_url
            r = requests.get(_GITHUB_API_URL + '/users/%s' % user['login'])
            user_data = r.json()
            try:
                name = user_data['name']
            except KeyError:
                continue
            if name is None:
                continue
            avatar_url = user_data['avatar_url']

            # get avatar
            r = requests.get(avatar_url)
            if not r.ok:
                raise RuntimeError(
                    'Failed request to %s (code: %s)'
                    % (avatar_url, r.status_code)
                    )
            # save the image as png
            i = Image.open(BytesIO(r.content))
            filename = os.path.join(out_dir, '%s.png' % name)
            print('    Saving %s...' % filename)
            i.save(filename)

        if len(data) < max_per_page:
            break
        k += 1

    return
