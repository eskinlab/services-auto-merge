from config import CURRENT_STAGE, LOGS
from stages import Stage
from argparse import ArgumentParser
from distutils.util import strtobool
import logging
import sys


def args_parser():
    parser = ArgumentParser(description='Auto Merge')
    parser.add_argument('--system', '-s',
                        type=str, required=True,
                        default='gitlab',
                        choices=['gitlab', 'bitbucket'],
                        help='The version control system [gitlab; bitbucket]')
    parser.add_argument('--branch_from', '-f',
                        type=str, required=True,
                        help='The source branch')
    parser.add_argument('--branch_to', '-t',
                        type=str, required=True,
                        help='The destination branch')
    parser.add_argument('--up_gradle_version', '-ug',
                        type=strtobool, required=False,
                        default=False,
                        choices=(False, True),
                        help='Up versions of gradle.properties according to actual_version.ini')
    parser.add_argument('--rm_snapshot', '-r',
                        type=strtobool, required=False,
                        default=False,
                        choices=(False, True),
                        help='Remove -SNAPSHOT')
    parser.add_argument('--up_semantic_version', '-us',
                        type=strtobool, required=False,
                        default=False,
                        choices=(False, True),
                        help='Update version of semantic-build-versioning.gradle')
    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=LOGS["level"], format=LOGS["format"], stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.info("=== Start Auto-Merge ===")
    args = args_parser()
    s = Stage(CURRENT_STAGE, args, logger)
    s.run()
