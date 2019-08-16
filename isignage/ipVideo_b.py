#!/usr/bin/env python
import sys
import gi
import time
import ctypes
from os import path

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GObject, Gtk, GstVideo, Gdk


class ipVideo(Gtk.DrawingArea):
    def __init__(self, name, file, w, h):
        # GObject.threads_init()
        # print("ipVideo_init")
        Gtk.DrawingArea.__init__(self)
        self.set_size_request(w, h)
        self.connect("draw", self.on_draw)
        self.connect("realize", self.on_realize)
        # self.connect("destroy", self.on_destroy)
        self.connect("unrealize", self.on_unrealize)

        self.videoFile = file
        self.playflag = "init"
        # self.player = None
        # self.bus = None

    def gstPlayerInit(self):
        # Gst.init(None)
        # Create GStreamer pipelineclearPropertis
        # self.pipeline = Gst.Pipeline()
        # Setup GStreamer
        self.player = Gst.ElementFactory.make("playbin", "MultimediaPlayer")

        self.bus = self.player.get_bus()
        # self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_eos)
        self.bus.connect("message::error", self.on_error)
        self.bus.enable_sync_message_emission()
        # used to get messages that GStreamer emits
        # self.bus.connect("message", self.on_message)
        # used for connecting video to your application
        self.bus.connect("sync-message::element", self.on_sync_message)

        # Add playbin to the pipeline
        # self.pipeline.add(self.player)

        # start playing default video
        self.player.set_property("uri", "file:///" + self.videoFile)
        # self.pipeline.set_state(Gst.State.PLAYING)
        # self.startPlay()

    def on_realize(self, widget, data=None):
        print("on_relaize")
        self.gstPlayerInit()

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

        self.show_all()
        # print("winid", self.winid)

        # self.queue_draw()

    def startPlay(self):
        self.player.set_state(Gst.State.PLAYING)
        self.playflag = "playing"
        print("playflag:", self.playflag)

    def stopPlay(self):
        self.player.set_state(Gst.State.NULL)
        self.playflag = "stop"
        print("playflag:", self.playflag)

    def on_draw(self, widget, cr):
        print("ondraw")
        if self.player.get_state(0).state < Gst.State.PAUSED:
            # if self.pipeline.get_state(0).state < Gst.State.PAUSED:
            allocation = widget.get_allocation()
            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(0, 0, allocation.width, allocation.height)
            cr.fill()

    def on_unrealize(self, widget, data=None):
        print("on_unrealize")
        self.player.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        if message.get_structure() is None:
            return False
        msgStrName = message.get_structure().get_name()
        # print("sync_message", msgStrName)
        if msgStrName == "prepare-window-handle" or msgStrName == "prepare-xwindow-id":
            if sys.platform == "win32":
                # win_id = self.videowidget.window.handle
                window = self.get_window()
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
                win_id = self.window.xid

            assert win_id

            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            if sys.platform == "win32":
                imagesink.set_window_handle(win_id)
            else:
                imagesink.set_xwindow_id(win_id)

    def on_eos(self, bus, msg):
        print("on_eos(): seeking to start of video")
        self.player.seek_simple(
            Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0
        )
        self.player.set_state(Gst.State.NULL)
        time.sleep(0.1)
        self.player.set_state(Gst.State.PLAYING)
        print(self.player.get_state(0).state)

    def on_error(self, bus, msg):
        print("on_error():", msg.parse_error())

    def on_destroy(self, event):
        print("on video destroy")
        # print("clearVideo:")
        # self.playflag = "clear"
        # to prevent racing conditions when closing the window while playing
        self.player.set_state(Gst.State.NULL)
        Gst.deinit()
        # self.pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    pass
    # test()
