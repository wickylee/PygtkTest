import gi
import os
from os import path


gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "3.0")
from gi.repository import Gtk, Gdk, WebKit2, GdkPixbuf, GLib, GObject, Gst


class Video:
    def __init__(self):
        def on_message(bus, message):
            if message.type == Gst.MESSAGE_EOS:
                # End of Stream
                player.seek(
                    1.0,
                    Gst.FORMAT_TIME,
                    Gst.SEEK_FLAG_FLUSH,
                    Gst.SEEK_TYPE_SET,
                    5000000000,
                    Gst.SEEK_TYPE_NONE,
                    6000000000,
                )
            elif message.type == Gst.MESSAGE_ERROR:
                player.set_state(Gst.STATE_NULL)
                (err, debug) = message.parse_error()
                print("Error: %s", err)

        def on_sync_message(bus, message):
            # if message.structure is None:
            # return False
            # if message.structure.get_name() == "prepare-xwindow-id":
            Gdk.threads_enter()
            Gdk.Display.get_default().sync()
            win_id = videowidget.get_property("window").get_xid()
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_xwindow_id(win_id)
            Gdk.threads_leave()

        def click_me(event, data=None):
            player.seek(
                1.0,
                Gst.FORMAT_TIME,
                Gst.SEEK_FLAG_FLUSH,
                Gst.SEEK_TYPE_SET,
                5000000000,
                Gst.SEEK_TYPE_NONE,
                6000000000,
            )

        win = Gtk.Window()
        win.set_resizable(False)
        win.set_decorated(False)
        win.set_position(Gtk.WindowPosition.CENTER)

        overlay = Gtk.Overlay()
        win.add(overlay)
        overlay.show()

        videowidget = Gtk.DrawingArea()
        overlay.add(videowidget)
        videowidget.set_halign(Gtk.Align.START)
        videowidget.set_valign(Gtk.Align.START)
        videowidget.set_size_request(640, 480)
        videowidget.window.ensure_native()
        videowidget.show()

        fixed = Gtk.Fixed()
        overlay.add_overlay(fixed)
        fixed.show()

        # pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("IMG/IMG-MPG-LOGO.png", 250, 50)
        # imgMPL = Gtk.Image()
        # imgMPL.set_from_pixbuf(pixbuf)
        # eb_imgMPL = Gtk.EventBox()
        # eb_imgMPL.set_visible_window(False)
        # eb_imgMPL.add(imgMPL)
        # fixed.put(eb_imgMPL, 10, 10)
        # imgMPL.show()
        # eb_imgMPL.show()

        win.show_all()

        # Setup GStreamer
        player = Gst.element_factory_make("playbin", "MultimediaPlayer")
        bus = player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        # used to get messages that GStreamer emits
        bus.connect("message", on_message)
        # used for connecting video to your application
        bus.connect("sync-message::element", on_sync_message)
        player.set_property("uri", "file://" + os.getcwd() + "media/Video1280x720b.mp4")
        player.set_state(Gst.STATE_PLAYING)


if __name__ == "__main__":
    Gdk.threads_enter()
    Video()
    Gtk.main()
