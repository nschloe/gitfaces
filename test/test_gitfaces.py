import gitfaces
import os


def test_gitfaces():
    os.mkdir('out')
    gitfaces.fetch(
        # This is where travis puts the repo
        os.path.join(os.path.expanduser('~'), 'nschloe/gitfaces'),
        'out'
        )
    return
