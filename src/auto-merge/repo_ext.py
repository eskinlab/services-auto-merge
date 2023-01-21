from config import CURRENT_DIR, PYTHON
import subprocess
import os


class RepoExt:

    def __init__(self, logger, repo_cnf):
        self.logger = logger
        self.repo_name = repo_cnf["serviceName"]
        self.repo_group = repo_cnf["serviceGroup"]
        try:
            self.repo_maintainer = repo_cnf["repoMaintainer"]
            self.telegram_maintainer = repo_cnf["telegramMaintainer"]
        except Exception:
            pass
        self.repo_path = os.path.join(CURRENT_DIR, self.repo_name)

    def info(self, branch_from, branch_to):
        self.logger.info('--------------------------------')
        self.logger.info(f'{self.repo_name} {branch_from} -> {branch_to}')

    def update_gradle_properties(self, up_version, rm_snapshot, branch_to):
        cmd = f"{PYTHON} {CURRENT_DIR}/src/upd-gradle-versions/main.py" \
              f" --prj_path={self.repo_path}" \
              f" --branch_to={branch_to}" \
              f" --up_version={up_version}" \
              f" --rm_snapshot={rm_snapshot}"
        subprocess.getoutput(cmd)

    def update_semantic_version(self, file, branch_to):
        file = os.path.join(self.repo_path, file)
        if os.path.isfile(file):
            self.logger.info(f'Run Up Version for {file}')
            cmd = f"{PYTHON} {CURRENT_DIR}/src/upd-semantic-version/main.py" \
                  f" --file={file}" \
                  f" --branch_to={branch_to}"
            print(subprocess.getoutput(cmd))
            return True
        else:
            self.logger.info(f'File {file} is not exist')
            return False
