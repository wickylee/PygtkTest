from os import path
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .ipImage import ipImage
from .ipPdf import ipPdf
from .ipTicker import ipTicker
from .ipVideo import ipVideo
from .ipWeb import ipWeb


class ipFrame(Gtk.Box):
    def __init__(self, fIndex, ipElements, showTime, mediaPath):
        Gtk.Box.__init__(self)
        self.fIndex = fIndex
        self.showTime = showTime
        self.mPath = mediaPath
        self.fixedlayout = Gtk.Fixed()
        self.add(self.fixedlayout)

        self.emVideo = None
        self.VideoWidget = None

        for em in ipElements:
            nE = None
            if em.elementType == "image":
                nE = ipImage(
                    em.name, path.join(self.mPath, em.src), em.width, em.height
                )
            if em.elementType == "pdf":
                nE = ipPdf(em.name, path.join(self.mPath, em.src), em.width, em.height)
            if em.elementType == "ticker":
                nE = ipTicker(em.name, em.src, em.width, em.height)
            if em.elementType == "video":
                self.emVideo = em
            if em.elementType == "web":
                nE = ipWeb(em.name, em.src, em.width, em.height)
            if nE is not None:
                self.fixedlayout.put(nE, em.px, em.py)

    def showVideo(self):
        if self.emVideo is not None:
            self.VideoWidget = ipVideo(
                self.emVideo.name,
                path.join(self.mPath, self.emVideo.src),
                self.emVideo.width,
                self.emVideo.height,
            )
            self.fixedlayout.put(self.VideoWidget, self.emVideo.px, self.emVideo.py)

    def playVideo(self):
        if self.VideoWidget is not None:
            self.VideoWidget.startPlay()

    def stopVideo(self):
        if self.VideoWidget is not None:
            self.VideoWidget.stopPlay()


if __name__ == "__main__":
    pass
    # test()
