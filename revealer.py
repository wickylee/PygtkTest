import gi
import sys, os, time, threading

from apscheduler.schedulers.background import BackgroundScheduler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GObject
from os import path
from ipimage import ipImage
from datetime import datetime
from datetime import timedelta
from ipvideo import ipVideo
import random


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello PyObject")
        self.imgH, self.imgW = [800, 600]
        self.set_default_size(self.imgH, self.imgW)  #
        self.set_size_request(self.imgH, self.imgW)
        self.GtkWindowType = Gtk.WindowType.TOPLEVEL
        self.connect("key-press-event", self.on_key_press_event)
        self.data_path = path.join(path.abspath(path.dirname(__file__)), "data")
        self.media_path = path.join(path.abspath(path.dirname(__file__)), "media")

        self.mainBox = Gtk.Fixed()

        self.revealer1 = Gtk.Revealer()
        self.revealer1.set_reveal_child(True)
        self.revealer1.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.revealer1.set_transition_duration(1000)
        self.fixWin = Gtk.Fixed()
        filePath = path.join(self.media_path, "img1.jpg")
        self.newImage = ipImage("demoImage", filePath, 800, 600)
        self.fixWin.put(self.newImage, 0, 0)
        self.revealer1.add(self.fixWin)
        self.mainBox.put(self.revealer1, 0, 0)

        self.revealer2 = Gtk.Revealer()
        self.revealer2.set_reveal_child(False)
        self.revealer2.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.revealer2.set_transition_duration(1000)
        self.fixWin2 = Gtk.Fixed()
        filePath = path.join(self.media_path, "img2.jpg")
        self.newImage2 = ipImage("demoImage3", filePath, 800, 600)
        self.fixWin2.put(self.newImage2, 0, 0)
        self.newVideo = ipVideo(
            "tempVideo", path.join(self.media_path, "Video1280x720b.mp4"), 640, 480
        )
        self.fixWin.put(self.newVideo, 0, 0)
        self.revealer2.add(self.fixWin2)
        self.mainBox.put(self.revealer2, 0, 0)

        self.revealer3 = Gtk.Revealer()
        self.revealer3.set_reveal_child(False)
        self.revealer3.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.revealer3.set_transition_duration(1000)
        self.fixWin3 = Gtk.Fixed()
        filePath = path.join(self.media_path, "img5.jpg")
        self.newImage3 = ipImage("demoImage5", filePath, 800, 600)
        self.fixWin3.put(self.newImage3, 0, 0)
        self.revealer3.add(self.fixWin3)
        self.mainBox.put(self.revealer3, 0, 0)

        self.add(self.mainBox)
        self.show_all()

        self.iScheduler = BackgroundScheduler()
        exec_date = datetime.now() + timedelta(seconds=5)
        print(exec_date)
        self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        self.iScheduler.start()

    def switchClipWin(self):
        self.revealer1.set_reveal_child(False)
        self.revealer2.set_reveal_child(True)
        # self.newVideo.startPlay()
        print("switchClipWin")
        exec_date = datetime.now() + timedelta(seconds=10)
        print(exec_date)
        self.iScheduler.add_job(self.switchClipWin2, "date", run_date=exec_date)

    def switchClipWin2(self):
        # self.newVideo.stopPlay()
        self.revealer2.set_reveal_child(False)
        self.revealer3.set_reveal_child(True)
        print("switchClipWin2")

    def on_key_press_event(self, widget, event):
        # print("Key press on widget: ", widget)
        # print("          Modifiers: ", event.state)
        # print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_q:
            print("Quit App")
            Gtk.main_quit()


GObject.threads_init()
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
# print(dir(win.button.props))
# win.set_size_request(800, 600)
win.set_position(Gtk.WindowPosition.CENTER)
# win.set_resizable(False)

Gtk.main()
