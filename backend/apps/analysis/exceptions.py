class RepositoryNotFound(Exception):
    pass


class ActiveAnalysisExists(Exception):

    def __init__(self, analysis_job):
        self.analysis_job = analysis_job