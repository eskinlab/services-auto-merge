from config import \
    SERVISES_FILE, UPDATE_FILE, SERVICES_TYPE, GIT, GITLAB, BITBUCKET
from gitlab_ext import GitlabExt
from bitbucket_ext import BitbucketExt
import json


class Stage:

    def __init__(self, stage, args, logger):
        self.stage = stage
        self.system = args.system
        self.branch_from = args.branch_from
        self.branch_to = args.branch_to
        self.up_gradle_version = args.up_gradle_version
        self.rm_snapshot = args.rm_snapshot
        self.up_semantic_version = args.up_semantic_version
        self.logger = logger
        self.logger.info(f'Parameters: stage={self.stage},'
                         f' branch_from={self.branch_from}, branch_to={self.branch_to},'
                         f' up_gradle_version={self.up_gradle_version}, rm_snapshot={self.rm_snapshot},'
                         f' up_semantic_version={self.up_semantic_version}')

    def __get_repos(self, file_cnf):
        """Read file, convert to json and get list of objects
        TODO:
        :return: list
        """
        self.logger.info(f'Get data from file {file_cnf["fileName"]}')
        repo = self.__connect_to_version_control(file_cnf)
        data = repo.read_file(file_cnf["fileName"], file_cnf["branch"])
        data = json.loads(data)
        return data[self.stage]

    def __actualize_branches(self, prj_data):
        self.branch_from = prj_data["branchFrom"]
        self.branch_to = prj_data["branchTo"]

    def __pre_merge_update(self, repo):
        staged = False
        if self.up_gradle_version or self.rm_snapshot:
            file_name = UPDATE_FILE['up_version_or_rm_snapshot']
            repo.update_gradle_properties(self.up_gradle_version, self.rm_snapshot, self.branch_to)
            staged += repo.add_file(file_name)
        if self.up_semantic_version:
            file_name = UPDATE_FILE['up_ui_version']
            if repo.update_semantic_version(file_name, self.branch_to):
                staged += repo.add_file(file_name)
            file_name = UPDATE_FILE['up_semantic_version']
            if repo.update_semantic_version(file_name, self.branch_to):
                staged += repo.add_file(file_name)
        if staged:
            repo.commit(GIT["commit_msg"])

    def __merge(self, repo):
        repo.merge(self.branch_from)
        if not repo.conflict:
            repo.push(self.branch_to)
        else:
            repo.create_mr(self.branch_from, self.branch_to)

    def __connect_to_version_control(self, repo_cnf):
        """Create remote version control system object
        TODO:
        :return: version control object
        """
        if self.system == "gitlab":
            repo = GitlabExt(self.logger, repo_cnf, GIT, GITLAB)
        elif self.system == "bitbucket":
            repo = BitbucketExt(self.logger, repo_cnf, GIT, BITBUCKET)
        return repo

    def run(self):
        self.logger.info(f'Run stage: {self.stage}')
        repos = self.__get_repos(SERVISES_FILE)
        for repo_cnf in repos:
            if self.stage in SERVICES_TYPE["branch-set"]:
                self.__actualize_branches(repo_cnf)
            repo = self.__connect_to_version_control(repo_cnf)
            repo.info(self.branch_from, self.branch_to)
            if self.stage in SERVICES_TYPE["mr-set"]:
                repo.create_mr(self.branch_from, self.branch_to)
            elif self.stage in SERVICES_TYPE["general"]:
                if repo.clone(repo.repo_url, self.branch_from):
                    repo.config()
                    repo.checkout(self.branch_to)
                    # --- Update files ---
                    self.__pre_merge_update(repo)
                    # --- Merge ---
                    self.__merge(repo)
            else:
                self.logger.error(f'Unknown stage: {self.stage} {repo.name}')
            del repo
