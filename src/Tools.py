import os

class Tools():

    def __init__(self):
        pass

    @classmethod
    def isAbsolute(self, normPath: str) -> bool:
        parts = normPath.split(os.sep)
        try:
            if os.path.ismount(parts[0]+os.sep):
                return True
        except FileNotFoundError:
            return False
        return False

    @classmethod
    def getFileNameWithoutExtension(self, filename: str) -> str:
        pointIndex = filename.rfind(".")
        if pointIndex != -1:
            return filename[:pointIndex]
        return filename

    @classmethod
    def makeFolder(self, path: str):
        dirName = os.path.dirname(path)
        print(dirName)
        if os.path.exists(dirName) is False:
            os.makedirs(dirName)
