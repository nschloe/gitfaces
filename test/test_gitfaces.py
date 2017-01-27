import gitfaces
import os


def test_gitfaces():
    repo_dir = os.getenv('GITFACES_REPO')
    print('repo_dir', repo_dir)
    os.mkdir('out')
    gitfaces.fetch(repo_dir, 'out')
    return
