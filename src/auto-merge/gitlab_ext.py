from gitlab import Gitlab
from git_ext import GitExt


class GitlabExt(GitExt):
    def __init__(self, logger, repo_cnf, git_cnf, gl_cnf):
        super().__init__(logger, repo_cnf, git_cnf)
        self.__protocol = gl_cnf['protocol']
        self.__token = gl_cnf['token']
        self.__url = gl_cnf['url']
        self.__automerge_title = gl_cnf["automerge_title"]

    @property
    def url(self):
        return f'{self.__protocol}://{self.__url}'

    @property
    def repo_url(self):
        return f"{self.__protocol}://oauth2:{self.__token}@" \
                f"{self.__url}/{self.repo_group}/{self.repo_name}.git"

    def read_file(self, file_name, file_branch="master"):
        repo = self.get_project(f'{self.repo_group}/{self.repo_name}')
        f = repo.files.raw(file_path=file_name, ref=file_branch)
        return f.decode()

    def get_project(self, name):
        gl = Gitlab(self.url, private_token=self.__token)
        return gl.projects.get(name)

    def get_user_id(self, user):
        gl = Gitlab(self.url, private_token=self.__token)
        try:
            user = gl.users.list(username=user)[0]
        except IndexError:
            return None
        return user.id

    def create_mr(self, branch_from, branch_to):
        self.logger.info(f'Create gitlab MR and assignee to {self.repo_maintainer}')
        prj_path = f"{self.repo_group}/{self.repo_name}"
        prj = self.get_project(prj_path)
        maintainer_id = self.get_user_id(self.repo_maintainer)
        try:
            prj.mergerequests.create({
                'source_branch': branch_from,
                'target_branch': branch_to,
                'title': f'{self.__automerge_title} {branch_from}->{branch_to}',
                'assignee_id': maintainer_id
            })
        except:
            self.logger.error(f'Another MR is already exist for {self.repo_name}')
