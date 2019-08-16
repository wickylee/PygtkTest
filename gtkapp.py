#!/usr/bin/python
# coding=utf8
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import GObject, Gio, Gdk, Gtk
import gtkapp_portion


class MyApplication(Gtk.Application):
    # Main initialization routine
    def __init__(self, application_id, flags):
        Gtk.Application.__init__(self, application_id=application_id, flags=flags)
        self.connect("activate", self.new_window)

    def new_window(self, *args):
        AppWindow(self)


class AppWindow(object):
    def __init__(self, application):
        self.Application = application

        # Read GUI from file and retrieve objects from Gtk.Builder
        try:
            GtkBuilder = Gtk.Builder.new_from_file("gtkapp_login.ui")
            GtkBuilder.connect_signals(gtkapp_portion.lgn(application, GtkBuilder))
        except GObject.GError:
            print("Error reading GUI file")
            raise

        # Fire up the main window
        self.MainWindow = GtkBuilder.get_object("LoginWindow")
        self.MainWindow.set_application(application)
        self.MainWindow.show()
        if GtkBuilder.get_application().get_window_by_id(2):
            GtkBuilder.get_application().get_window_by_id(2).destroy()

    def close(self, *args):
        self.MainWindow.destroy()


# Starter
def main():
    # Initialize GTK Application
    Application = MyApplication("com.b.example", Gio.ApplicationFlags.FLAGS_NONE)

    # Start GUI
    Application.run()


if __name__ == "__main__":
    main()
