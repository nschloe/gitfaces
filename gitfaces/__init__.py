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

from io import BytesIO
import os
from PIL import Image
import requests

# import pipdated
# if pipdated.needs_checking(__name__):
#     msg = pipdated.check(__name__, __version__)
#     if msg:
#         print(msg)


def fetch(github_repo, out_dir):

    assert os.path.isdir(out_dir)

    github_api_url = 'https://api.github.com'
    endpoint = '/repos/%s/contributors' % github_repo
    # https://developer.github.com/v3/#pagination
    default_page_length = 30

    k = 1
    while True:
        params = {'page': k}
        r = requests.get(github_api_url + endpoint, params=params)
        if not r.ok:
            raise RuntimeError(
                'Failed request to %s (code: %s)' % (r.url, r.status_code)
                )
        data = r.json()

        for user in data:
            print('User %s...' % user['login'])
            # get name and avatar_url
            r = requests.get(github_api_url + '/users/%s' % user['login'])
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
        exit(1)

        if len(data) < default_page_length:
            break
        k += 1

    return
