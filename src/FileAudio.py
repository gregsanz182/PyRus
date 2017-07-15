from PySide.QtCore import QProcess, QIODevice, QFile, QByteArray
from os import path

class FileAudio():

    def __init__(self, metaInfo):
        self.completePath = metaInfo["General"]["Complete name"]
        self.title = metaInfo["General"].get("Track name")
        self.album_artist = metaInfo["General"].get("Album/Performer")
        self.artist =  metaInfo["General"].get("Performer")
        self.album =  metaInfo["General"].get("Album")
        self.track = metaInfo["General"].get("Track name/Position")
        self.totalTracks = metaInfo["General"].get("Track name/Total")
        self.numberDisc =  metaInfo["General"].get("Part/Position")
        self.totalNumberDisc = metaInfo["General"].get("Part/Total")
        self.genre = metaInfo["General"].get("Genre")
        self.year = metaInfo["General"].get("Recorded date")
        self.commentary = metaInfo["General"].get("Comment")
        self.bitrate = metaInfo["Audio"].get("Bit rate")
        self.bitrateMode = metaInfo["Audio"].get("Bit rate mode")
        self.coverFile = self.getAlbumCover(metaInfo)
        self.lyrics = metaInfo["General"].get("Lyrics")

    def printTags(self):
        print("Comple Path:", self.completePath)
        print("Title:", self.title)
        print("Album Artist:", self.album_artist)
        print("Artist:", self.artist)
        print("Album:", self.album)
        print("Track num:", self.track)
        print("Total tracks:", self.totalTracks)
        print("Disc number:", self.numberDisc)
        print("Total Number Disc:", self.totalNumberDisc)
        print("Genre:", self.genre)
        print("Year:", self.year)
        print("Commentary:", self.commentary)
        print("Bitrate:", self.bitrate)
        print("Bitrate mode:", self.bitrateMode)
        print("Lyrics:", self.lyrics)
        print("Cover:", self.coverFile)

    def getAlbumCover(self, metaInfo):
        if "Cover" in metaInfo["General"] and metaInfo["General"]["Cover"] == "Yes":
            coverFormat = metaInfo["General"]["Cover MIME"]
            process = QProcess()
            process.start("resources/tools/mediainfo.exe", ["--Inform=file://resources/tools/art.txt", self.completePath])
            process.waitForFinished();
            if process.canReadLine():
                cad = process.readLine()
                byte = QByteArray.fromBase64(cad)
                name = str(cad)[:60]
                name = "".join(c for c in name if c.isalnum() or c == ' ')
                name += self.album[:10]
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
                return name
        return None
