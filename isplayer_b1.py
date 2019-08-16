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

# import iplays media element class
from ipimage import ipImage
from ipticker import ipTicker
from ipvideo import ipVideo

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
        # self.connect("realize", self.on_realize)
        self.fixCon = Gtk.Fixed()
        self.add(self.fixCon)

        for elem in elementList:
            addElem = None
            if elem.elementType == "image":
                addElem = ipImage(
                    elem.name, path.join(media_path, elem.info), elem.width, elem.height
                )
            if elem.elementType == "ticker":
                addElem = ipTicker(elem.name, elem.info, elem.width, elem.height)
            if elem.elementType == "video":
                self.video = elem
            if addElem is not None:
                self.fixCon.put(addElem, elem.dx, elem.dy)

    def showVideo(self):
        if self.video is not None:
            addElem = ipVideo(
                self.video.name,
                path.join(media_path, self.video.info),
                self.video.width,
                self.video.height,
            )
            self.fixCon.put(addElem, self.video.dx, self.video.dy)

    # def on_realize(self, event):
    #     pass


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.application_id = "iSignage Player"
        # create Background job Scheduler
        self.iScheduler = BackgroundScheduler()
        self.frameTime = [5, 20, 10]
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
            elem2 = playElement("ticker1", "ticker", "香港九龍尖沙咀東麼地道", 800, 100, 0, 200)
            elements.append(elem2)

        return layoutBox(elements)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.mainWin = AppWin("Main Window", self)

        self.switchClipWin()

        # exec_date = datetime.now() + timedelta(seconds=self.frameTime[0])
        # self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        self.iScheduler.start()

    def checkPlayingVideoAndStop(self):
        layoutbox = self.mainWin.main_area.get_visible_child()
        if layoutbox is not None:
            fixed = layoutbox.get_children()[0]
            if fixed is not None:
                chilVideo = None
                for ch in fixed.get_children():
                    if isinstance(ch, ipVideo):
                        chilVideo = ch

                if chilVideo is not None:
                    chilVideo.stopPlay()
                    print("checkPlayingVideoAndStop")

    def checkVideoAndRemove(self):
        # print("frameName:", frameName)
        # remove(widget)
        layoutbox = self.mainWin.main_area.get_visible_child()
        if layoutbox is not None:
            fixed = layoutbox.get_children()[0]
            if fixed is not None:
                chilVideo = None
                for ch in fixed.get_children():
                    if isinstance(ch, ipVideo):
                        chilVideo = ch
                if chilVideo is not None:
                    self.mainWin.main_area.remove(layoutbox)

    def switchClipWin(self):
        print("switchClipWin -> ", self.playframeIndex)

        frameName = "conWin" + str(self.playframeIndex)

        self.checkPlayingVideoAndStop()
        if self.mainWin.main_area.get_child_by_name(frameName) is None:
            self.mainWin.main_area.add_titled(
                self.getPlayFrames(self.playframeIndex), frameName, frameName
            )
            print("frameName", frameName)
        self.mainWin.main_area.get_child_by_name(frameName).showVideo()
        self.mainWin.show_all()

        self.mainWin.main_area.set_visible_child_name(frameName)

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
        # self.colW, self.rowH = [self.stageW / 3, self.stageH / 2]
        self.set_default_size(self.stageW, self.stageH)
        # self.set_size_request(self.stageW, self.stageH)
        self.set_resizable(False)
        # self.set_decorated(False) # set hiden window bar
        self.set_border_width(0)
        # self.set_name("stageWin")
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

        self.main_area = Gtk.Stack(name="mainArea")
        self.main_area.set_interpolate_size(True)
        # GTK_STACK_TRANSITION_TYPE_NONE
        # GTK_STACK_TRANSITION_TYPE_CROSSFADE
        # GTK_STACK_TRANSITION_TYPE_SLIDE_RIGHT
        # GTK_STACK_TRANSITION_TYPE_SLIDE_LEFT
        # GTK_STACK_TRANSITION_TYPE_SLIDE_UP
        # GTK_STACK_TRANSITION_TYPE_SLIDE_DOWN
        # GTK_STACK_TRANSITION_TYPE_SLIDE_LEFT_RIGHT
        # GTK_STACK_TRANSITION_TYPE_SLIDE_UP_DOWN
        # GTK_STACK_TRANSITION_TYPE_OVER_UP
        # GTK_STACK_TRANSITION_TYPE_OVER_DOWN
        # GTK_STACK_TRANSITION_TYPE_OVER_LEFT
        # GTK_STACK_TRANSITION_TYPE_OVER_RIGHT
        # GTK_STACK_TRANSITION_TYPE_UNDER_UP
        # GTK_STACK_TRANSITION_TYPE_UNDER_DOWN
        # GTK_STACK_TRANSITION_TYPE_UNDER_LEFT
        # GTK_STACK_TRANSITION_TYPE_UNDER_RIGHT
        self.main_area.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.main_area.set_transition_duration(1000)

        # elements = []
        # elem1 = playElement("Img0", "image", "img0.jpg", 500, 300, 10, 10)
        # elements.append(elem1)
        # elem2 = playElement("img1", "image", "img1.jpg", 500, 300, 50, 50)
        # elements.append(elem2)
        #
        # conWin1 = layoutBox(elements)
        # frameName = "conWin" + str(self.get_application().playframeIndex)
        # self.main_area.add_titled(
        #     self.get_application().getPlayFrames(0), frameName, frameName
        # )

        # conWin2 = layoutBox("img1", "img1.jpg")
        # self.main_area.add_titled(conWin2, "conWin2", "conWin2")

        self.add(self.main_area)

        self.show_all()

    def on_q_control_press_event(self, widget, event):
        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_q:
            self.clearPropertis(event)
            self.get_application().appQuit()

    # def clearPropertis(self, event):
    #     if self.load_timeout:
    #         GLib.source_remove(self.load_timeout)
    #
    #     if self.pixbuf_loader:
    #         try:
    #             self.pixbuf_loader.close()
    #         except GObject.GError:
    #             pass
    #
    #     if self.image_stream:
    #         self.image_stream.close()
    #     # Gtk.main_quit()


# Starter
def main():
    # Initialize GTK Application
    Application = App()

    # Start GUI
    Application.run()

    GObject.threads_init()
    # Gst.init(None)
    # Gtk.main()


if __name__ == "__main__":
    main()
