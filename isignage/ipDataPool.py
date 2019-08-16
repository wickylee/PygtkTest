import gi, ctypes, json, codecs
from os import path

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
gi.require_version("EvinceView", "3.0")

from gi.repository import Gtk, Gst, EvinceView, EvinceDocument

from .ipFrame import ipFrame
from .ipElement import ipElement


class ipDataPool(object):
    def __init__(self, dPath, mPath, dataSrc):
        # to do read the josn file for get the screen display contents
        print("ipDataPool")
        self.dPath = dPath
        self.mPath = mPath
        self.fShowTime = []
        self.hasVideo = False
        self.hasPdf = False
        self.clipData = None

        with open(path.join(self.dPath, dataSrc), encoding="utf-8") as read_file:
            self.clipData = json.load(read_file)

    def produceClipFrames(self):
        clipFrames = []  # for store frame in this clip
        findex = 0
        for frame in self.clipData:
            self.fShowTime.append(frame["FrameTime"])
            ipElements = []
            for element in frame["Elements"]:
                # print(element)
                if element["type"] == "video" and self.hasVideo is False:
                    self.hasVideo = True
                    Gst.init(None)
                if element["type"] == "pdf" and self.hasPdf is False:
                    self.hasPdf = True
                    EvinceDocument.init()
                # create ipElement object
                ipEm = ipElement(
                    element["type"],
                    element["name"],
                    element["src"],
                    element["width"],
                    element["height"],
                    element["px"],
                    element["py"],
                )
                ipElements.append(ipEm)

            clipFrames.append(
                ipFrame(findex, ipElements, frame["FrameTime"], self.mPath)
            )
            findex = findex + 1

        if self.hasPdf is not True:
            EvinceDocument.init()
        if self.hasVideo is not True:
            Gst.init(None)
        return clipFrames


if __name__ == "__main__":
    pass
    # test()
