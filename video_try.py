import sys, os
import gi
from os import path
import ctypes

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk, GstVideo, GdkX11


filename = path.join(path.dirname(path.abspath(__file__)), "media/Video1280x720b.mp4")
uri = "file:///" + filename


class GTK_Main(object):
    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Video-Player")
        # window.set_default_size(500, 400)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        self.entry = Gtk.Entry()
        hbox.add(self.entry)
        self.button = Gtk.Button("Start")
        hbox.pack_start(self.button, False, False, 0)
        self.button.connect("clicked", self.start_stop)
        self.movie_window = Gtk.DrawingArea()
        self.movie_window.set_size_request(600, 800)
        vbox.add(self.movie_window)
        window.show_all()

        self.player = Gst.ElementFactory.make("playbin", "player")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

        self.player.set_property("uri", uri)
        self.player.set_state(Gst.State.PLAYING)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.set_property("uri", uri)
                self.player.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            # print "Error: %s" %err, debug
            self.button.set_label("Start")

    def on_sync_message(self, bus, message):
        if message.get_structure() is None:
            return False
        msgStrName = message.get_structure().get_name()
        if msgStrName == "prepare-window-handle" or msgStrName == "prepare-xwindow-id":
            print(msgStrName)
            if sys.platform == "win32":
                # win_id = self.videowidget.window.handle
                window = self.movie_window.get_window()
                if not window.ensure_native():
                    print("Error - video playback requires a native window")
                ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
                drawingarea_gpointer = ctypes.pythonapi.PyCapsule_GetPointer(
                    window.__gpointer__, None
                )
                gdkdll = ctypes.CDLL("libgdk-3-0.dll")
                win_id = gdkdll.gdk_win32_window_get_handle(drawingarea_gpointer)
            else:
                win_id = self.movie_window.window.xid
            print("win_id")
            print(win_id)
            # assert win_id
            imagesink = message.src
            print(imagesink)
            imagesink.set_property("force-aspect-ratio", True)
            if sys.platform == "win32":
                imagesink.set_window_handle(win_id)
            else:
                imagesink.set_xwindow_id(win_id)


GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()
