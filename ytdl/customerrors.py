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

class DirectoryNotFoundError(Error):
    """Exception raised when directory does not exist

    Attributes:
        message -- explanation of the error,
        path -- the path
    """

    def __init__(self, path):
        super(DirectoryNotFoundError, self).__init__('Directory not found')
        self.path = path

class FileNotFoundError(Error):
    """Exception raised when File does not exist

    Attributes:
        message -- explanation of the error,
        path -- the path
    """

    def __init__(self, path):
        super(FileNotFoundError, self).__init__('File not found')
        self.path = path

class InvalidConfig(Error):
    "Exception raised when config is invalid"

    def __init__(self, path):
        super(InvalidConfig, self).__init__('Invalid config')
        self.path = path
