import sys, os, time, threading
import gi, ctypes

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
gi.require_version("WebKit2", "3.0")
gi.require_version("GstVideo", "1.0")
gi.require_version("EvinceView", "3.0")
gi.require_version("PangoCairo", "1.0")
from datetime import datetime
from datetime import timedelta
from os import path
from apscheduler.schedulers.background import BackgroundScheduler
from gi.repository import (
    Gtk,
    Gdk,
    Gio,
    WebKit2,
    GdkPixbuf,
    GLib,
    GObject,
    Gst,
    GstVideo,
    EvinceView,
    EvinceDocument,
    Pango,
    PangoCairo,
)

# import isignage iplays media element class
from isignage.ipImage import ipImage
from isignage.ipPdf import ipPdf
from isignage.ipTicker import ipTicker
from isignage.ipVideo import ipVideo
from isignage.ipWeb import ipWeb

data_path = path.join(path.abspath(path.dirname(__file__)), "data")
media_path = path.join(path.abspath(path.dirname(__file__)), "media")


class playElement(object):
    def __init__(self, name, elementType, info, width, height, dx, dy):
        self.name = name
        self.elementType = elementType
        self.info = info
        self.width = width
        self.height = height
        self.dx = dx
        self.dy = dy


class layoutBox(Gtk.Box):
    def __init__(self, elementList):
        Gtk.Box.__init__(self)
        self.video = None
        self.videoElem = None
        self.fixCon = Gtk.Fixed()
        self.add(self.fixCon)

        for elem in elementList:
            addElem = None
            if elem.elementType == "image":
                addElem = ipImage(
                    elem.name, path.join(media_path, elem.info), elem.width, elem.height
                )
            if elem.elementType == "pdf":
                addElem = ipPdf(
                    elem.name, path.join(media_path, elem.info), elem.width, elem.height
                )
            if elem.elementType == "ticker":
                addElem = ipTicker(elem.name, elem.info, elem.width, elem.height)
            if elem.elementType == "video":
                self.video = elem
            if elem.elementType == "web":
                addElem = ipWeb(elem.name, elem.info, elem.width, elem.height)
            if addElem is not None:
                self.fixCon.put(addElem, elem.dx, elem.dy)

    def showVideo(self):
        if self.video is not None:
            self.videoElem = ipVideo(
                self.video.name,
                path.join(media_path, self.video.info),
                self.video.width,
                self.video.height,
            )
            self.fixCon.put(self.videoElem, self.video.dx, self.video.dy)

    def playVideo(self):
        if self.videoElem is not None:
            self.videoElem.startPlay()

    def stopVideo(self):
        if self.videoElem is not None:
            self.videoElem.stopPlay()


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.application_id = "iSignage Player"
        # create Background job Scheduler
        self.iScheduler = BackgroundScheduler()
        self.EvinceDocumentInit = False
        self.GstInit = False
        self.frameTime = [10, 10, 10]
        self.frames = []
        self.playframeIndex = 0

    def getPlayFrames(self, frmaIndex):
        elements = []
        # frame 1
        if frmaIndex == 0:
            elem1 = playElement("Img0", "image", "img0.jpg", 800, 600, 0, 0)
            elements.append(elem1)
            elem2 = playElement("img1", "image", "img1.jpg", 500, 300, 50, 50)
            elements.append(elem2)
            elem3 = playElement(
                "pdf0", "pdf", "OsmoManual_v1.0_en.pdf", 500, 700, 300, 0
            )
            elements.append(elem3)
        # frame 3
        if frmaIndex == 1:
            elem1 = playElement("Img5", "image", "img5.jpg", 800, 600, 0, 0)
            elements.append(elem1)
            elem2 = playElement("Video1", "video", "Video1280x720b.mp4", 500, 300, 0, 0)
            elements.append(elem2)
        # frame 2
        if frmaIndex == 2:
            elem1 = playElement("Img2", "image", "img2.jpg", 800, 600, 10, 10)
            elements.append(elem1)
            # elem2 = playElement("Video2", "video", "Wildlife.mp4", 640, 480, 100, 10)
            # elements.append(elem2)
            elem2 = playElement(
                "webview1", "web", "http://api.jquery.com", 700, 500, 10, 10
            )
            elements.append(elem2)
            elem3 = playElement("ticker1", "ticker", "香港九龍尖沙咀東麼地道", 800, 100, 0, 500)
            elements.append(elem3)

        if self.EvinceDocumentInit is not True:
            EvinceDocument.init()
        if self.GstInit is not True:
            Gst.init(None)

        return layoutBox(elements)

    # def do_startup(self):
    #     print("Do Startup")

    def do_activate(self):
        self.mainWin = AppWin("Main Window", self)

        self.frames.append(self.getPlayFrames(0))
        self.frames.append(self.getPlayFrames(1))
        self.frames.append(self.getPlayFrames(2))
        for fm in self.frames:
            self.mainWin.get_children()[0].put(fm, 0, 0)

        # add video
        for fm in self.frames:
            fm.showVideo()

        self.mainWin.show_all()

        self.switchClipWin()

        self.iScheduler.start()

    def switchClipWin(self,):
        print("switchClipWin -> ", self.playframeIndex)

        self.frames[self.playframeIndex - 1].stopVideo()

        for fm in self.frames:
            fm.hide()

        # to show next frame
        opacity = 0.1
        self.frames[self.playframeIndex].set_opacity(opacity)
        self.frames[self.playframeIndex].show_all()
        # self.frames[self.playframeIndex].playVideo()
        while opacity < 1:
            opacity = opacity + 0.1
            self.frames[self.playframeIndex].set_opacity(opacity)
            time.sleep(0.1)

        self.frames[self.playframeIndex].playVideo()

        nextTime = self.frameTime[self.playframeIndex]
        exec_date = datetime.now() + timedelta(seconds=nextTime)
        self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        print(exec_date)
        self.playframeIndex = self.playframeIndex + 1
        if self.playframeIndex == len(self.frameTime):
            self.playframeIndex = 0

    def on_quit(self, action, param):
        self.appQuit()

    def appQuit(self):
        # self.sched.shutdown()
        print("Quit App")
        self.quit()


class AppWin(Gtk.Window):
    def __init__(self, title, application):
        Gtk.Window.__init__(self, title=title)
        self.set_application(application)
        # self.app = application
        self.GtkWindowType = Gtk.WindowType.TOPLEVEL
        self.stageW, self.stageH = [1366, 768]
        self.set_default_size(self.stageW, self.stageH)
        self.set_size_request(self.stageW, self.stageH)
        self.set_resizable(False)
        # self.set_decorated(False) # set hiden window bar
        self.set_border_width(0)
        self.set_name("stageWin")
        # self.connect("destroy", self.clearPropertis)
        # connect Quit Key
        self.connect("key-press-event", self.on_q_control_press_event)

        # load css style
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(path.join(data_path, "stage.css"))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),  # self.get_style_context(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.main_area = Gtk.Fixed(name="mainArea")

        self.add(self.main_area)
        self.show_all()

    def on_q_control_press_event(self, widget, event):
        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_q:
            # self.clearPropertis(event)
            self.get_application().appQuit()


# Starter
def main():
    # Initialize GTK Application
    Application = App()

    # Start GUI
    Application.run()

    # GObject.threads_init()

    # Gtk.main()


if __name__ == "__main__":
    main()
