from config import LOGS
from semantic import Semantic
from argparse import ArgumentParser
import logging


def args_parser():
    parser = ArgumentParser(description=
                            'Update version in semantic-build-versioning.gradle')
    parser.add_argument('--file', '-f',
                        type=str, required=True,
                        help='Semantic file full path')
    parser.add_argument('--branch_to', '-b',
                        type=str, required=True,
                        help='This is destination branch')
    return parser.parse_args()


# Get number of end of string
# ex. return 10 if branch10
def get_num_of_str(item):
    for index, letter in enumerate(item, 0):
        if letter.isdigit():
            return item[index:]


def main():
    logging.basicConfig(level=LOGS["level"], format=LOGS["format"])
    logger = logging.getLogger(__name__)
    logger.info(f"-- Start Update --")
    args = args_parser()
    release = get_num_of_str(args.branch_to)
    logger.info(f"Update {args.file} to version {release}")
    s = Semantic(logger, args.file)
    s.upd_version(release)
    logger.info(f"-- End Update --")


if __name__ == "__main__":
    main()
