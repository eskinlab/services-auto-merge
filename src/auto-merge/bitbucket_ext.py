from atlassian import Bitbucket
import sys


class BitbucketExt:

    def __init__(self, logger, repo_cnf, git_cnf, bb_cnf):
        super().__init__(logger, repo_cnf, git_cnf)
        self.__protocol = bb_cnf['protocol']
        self.__user = bb_cnf['user']
        self.__password = bb_cnf['password']
        self.__url = bb_cnf['url']
        self.__automerge_title = bb_cnf["automerge_title"]

    @property
    def url(self):
        return f'{self.__protocol}://{self.__url}'

    @property
    def repo_url(self):
        return f"{self.__protocol}://{self.__user}:{self.__password}" \
               f"@{self.__url}{self.repo_group}/{self.repo_name}.git"

    def __connect_to_bitbucket(self):
        """Connect to bitbucket
        TODO: add desc for func

        :return: bitbucket
        """
        self.logger.info(f'Connect to {self.__url}')
        try:
            bitbucket = Bitbucket(
                self.url, #__url
                self.__user,
                self.__password,
                verify_ssl=False
            )
        except Exception as e:
            self.logger.error(f'bitbucket: {e}')
            sys.exit("Connect error")
        return bitbucket

    def read_file(self, file_name, file_branch="master"):
        bb = self.__connect_to_bitbucket()
        data = bb.get_content_of_file(self.repo_group, self.repo_name,
                                      file_name, at=None, markup=None)
        return data

    def create_mr(self, branch_from, branch_to):
        self.logger.info(f'Create MR and assignee to {self.repo_maintainer}')
        source_repo, dest_repo = self.repo_name, self.repo_name
        source_project, dest_project = self.repo_group, self.repo_group
        try:
            self.bb.open_pull_request(source_project, source_repo,\
                                    dest_project, dest_repo,\
                                    branch_from, branch_to,\
                                    f'{self.__automerge_title} {branch_from}->{branch_to}',\
                                    f'{self.__automerge_title}',\
                                    self.repo_maintainer)
        except BaseException as e:
            self.logger.error(f'Possible another MR is already exist for {self.repo_name}')
