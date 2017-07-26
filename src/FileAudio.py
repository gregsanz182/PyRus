from PySide.QtCore import QProcess, QIODevice, QFile, QByteArray, Qt, QCryptographicHash
from PySide.QtGui import QPixmap
from os import path
import hashlib

class FileAudio():

    def __init__(self, metaInfo):
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
        for key, value in self.metadata.items():
            print("{0}: {1}".format(key, value))

    def getAlbumCover(self, metaInfo):
        if "Cover" in metaInfo["General"] and metaInfo["General"]["Cover"] == "Yes":
            coverFormat = metaInfo["General"].get("Cover MIME")
            process = QProcess()
            process.start("resources/tools/mediainfo.exe", ["--Inform=file://resources/tools/art.txt", self.metadata["<path>"]])
            process.waitForFinished();
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
        st = stringText[:]
        for tag, value in self.metadata.items():
            st = st.replace(tag, value)

        return st

    def getCoverWithInfo(self):
        if self.metadata["<coverfile>"] is not None:
            pixmap = QPixmap(self.metadata["<coverfile>"])
            detail = "{0}x{1}".format(pixmap.width(), pixmap.height())
            if self.metadata["<covermime>"] is not None:
                detail += "   {0}".format(self.metadata["<covermime>"])
            detail += "   {:.1f} KB".format(path.getsize(self.metadata["<coverfile>"])/1024)
            return (pixmap, detail)
        return None, "No cover available"

    def getMD5FromFile(self, fileName):
        f = QFile(fileName)
        f.open(QIODevice.ReadOnly)
        byte = f.readAll()
        f.close()
        return getSHA1FromBytes(byte)

    def getSHA1FromBytes(self, data):
        hash_sha1 = QCryptographicHash(QCryptographicHash.Sha1)
        hash_sha1.addData(data)
        return str(QByteArray.toHex(hash_sha1.result()))
