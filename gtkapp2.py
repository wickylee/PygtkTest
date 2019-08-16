#!/usr/bin/python
# coding=utf8
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


class MyApplication(Gtk.Application):
    # Main initialization routine
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)
        # self.iScheduler = BackgroundScheduler()
        self.AppWin = None

    def new_window(self, *args):
        self.AppWin = AppWindow(self)

        # print(datetime.now())
        # exec_date = datetime.now() + timedelta(seconds=5)
        # print(exec_date)
        # self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        # self.iScheduler.start()

    def switchClipWin(self):
        print("switchClipWin")
        # self.AppWin.loginbtn_clicked_cb("switch")
        # self.secondWindow = Gtk.ApplicationWindow()
        # self.secondWindow.set_default_size(800, 600)
        # self.secondWindow.set_application(self)
        #
        # box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.secondWindow.add(box)
        #
        # button2 = Gtk.Button()
        # button2 = Gtk.Button(name="but2", label="secondWindow")
        # box.pack_start(button2, True, True, 0)
        #
        # # self.secondWindow.show_all()
        #
        # self.get_window_by_id(2).set_visible(True)
        # self.get_window_by_id(1).destroy()


class AppWindow(object):
    def __init__(self, application):
        self.Application = application
        # self.iScheduler = BackgroundScheduler()
        # Read GUI from file and retrieve objects from Gtk.Builder
        # try:
        #     GtkBuilder = Gtk.Builder.new_from_file("gtkapp_login.ui")
        #     GtkBuilder.connect_signals(gtkapp_portion.lgn(application, GtkBuilder))
        # except GObject.GError:
        #     print("Error reading GUI file")
        #     raise

        # Fire up the main window
        # self.MainWindow = GtkBuilder.get_object("LoginWindow")
        self.MainWindow = Gtk.ApplicationWindow()
        self.MainWindow.set_default_size(800, 600)
        self.MainWindow.set_application(application)
        # self.MainWindow.connect("realize", self.loginbtn_clicked_cb)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        button1 = Gtk.Button()
        button1 = Gtk.Button(name="but1", label="Hello")
        button1.connect("clicked", self.loginbtn_clicked_cb)
        box.pack_start(button1, True, True, 0)

        self.MainWindow.add(box)
        self.MainWindow.show_all()
        if self.Application.get_window_by_id(2):
            self.Application.get_window_by_id(2).destroy()

    # def close(self, *args):
    #     self.MainWindow.destroy()

    def loginbtn_clicked_cb(self, event):
        # exec_date = datetime.now() + timedelta(seconds=5)
        # self.iScheduler.add_job(self.switchClipWin, "date", run_date=exec_date)
        # self.iScheduler.start()
        # print(exec_date)

        self.secondWindow = Gtk.ApplicationWindow()
        self.secondWindow.set_default_size(800, 600)
        self.secondWindow.set_application(self.Application)
        self.secondWindow.set_application(self.Application)
        # self.secondWindow.connect("realize", self.on_realize)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.secondWindow.add(box)

        button2 = Gtk.Button()
        button2 = Gtk.Button(name="but2", label="secondWindow")
        box.pack_start(button2, True, True, 0)

        self.Application.get_window_by_id(2).set_visible(True)
        self.Application.get_window_by_id(1).destroy()

        self.secondWindow.show_all()

        # print(datetime.now())

    # def on_realize(self, event):
    #     pass


# Starter
def main():
    # Initialize GTK Application
    Application = MyApplication("com.b.example", Gio.ApplicationFlags.FLAGS_NONE)

    # Start GUI
    Application.run()


if __name__ == "__main__":
    main()
