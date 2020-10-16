from typing import TextIO


class Reader():
    """
    Wraps a file opened for reading to provide read_until method
    """

    def __init__(self, file: TextIO) -> None:
        """
        Wrap file, file should be read-only, file should not be read through any other means
        """
        if not file.readable():
            raise ValueError("Attempt to wrap a non-readable file")
        if file.writable():
            raise ValueError("Attempt to wrap a non-read-only file")
        self.file = file
        self.buf = ""

    def read_until(self, char: str) -> str:
        """
        Returns a string from the current position up to and including char
        """
        result, sep, self.buf = self.buf.partition(char)
        if sep:
            return result + sep
        else:
            while True:
                chunk, sep, self.buf = self.file.readline().partition(char)
                if not chunk:
                    return result
                result += chunk + sep
                if sep:
                    return result
