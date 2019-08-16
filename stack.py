#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import os, sys

UI_FILE = "pygtk_stack.ui"


class GUI:
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.view_one = self.builder.get_object("box1")
        self.view_two = self.builder.get_object("box2")
        self.stack.add_named(self.view_one, "view one")
        self.stack.add_named(self.view_two, "view two")
        window = self.builder.get_object("window")
        window.add(self.stack)
        window.show_all()

    def view_two_activated(self, meuitem):
        self.stack.set_visible_child(self.view_two)

    def view_one_clicked(self, button):
        self.stack.set_visible_child(self.view_one)

    def on_window_destroy(self, window):
        Gtk.main_quit()


def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
