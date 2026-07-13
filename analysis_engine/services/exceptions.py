class GitCommandFailed(Exception):

    def __init__(
        self,
        command: str,
        return_code: int,
        stderr: str,
    ):
        self.command = command
        self.return_code = return_code
        self.stderr = stderr.strip()

        super().__init__(self.__str__())

    def __str__(self) -> str:
        return (
            f"Git command '{self.command}' failed "
            f"(exit code {self.return_code}): "
            f"{self.stderr}"
        )


class InvalidRepositoryPath(Exception):
    pass


class DirtyRepositoryError(Exception):
    pass