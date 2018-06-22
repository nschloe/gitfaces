# -*- coding: utf-8 -*-
#
import argparse

import gitfaces


def _get_parser():
    parser = argparse.ArgumentParser(
        description="fetch contributor avatars for a GitHub repository"
    )
    parser.add_argument("repo", type=str, help="local Git repository")
    parser.add_argument("outdir", type=str, help="output directory")
    return parser


def main(argv=None):
    parser = _get_parser()
    args = parser.parse_args(argv)
    gitfaces.fetch(args.repo, args.outdir)
    return
