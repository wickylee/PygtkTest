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
from isignage.ipDataPool import ipDataPool
from isignage.ipFrame import ipFrame
from isignage.ipElement import ipElement
from isignage.ipImage import ipImage
from isignage.ipPdf import ipPdf
from isignage.ipTicker import ipTicker
from isignage.ipVideo import ipVideo
from isignage.ipWeb import ipWeb

dataPath = path.join(path.abspath(path.dirname(__file__)), "data")
mediaPath = path.join(path.abspath(path.dirname(__file__)), "media")


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.application_id = "iSignage Player"
        # create Background job Scheduler
        self.iScheduler = BackgroundScheduler()
        self.clipFrames = []
        self.playframeIndex = 0
        self.dataPool = ipDataPool(dataPath, mediaPath, "clipFrames.json")

    def do_activate(self):
        # creat main window --
        self.mainWin = AppWin("Main Window", self)

        # produce the presentaion media data
        self.clipFrames = self.dataPool.produceClipFrames()

        for fm in self.clipFrames:
            self.mainWin.get_children()[0].put(fm, 0, 0)

        # add video
        for fm in self.clipFrames:
            fm.showVideo()

        self.mainWin.show_all()
        self.switchClipWin()
        self.iScheduler.start()

    def switchClipWin(self,):
        print("switchClipWin -> ", self.playframeIndex)
        self.clipFrames[self.playframeIndex - 1].stopVideo()

        for fm in self.clipFrames:
            fm.hide()

        # to show next frame
        opacity = 0.1
        self.clipFrames[self.playframeIndex].set_opacity(opacity)
        self.clipFrames[self.playframeIndex].show_all()

        while opacity < 1:
            opacity = opacity + 0.1
            self.clipFrames[self.playframeIndex].set_opacity(opacity)
            time.sleep(0.1)

        self.clipFrames[self.playframeIndex].playVideo()

        # set this frame display time --
        nextTime = self.dataPool.fShowTime[self.playframeIndex]
        exec_date = datetime.now() + timedelta(seconds=nextTime)
        self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        print(exec_date)

        # reset playframeIndex to next or jump to start
        self.playframeIndex = self.playframeIndex + 1
        if self.playframeIndex == len(self.dataPool.fShowTime):
            self.playframeIndex = 0

    def on_quit(self, action, param):
        self.appQuit()

    def appQuit(self):
        self.sched.shutdown()
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
        self.set_decorated(False)  # set hiden window bar
        self.set_border_width(0)
        self.set_name("stageWin")

        # connect Quit Key
        self.connect("key-press-event", self.on_q_control_press_event)

        # load css style
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(path.join(dataPath, "stage.css"))

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
