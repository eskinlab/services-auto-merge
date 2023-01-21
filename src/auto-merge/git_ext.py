from repo_ext import RepoExt
from git import Repo
import shutil


class GitExt(RepoExt):
    def __init__(self, logger, repo_cnf, git_cnf):
        super().__init__(logger, repo_cnf)
        self.user = str(git_cnf['user'])
        self.email = str(git_cnf['email'])
        self.repo = None
        self.conflict = False

    def clone(self, url, branch):
        self.logger.info(f'Clone project {self.repo_name}')
        try:
            self.repo = Repo.clone_from(url, self.repo_name, branch=branch)
        except Exception as e:
            print(e)
            self.logger.error(f'Error to clone repo {self.repo_name} {branch}')
            return False
        if not self.repo.bare:
            self.logger.info(f'Repo successfully loaded')
            return True
        else:
            self.logger.error(f'Repo unsuccessfully loaded')
            return False

    def config(self):
        with self.repo.config_writer() as config:
            config.set_value("user", "name", str({self.user}))
            config.set_value("user", "email", str({self.email}))
            config.set_value("merge", "ff", "no")
            config.set_value("core", "mergeoptions", "--no-ff")

    def get_ff_value(self):
        with self.repo.config_writer() as config:
            field = config.get_value("merge", "ff")
        print(field)

    def checkout(self, branch):
        try:
            self.repo.git.checkout(branch)
            self.logger.info(f'Checkout branch {branch}')
        except:
            self.repo.git.checkout('-b', branch)
            self.logger.info(f'Create branch {branch}. Current {self.repo.active_branch}')

    # Merge branch into current branch
    def merge(self, branch):
        self.logger.info(f'Merge {branch}')
        try:
            self.repo.git.merge(f'{branch}', no_ff=True)
        except Exception as e:
            self.logger.warn(f'Merge conflict {self.repo_name}')
            print(e)
            self.conflict = True

    def add_file(self, file):
        t = self.repo.head.commit.tree
        diff = self.repo.git.diff(t)
        if file in diff:
            self.repo.index.add(file)
            return True
        else:
            return False

    def commit(self, msg):
        self.logger.info(f'Commit: {msg}')
        print(self.repo.index.commit(msg, skip_hooks=True))

    # Show commits for current branch
    def show_commits(self, count):
        commits = self.repo.iter_commits(max_count=count)
        for commit in commits:
            print(commit.hexsha, commit.message)

    def push(self, branch):
        self.logger.info(f'Git Push branch {branch}')
        self.repo.git.push('origin', branch)

    def __del__(self):
        self.logger.info(f'Delete project {self.repo_name}')
        try:
            shutil.rmtree(self.repo_name, ignore_errors=True)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
