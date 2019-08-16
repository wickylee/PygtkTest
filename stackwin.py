import gi
import sys, os, time, threading

from apscheduler.schedulers.background import BackgroundScheduler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
from os import path
from ipimage import ipImage
from datetime import datetime
from datetime import timedelta


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello PyObject")
        imgH, imgW = [800, 600]
        self.set_default_size(imgH, imgW)  # set_size_request(imgH, imgW)
        self.GtkWindowType = Gtk.WindowType.TOPLEVEL
        # set hiden window bar
        # self.set_decorated(False)
        # keyname = Gdk.keyval_name(self.key)
        self.connect("key-press-event", self.on_key_press_event)
        self.data_path = path.join(path.abspath(path.dirname(__file__)), "data")
        self.media_path = path.join(path.abspath(path.dirname(__file__)), "media")

        # box = Gtk.VBox()

        # label = Gtk.Label("Insert text you want to search for:")
        # box.add(label)

        #        self.entry = Gtk.Entry()
        #        box.add(self.entry)

        self.main_area = Gtk.Stack()
        self.main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_area.set_transition_duration(1000)

        self.conWin1 = Gtk.Box()
        self.main_area.add_titled(self.conWin1, "window1", "window1")
        fixCon = Gtk.Fixed()
        self.conWin1.add(fixCon)
        filePath = path.join(self.media_path, "img1.jpg")
        newImage = ipImage("demoImage", filePath, 800, 600)
        fixCon.put(newImage, 0, 0)

        # self.labelS = Gtk.Label()
        # self.label_txt = """<big><i>you have choice to runn the scan directly or after setup the scanning process you want to follow on your target</i></big>"""
        # self.labelS.set_markup(self.label_txt)
        # self.labelS.set_line_wrap(True)

        self.conWin2 = Gtk.Box()
        self.main_area.add_titled(self.conWin2, "window2", "window2")
        fixCon2 = Gtk.Fixed()
        self.conWin2.add(fixCon2)
        filePath2 = path.join(self.media_path, "img5.jpg")
        newImage2 = ipImage("demoImage2", filePath2, 800, 600)
        fixCon2.put(newImage2, 0, 0)

        # self.our_stackSwitcher = Gtk.StackSwitcher()
        # self.our_stackSwitcher.set_stack(self.main_area)

        # box.add(self.our_stackSwitcher)
        # box.add(self.main_area)
        self.add(self.main_area)

        self.show_all()

        self.iScheduler = BackgroundScheduler()
        exec_date = datetime.now() + timedelta(seconds=5)
        print(exec_date)
        self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        self.iScheduler.start()

    def switchClipWin(self):
        print("switchClipWin")
        self.main_area.set_visible_child_name("window2")

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


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
# print(dir(win.button.props))
# win.set_size_request(800, 600)
win.set_position(Gtk.WindowPosition.CENTER)
# win.set_resizable(False)

Gtk.main()
