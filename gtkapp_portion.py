import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import GObject, Gio, Gdk, Gtk


class lgn(object):
    def __init__(self, application, builder):
        self.Application = application

    def loginbtn_clicked_cb(self, button):
        builder = Gtk.Builder.new_from_file("gtkapp_portion.ui")
        builder.connect_signals(self)
        self.lgnwins = builder.get_object("applicationwindow1")
        self.lgnwins.set_application(self.Application)

        self.Application.get_window_by_id(2).set_visible(True)
        self.Application.get_window_by_id(1).destroy()
