from config import PATTERN
from copy import deepcopy
import re


def read_data(logger, file):
    data = None
    try:
        with open(file, mode="r") as f:
            data = f.readlines()
    except IOError:
        logger.warn(f'File {file} is not found')
    return data


def write_data(file, data):
    with open(file, mode="w") as f:
        f.writelines(data)


class Semantic:

    def __init__(self, logger, file):
        self.logger = logger
        self.file = file

    def __upd_data(self, data, release):
        new_data = deepcopy(data)
        new_line = None
        for line in data:
            double_digits = re.findall(r'[1-9][0-9]', line)
            if double_digits:
                version = double_digits[0]
                # Can we move to earlier version ?
                if release > version and (PATTERN[0] or PATTERN[1] in line):
                    new_line = re.sub(version, release, line)
                    if new_line is not line:
                        self.logger.info(f'Update [{line.rstrip()}] -> [{new_line.rstrip()}]')
                        new_data = list(map(lambda item: item.replace(line, new_line), new_data))
        if not new_line:
            self.logger.info(f'Current version {version}')
        return new_data

    def upd_version(self, release):
        data = read_data(self.logger, self.file)
        if data:
            new_data = self.__upd_data(data, release)
            if new_data != data:
                write_data(self.file, new_data)
            else:
                self.logger.info(f'File is up-to-date')
