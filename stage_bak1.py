#!/usr/bin/env python
import sys, os, time, threading
import gi
import ctypes

from os import path
from apscheduler.schedulers.background import BackgroundScheduler

gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
gi.require_version("WebKit2", "3.0")
gi.require_version("GstVideo", "1.0")
gi.require_version("EvinceView", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import (
    Gtk,
    Gdk,
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

# Poppler

data_path = path.join(path.abspath(path.dirname(__file__)), "data")
media_path = path.join(path.abspath(path.dirname(__file__)), "media")


class videoWedgit(Gtk.DrawingArea):
    def __init__(self, file, w, h):
        Gtk.DrawingArea.__init__(self)
        self.set_size_request(w, h)
        self.connect("draw", self.on_draw)
        self.connect("realize", self.on_realize)
        self.connect("unrealize", self.on_unrealize)

        # Create GStreamer pipeline
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
        self.player.set_property("uri", "file:///" + path.join(media_path, file))
        # self.pipeline.set_state(Gst.State.PLAYING)
        self.player.set_state(Gst.State.PLAYING)

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
        if self.player.get_state(0).state < Gst.State.PAUSED:
            # if self.pipeline.get_state(0).state < Gst.State.PAUSED:
            allocation = widget.get_allocation()
            cr.set_source_rgb(0, 0, 0)
            cr.rectangle(0, 0, allocation.width, allocation.height)
            cr.fill()

    def on_unrealize(self, widget, data=None):
        # to prevent racing conditions when closing the window while playing
        self.player.set_state(Gst.State.NULL)
        # self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        if message.get_structure() is None:
            return False
        msgStrName = message.get_structure().get_name()
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
        self.player.seek_simple(
            Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0
        )
        self.player.set_state(Gst.State.NULL)
        time.sleep(0.1)
        self.player.set_state(Gst.State.PLAYING)
        print(self.player.get_state(0).state)

    def on_error(self, bus, msg):
        print("on_error():", msg.parse_error())


class pdfWedgit(Gtk.ScrolledWindow):
    def __init__(self, file, w, h):
        # Setup pdf window
        Gtk.ScrolledWindow.__init__(self)
        self.doc = EvinceDocument.Document.factory_get_document(
            "file:///" + path.join(media_path, file)
        )
        # evince view
        self.view = EvinceView.View()
        # evince model
        self.model = EvinceView.DocumentModel()
        self.model.set_document(self.doc)
        self.model.set_continuous(False)
        self.model.set_sizing_mode(EvinceView.PageLayout.SINGLE)
        self.model.set_page_layout(EvinceView.SizingMode.FIT_PAGE)
        self.view.set_model(self.model)
        self.set_size_request(w, h)
        self.add(self.view)

    def nextPageOnTime(self):
        if self.model.get_page() < (self.doc.get_n_pages() - 1):
            self.view.next_page()
        else:
            self.model.set_page(0)
        self.model.set_sizing_mode(EvinceView.PageLayout.SINGLE)
        self.model.set_page_layout(EvinceView.SizingMode.FIT_PAGE)


class Stage(Gtk.Window):
    def __init__(self):
        # Setup stage window
        Gtk.Window.__init__(self)
        self.GtkWindowType = Gtk.WindowType.TOPLEVEL
        self.set_title("iPalys Stage")
        self.stageW, self.stageH = [1366, 768]
        self.colW, self.rowH = [self.stageW / 3, self.stageH / 2]
        self.set_default_size(self.stageW, self.stageH)
        self.set_size_request(self.stageW, self.stageH)
        self.set_resizable(False)
        # self.set_decorated(False) # set hiden window bar
        self.set_border_width(0)
        self.set_name("stageWin")
        self.connect("destroy", self.quit)
        # connect Quit Key
        self.connect("key-press-event", self.on_q_control_press_event)
        # create Background job Scheduler
        self.sched = BackgroundScheduler()
        self.load_timeout = None
        self.pixbuf_loader = None
        self.image_stream = None
        self.run = False
        # load css style
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(path.join(data_path, "stage.css"))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),  # self.get_style_context(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # New fixed container
        fixCon = Gtk.Fixed()
        self.add(fixCon)
        # add Partition layout
        grid = Gtk.Grid(name="layoutGrid")
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        # add media to stage
        grid.attach(self.loadImage("img0", "img0.jpg", 1, 2), 0, 0, 1, 2)
        grid.attach(self.loadImage("img1", "img1.jpg", 2, 1), 1, 0, 2, 1)
        grid.attach(self.loadImage("img2", "img2.jpg", 1, 1), 1, 1, 1, 1)
        grid.attach(self.loadImage("img3", "img3.jpg", 1, 1), 2, 1, 1, 1)
        fixCon.put(grid, 0, 0)

        # Add a WebFrame
        # webFrame = Gtk.Frame(name="webFrame")
        # webview = WebKit2.WebView()
        # webview.load_uri("http://api.jquery.com")
        # webview.set_size_request(400, 600)
        # webFrame.add(webview)
        # fixCon.put(webFrame, 10, 10)

        # add a Image
        image = self.loadImage("img5", "img5.jpg", 1, 1)
        fixCon.put(image, 300, 100)

        # add pdf file
        # EvinceDocument.init()
        # self.pdfwedgit_1 = pdfWedgit("OsmoManual_v1.0_en.pdf", 500, 720)
        # self.sched.add_job(self.pdfwedgit_1.nextPageOnTime, "interval", seconds=5)
        # fixCon.put(self.pdfwedgit_1, 400, 10)

        # self.pdfwedgit_2 = pdfWedgit("id697.pdf", 300, 400)
        # self.sched.add_job(self.pdfwedgit_2.nextPageOnTime, "interval", seconds=5)
        # fixCon.put(self.pdfwedgit_2, 10, 400)

        # add video
        videowidget1 = videoWedgit("Video1280x720b.mp4", 400, 250)
        # Video1280x720b.mp4,Wildlife.mp4

        self.msgLabel = Gtk.Label("香港九龍尖沙咀東麼地道67號半島中心香港九龍尖沙咀東麼地道67號半島中心")
        self.msgLabel.set_name("msgLabel")

        tickerBox = Gtk.Box()
        tickerBox.set_size_request(1024, 100)
        tickerBox.set_name("scrollMsgBox")

        self.scrollingBox = Gtk.Fixed()
        self.set_opacity(0.5)
        self.scrollingBox.put(self.msgLabel, 1000, 20)
        tickerBox.add(self.scrollingBox)

        fixCon.put(tickerBox, 0, 668)
        fixCon.put(videowidget1, 600, 10)
        # self.sched.add_job(self.tickerScrolling, "interval", seconds=1)
        # self.t = perpetualTimer(0.5, self.tickerScrolling)
        # self.t.start()
        # GObject.timeout_add(10, self.tickerScrolling)
        # overlay container test --
        # overlay = Gtk.Overlay()
        # overlay.add_overlay(grid)
        # overlay.add_overlay(fixCon)
        # overlay.add_overlay(self.loadImasge("img4", "img4.jpg", 1, 1))
        # self.add(overlay)
        # -------------------------

        self.show_all()
        self.run = True
        # self.fullscreen()
        # self.sched.start()

    def tickerScrolling(self):
        r = self.msgLabel.get_allocation()
        # print(r.x)
        self.scrollingBox.move(self.msgLabel, (r.x - 1), 0)
        if self.run:
            GObject.timeout_add(100, self.tickerScrolling)

    def loadImage(self, name, imageFile, col, rom):
        # add media to stage
        imagename = path.join(media_path, imageFile)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(imagename)

        pixbuf = pixbuf.scale_simple(
            self.colW * col, self.rowH * rom, GdkPixbuf.InterpType.BILINEAR
        )
        # transparent = pixbuf.add_alpha(True, 0xFF, 0xFF, 0xFF)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        image.set_name(name)
        return image

    def on_q_control_press_event(self, widget, event):
        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_q:
            self.quit(event)

    def quit(self, event):
        if self.load_timeout:
            GLib.source_remove(self.load_timeout)

        if self.pixbuf_loader:
            try:
                self.pixbuf_loader.close()
            except GObject.GError:
                pass

        if self.image_stream:
            self.image_stream.close()

        # self.sched.shutdown()
        self.run = False
        print("Quit App")
        Gtk.main_quit()

    # def on_eos(self, bus, msg):
    #     print("on_eos(): seeking to start of video")
    #     self.pipeline.seek_simple(
    #         Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0
    #     )
    #     self.pipeline.set_state(Gst.State.NULL)
    #     time.sleep(0.1)
    #     self.pipeline.set_state(Gst.State.PLAYING)
    #     print(self.pipeline.get_state(0).state)
    #
    # def on_error(self, bus, msg):
    #     print("on_error():", msg.parse_error())


def main():
    GObject.threads_init()
    Gst.init(None)
    stage = Stage()
    stage.set_position(Gtk.WindowPosition.CENTER)
    stage.set_resizable(False)
    Gtk.main()


if __name__ == "__main__":
    main()
