import gi
import sys, os, time, threading

from apscheduler.schedulers.background import BackgroundScheduler

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio, GLib
from os import path
from ipimage import ipImage
from datetime import datetime
from datetime import timedelta
import random


class RevealerWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Revealer Example")
        self.data_path = path.join(path.abspath(path.dirname(__file__)), "data")
        self.media_path = path.join(path.abspath(path.dirname(__file__)), "media")

        fixed = Gtk.Fixed()
        fixed.set_size_request(800, 600)
        revealer = Gtk.Revealer()

        filePath = path.join(self.media_path, "img1.jpg")
        self.image = ipImage("demoImage", filePath, 800, 600)
        # Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
        revealer.add(self.image)
        revealer.set_reveal_child(True)
        revealer.set_transition_duration(1000)
        revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)

        fixed.add(revealer)
        _, w, h = Gtk.IconSize.lookup(Gtk.IconSize.MENU)
        self.width = fixed.get_size_request()[0] - w
        self.height = fixed.get_size_request()[1] - h
        self.add(fixed)
        GLib.timeout_add(1000, self.timeout, fixed, revealer)

    def timeout(self, fixed, revealer):
        isshow = revealer.get_reveal_child()
        # if not isshow:
        #     filePath = path.join(self.media_path, "img5.jpg")
        #     self.image = ipImage("demoImage5", filePath, 800, 600)
        #     # self.image.modify_bg(
        #     #     Gtk.StateType.NORMAL,
        #     #     Gdk.Color.from_floats(
        #     #         random.random(), random.random(), random.random()
        #     #     ),
        #     # )
        #     # x, y = int(self.width * random.random()), int(self.height * random.random())
        #     # fixed.move(revealer, x, y)
        # print("isshow:", isshow)
        revealer.set_reveal_child(not isshow)
        return True


def main():
    win = RevealerWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
