import gitfaces
import os


def test_gitfaces():
    repo_dir = os.getenv('GITFACES_REPO')
    os.mkdir('out')
    # Don't check GitHub, their rate limits are too tight for frequent tests.
    gitfaces.fetch(repo_dir, 'out', github=False)
    return
