import hashlib
from PySide.QtCore import QProcess, QIODevice, QFile, QByteArray, Qt, QCryptographicHash
from PySide.QtGui import QPixmap
from os import path

class FileAudio():
    """Represents the Audio Files. Contains all the metadata. This class is inherited by the Files Format Classes"""

    def __init__(self, metaInfo):
        """Constructor of the class. Initializes and sets all the components."""
        self.metadata = {}
        self.metadata["<path>"] = metaInfo["General"]["Complete name"]
        self.metadata["<title>"] = metaInfo["General"].get("Track name")
        self.metadata["<albumartist>"] = metaInfo["General"].get("Album/Performer")
        self.metadata["<artist>"] =  metaInfo["General"].get("Performer")
        self.metadata["<album>"] =  metaInfo["General"].get("Album")
        self.metadata["<tracknumber>"] = metaInfo["General"].get("Track name/Position")
        self.metadata["<tracktotal>"] = metaInfo["General"].get("Track name/Total")
        self.metadata["<discnumber>"] =  metaInfo["General"].get("Part/Position")
        self.metadata["<disctotal>"] = metaInfo["General"].get("Part/Total")
        self.metadata["<genre>"] = metaInfo["General"].get("Genre")
        self.metadata["<year>"] = metaInfo["General"].get("Recorded date")
        self.metadata["<comment>"] = metaInfo["General"].get("Comment")
        self.metadata["<bitrate>"] = metaInfo["Audio"].get("Bit rate")
        self.metadata["<bitratemode>"] = metaInfo["Audio"].get("Bit rate mode")
        self.metadata["<coverfile>"], self.metadata["<covermime>"] = self.getAlbumCover(metaInfo)
        self.metadata["<lyrics>"] = metaInfo["General"].get("Lyrics")
        self.metadata["<lenght>"] = metaInfo["Audio"].get("Duration")
        self.metadata["<filename>"] = path.basename(self.metadata["<path>"])

    def printTags(self):
        """Prints of all the available tags"""
        for key, value in self.metadata.items():
            try:
                print("{0}: {1}".format(key, value))
            except UnicodeEncodeError:
                print("Character error in tag {0}".format(key))

    def getAlbumCover(self, metaInfo):
        """If the file contains a cover, this method extract it and save it to a temporarily 
        location with its hash code as the file name.
        Returns a tuple containing the filename of the cover art, and MIME type of the cover"""
        if "Cover" in metaInfo["General"] and metaInfo["General"]["Cover"] == "Yes":
            coverFormat = metaInfo["General"].get("Cover MIME")
            process = QProcess()
            process.start("resources/tools/mediainfo.exe", ["--Inform=file://resources/tools/art.txt", self.metadata["<path>"]])
            process.waitForFinished()
            if process.canReadLine():
                cad = process.readLine()
                byte = QByteArray.fromBase64(cad)
                name = self.getSHA1FromBytes(byte)
                if coverFormat == "image/jpeg":
                    name += ".jpg"
                elif coverFormat == "image/png":
                    name += ".png"
                elif coverFormat == "image/gif":
                    name += ".gif"
                f = QFile(name)
                f.open(QIODevice.WriteOnly)
                f.write(byte)
                f.close()
                return name, coverFormat
        return None, None

    def getTagsValue(self, stringText):
        """Given the string 'stringText' returns the values of the tags presented in the string"""
        st = stringText[:]
        for tag, value in self.metadata.items():
            if value is None:
                st = st.replace("/"+str(tag), "")
                st = st.replace(str(tag), "")
            else:
                st = st.replace(tag, value)

        return st

    def getCoverWithInfo(self):
        """Returns tuple containing a QPixmap with the cover of the file and de details about it"""
        if self.metadata["<coverfile>"] is not None:
            pixmap = QPixmap(self.metadata["<coverfile>"])
            detail = "{0}x{1}".format(pixmap.width(), pixmap.height())
            if self.metadata["<covermime>"] is not None:
                detail += "   {0}".format(self.metadata["<covermime>"])
            detail += "   {:.1f} KB".format(path.getsize(self.metadata["<coverfile>"])/1024)
            return (pixmap, detail)
        return None, "No cover available"

    def getMD5FromFile(self, fileName):
        """This method is not currently working. Please use Carefuly.
        Given the file name, returns a cryptographic hash SHA1 from the file"""
        f = QFile(fileName)
        f.open(QIODevice.ReadOnly)
        byte = f.readAll()
        f.close()
        return getSHA1FromBytes(byte)

    def getSHA1FromBytes(self, data):
        """Given the data bytes, returns a Cryptographic Hash SHA1 of the data"""
        hash_sha1 = QCryptographicHash(QCryptographicHash.Sha1)
        hash_sha1.addData(data)
        return str(QByteArray.toHex(hash_sha1.result()))
