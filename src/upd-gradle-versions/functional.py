# -*- coding: utf-8 -*-
from config import SNAPSHOT_PATTERN
from tools import get_num_of_str
from configparser import ConfigParser
from copy import deepcopy
from re import sub
from packaging import version


# Remove -SNAPSHOT from gradle.properties
def rm_snapshot(data, logger):
    logger.info(f'Remove {SNAPSHOT_PATTERN}')
    data_new = deepcopy(data)
    for line in data.split('\n'):
        new_line = sub(rf'(\d|\s)({SNAPSHOT_PATTERN})$', r'\1', line)
        data_new = data_new.replace(line, new_line)
    return data_new


def parse_vers_line(line):
    snap = ""
    [serv, ver] = [i.strip() for i in line.split("=")]
    if SNAPSHOT_PATTERN in ver:
        [ver, snap] = [i.strip() for i in ver.split("-")]
    return [serv, ver, snap]


# Parse data .ini format
def parse_source_data(data, branch, logger):
    release = get_num_of_str(branch)
    logger.info(f'Source section -> {release}')
    config = ConfigParser()
    config.read_string(data)
    try:
        res = config[release]
    except KeyError:
        logger.error(f'Sections {release} is not exist. Update actual_version.ini.')
        res = None
    return res


# data_to - updated data
# data_actual - data with actual versions
def up_version(data_to, data_actual, logger):
    data_new = deepcopy(data_to)
    for service_from in list(data_actual.keys()):
        for line_to in data_to.split('\n'):
            if str(service_from) in line_to:
                [service_to, version_to, snapshot] = parse_vers_line(line_to)
                version_actual = data_actual.get(service_from)
                if version_to != version_actual:
                    if version.parse(version_actual) > version.parse(version_to):
                        logger.info(f"Update {service_to} {version_to} -> {version_actual}")
                        new_line = f"{service_to}={version_actual}"
                        if snapshot:
                            logger.info(f'+ {SNAPSHOT_PATTERN}')
                            new_line = new_line + SNAPSHOT_PATTERN
                        data_new = data_new.replace(line_to, new_line)
    return data_new
