"""Errors used in this application"""

class Error(Exception):
    """Base class for exceptions in this module"""
    def __init__(self, message):
        super(Error, self).__init__()
        self.message = message

class AuthError(Error):
    """Exception raised for authentication errors

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super(AuthError, self).__init__(message)

class FolderNotFoundError(Error):
    """Exception raised when folder does not exist

    Attributes:
        message -- explanation of the error,
        path -- the path
    """

    def __init__(self, path):
        super(FolderNotFoundError, self).__init__('Folder not found')
        self.path = path
