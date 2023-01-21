#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import GRADLE_FILE, SOURCE_FILE, GITLAB, LOGS
from tools import read_file, write_file, read_gitlab_file
from functional import parse_source_data, rm_snapshot, up_version
from argparse import ArgumentParser
from copy import deepcopy
import logging


def args_parser():
    parser = ArgumentParser(description=
                            'Update versions and cut -SNAPSHOT in gradle.properties')
    parser.add_argument('--prj_path', '-p',
                        type=str, required=True,
                        help='Path to the project where gradle.properties is located')
    parser.add_argument('--branch_to', '-b',
                        type=str, required=True,
                        help='This is destination branch')
    parser.add_argument('--up_version', '-u',
                        type=str, default='False',
                        required=True,
                        choices=['False', 'True'],
                        help='Up versions of gradle.properties according to actual_version.ini')
    parser.add_argument('--rm_snapshot', '-r',
                        type=str, default='False',
                        required=True,
                        choices=['False', 'True'],
                        help='Remove -SNAPSHOT')
    return parser.parse_args()


def run(prj_path, branch, up_versions, remove_snapshot, logger):
    logger.info(f'Start update {GRADLE_FILE}')
    gradle_file = f'{prj_path}/{GRADLE_FILE}'
    data = read_file(gradle_file, logger)
    if data:
        initial_data = deepcopy(data)
        if remove_snapshot == 'True':
            data = rm_snapshot(data, logger)
        if up_versions == 'True':
            source_data = read_gitlab_file(GITLAB, SOURCE_FILE)
            source_data = parse_source_data(source_data, branch, logger)
            if source_data:
                data = up_version(data, source_data, logger)
        if data != initial_data:
            write_file(gradle_file, data, logger)


if __name__ == '__main__':
    args = args_parser()
    logging.basicConfig(level=LOGS["level"], format=LOGS["format"])
    logger = logging.getLogger(__name__)
    run(args.prj_path, args.branch_to, args.up_version, args.rm_snapshot, logger)
