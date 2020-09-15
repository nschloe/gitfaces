import datetime
import hashlib
import os
import re
import time
from io import BytesIO

import git
import requests
from PIL import Image

_GITHUB_API_URL = "https://api.github.com"


def fetch(local_repo, out_dir, gravatar=True, github=True):
    repo = git.Repo(local_repo)

    # get all author and full names emails from the log
    log_names_emails = repo.git.log("--format=%an;%ae").split("\n")
    names_emails = {tuple(name_email.split(";")) for name_email in log_names_emails}

    # check for gravatar
    if gravatar:
        _fetch_gravatar(names_emails, out_dir)

    # check for github avatar
    if github:
        gh_repo = _get_github_repo(repo.remote("origin"))
        if gh_repo is not None:
            git_names = {name_email[0] for name_email in names_emails}
            _fetch_github(git_names, gh_repo, out_dir)
    return


def _wait_for_rate_limit(resource="core"):
    while True:
        r = requests.get(_GITHUB_API_URL + "/rate_limit")
        if not r.ok:
            raise RuntimeError(f"Failed request to {r.url} (code: {r.status_code})")
        data = r.json()

        if data["resources"][resource]["remaining"] > 0:
            break

        reset_time = datetime.datetime.fromtimestamp(
            data["resources"][resource]["reset"]
        )
        diff = reset_time - datetime.datetime.now()
        print(f"GitHub rate limit reached! (reset at {reset_time}). Waiting...")
        time.sleep(diff.total_seconds())


def _get_github_repo(remote):
    # git@github.com:trilinos/Trilinos.git
    # https://github.com/trilinos/Trilinos.git
    pattern = "github\\.com.([^\\.]*)\\.git"
    for url in remote.urls:
        res = re.search(pattern, url)
        try:
            return res.group(1)
        except (IndexError, AttributeError):
            pass
    return None


def _fetch_gravatar(names_emails, out_dir):
    gravatar_url = "https://www.gravatar.com"
    for name, email in names_emails:
        print(f"Check Gravatar for {email}...")

        email_str = email.strip().lower()
        try:
            gravatar_hash = hashlib.md5(email_str).hexdigest()
        except TypeError:
            # TypeError: Unicode-objects must be encoded before hashing
            gravatar_hash = hashlib.md5(str(email_str).encode("utf-8")).hexdigest()

        url = gravatar_url + "/avatar/" + gravatar_hash
        # get gravatar
        # fail if no gravatar is found
        params = {"d": 404, "size": 200}
        r = requests.get(url, params=params)
        if r.ok:
            # save the image as png
            i = Image.open(BytesIO(r.content))
            filename = os.path.join(out_dir, f"{name}.png")
            print(f"    Saving {filename}...")
            i.save(filename)
    return


def _fetch_github(git_names, github_repo, out_dir):
    assert os.path.isdir(out_dir)

    endpoint = f"/repos/{github_repo}/contributors"
    # https://developer.github.com/v3/#pagination
    max_per_page = 100

    k = 1
    while True:
        _wait_for_rate_limit()

        params = {"page": k, "per_page": max_per_page}
        r = requests.get(_GITHUB_API_URL + endpoint, params=params)
        if not r.ok:
            raise RuntimeError(f"Failed request to {r.url} (code: {r.status_code})")
        data = r.json()

        for user in data:
            avatar_url = user["avatar_url"]
            login = user["login"]
            print(f"GitHub user {login}...")
            # get name
            r = requests.get(_GITHUB_API_URL + f"/users/{login}")
            user_data = r.json()
            try:
                name = user_data["name"]
            except KeyError:
                name = None

            if name is None:
                continue
            if name not in git_names:
                print(f"    Name '{name}' does not appear in Git log. Skip.")
                continue

            filename = os.path.join(out_dir, f"{name}.png")
            if os.path.exists(filename):
                print(f"    File {filename} already exists.")
            else:
                # get avatar
                r = requests.get(avatar_url)
                if not r.ok:
                    raise RuntimeError(
                        f"Failed request to {avatar_url} (code: {r.status_code})"
                    )
                # save the image as png
                i = Image.open(BytesIO(r.content))
                print(f"    Saving {filename}...")
                i.save(filename)

        if len(data) < max_per_page:
            break
        k += 1
