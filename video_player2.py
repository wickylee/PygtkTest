#!/usr/bin/env python
import sys
import gi
import time
import ctypes
from os import path

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk, GstVideo


# per-set video file
defaultfilename = path.join(
    path.dirname(path.abspath(__file__)), "media\Video1280x720b.mp4"
)


class Main(object):
    def __init__(self):
        self.multimedia_file = ""
        self.playingfile = defaultfilename
        # Create the GUI
        self.win = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.win.set_title("Play Video Example")
        self.win.connect("delete_event", lambda w, e: Gtk.main_quit())

        vbox = Gtk.VBox(False, 0)
        hbox = Gtk.HBox(False, 0)
        self.load_file = Gtk.FileChooserButton("Choose Audio File")
        # create drawingarea for video widget --
        self.videowidget = Gtk.DrawingArea()
        self.videowidget.set_size_request(400, 250)
        self.videowidget.connect("draw", self.on_draw)
        self.videowidget.connect("realize", self.on_realize)
        self.videowidget.connect("unrealize", self.on_unrealize)
        # add playback contral buttons
        self.play_button = Gtk.Button("Play", Gtk.STOCK_MEDIA_PLAY)
        self.pause_button = Gtk.Button("Pause", Gtk.STOCK_MEDIA_PAUSE)
        self.stop_button = Gtk.Button("Stop", Gtk.STOCK_MEDIA_STOP)
        # connect buton event handle
        self.load_file.connect("selection-changed", self.on_file_selected)
        self.play_button.connect("clicked", self.on_playerBtnCall)
        self.pause_button.connect("clicked", self.on_playerBtnCall)
        self.stop_button.connect("clicked", self.on_playerBtnCall)
        # put UI to window
        vbox.pack_start(self.load_file, False, True, 0)
        vbox.pack_start(self.videowidget, True, True, 0)
        hbox.pack_start(self.play_button, False, True, 0)
        hbox.pack_start(self.pause_button, False, True, 0)
        hbox.pack_start(self.stop_button, False, True, 0)
        vbox.pack_start(hbox, False, True, 0)
        self.win.add(vbox)
        self.win.show_all()

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()
        # Setup GStreamer
        self.player = Gst.ElementFactory.make("playbin", "MultimediaPlayer")

        # self.bus = self.player.get_bus()
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)
        self.bus.enable_sync_message_emission()
        # used to get messages that GStreamer emits
        # self.bus.connect("message", self.on_message)
        # used for connecting video to your application
        self.bus.connect("sync-message::element", self.on_sync_message)

        # Add playbin to the pipeline
        self.pipeline.add(self.player)

        # start playing default video
        self.player.set_property("uri", "file:///" + self.playingfile)
        self.pipeline.set_state(Gst.State.PLAYING)
        # self.player.set_state(Gst.State.PLAYING)

    def on_file_selected(self, widget):
        self.multimedia_file = self.load_file.get_filename()

    def on_playerBtnCall(self, widget):
        print(widget.get_label() + "Button Call")
        if widget.get_label() == "Play":
            print(self.pipeline.get_state(0).state)
            filepath = self.multimedia_file
            if path.isfile(filepath) and self.playingfile != filepath:
                self.pipeline.set_state(Gst.State.NULL)
                self.player.set_property("uri", "file:///" + self.multimedia_file)
                self.playingfile = self.multimedia_file
            self.pipeline.set_state(Gst.State.PLAYING)
            print(self.pipeline.get_state(0).state)

        if widget.get_label() == "Pause":
            self.pipeline.set_state(Gst.State.PAUSED)
        if widget.get_label() == "Stop":
            self.pipeline.set_state(Gst.State.NULL)

    # def on_message(self, bus, message):
    #     if message.type == Gst.MessageType.EOS:
    #         # End of Stream
    #         self.player.set_state(Gst.State.NULL)
    #     elif message.type == Gst.MessageType.ERROR:
    #         self.player.set_state(Gst.State.NULL)
    #
    #         (err, debug) = message.parse_error()
    #         print("Error: %s" % err, debug)

    def on_realize(self, widget, data=None):
        print("on_relaize")

        window = widget.get_window()
        if sys.platform == "win32":
            if not window.ensure_native():
                print("Error - video playback requires a native window")
            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
            drawingarea_gpointer = ctypes.pythonapi.PyCapsule_GetPointer(
                window.__gpointer__, None
            )
            gdkdll = ctypes.CDLL("libgdk-3-0.dll")
            win_id = gdkdll.gdk_win32_window_get_handle(drawingarea_gpointer)
        #   win_id = widget.GetHandle()
        else:
            win_id = window.xid
        assert win_id
        self.winid = win_id

    def on_draw(self, widget, cr):
        # print("ondraw", self.player.get_state(0).state)
        if self.pipeline.get_state(0).state < Gst.State.PAUSED:
            allocation = widget.get_allocation()
            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(0, 0, allocation.width, allocation.height)
            cr.fill()

    def on_unrealize(self, widget, data=None):
        # to prevent racing conditions when closing the window while playing
        self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        if message.get_structure() is None:
            return False
        msgStrName = message.get_structure().get_name()
        if msgStrName == "prepare-window-handle" or msgStrName == "prepare-xwindow-id":
            if sys.platform == "win32":
                # win_id = self.videowidget.window.handle
                window = self.videowidget.get_window()
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
                win_id = self.videowidget.window.xid

            assert win_id
            # print("videowidget.window : ")
            # print(win_id)
            # print("----------")
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            if sys.platform == "win32":
                imagesink.set_window_handle(win_id)
            else:
                imagesink.set_xwindow_id(win_id)

    def on_eos(self, bus, msg):
        print("on_eos(): seeking to start of video")
        self.pipeline.seek_simple(
            Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0
        )
        self.pipeline.set_state(Gst.State.NULL)
        time.sleep(0.1)
        self.pipeline.set_state(Gst.State.PLAYING)
        print(self.pipeline.get_state(0).state)

    def on_error(self, bus, msg):
        print("on_error():", msg.parse_error())


if __name__ == "__main__":
    GObject.threads_init()
    Gst.init(None)
    Main()
    Gtk.main()
