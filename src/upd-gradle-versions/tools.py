from gitlab import Gitlab


# Get number of end of string
# ex. item = branch10 - return 10
def get_num_of_str(item):
    for index, letter in enumerate(item, 0):
        if letter.isdigit():
            return item[index:]


def read_gitlab_file(gitlab, item):
    gl = Gitlab(gitlab['url'], private_token=gitlab['token'])
    project = gl.projects.get(item['project'])
    f = project.files.raw(file_path=item['name'], ref=item['branch'])
    return f.decode()


def read_file(name, logger):
    try:
        with open(name, mode="r") as f:
            data = f.read()
    except FileNotFoundError:
        logger.error(f'No {name} file or directory')
    else:
        return data


def write_file(name, data, logger):
    with open(name, mode="w") as f:
        f.write(data)
    logger.info(f'File {f.name} is writen')
