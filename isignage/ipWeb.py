#!/usr/bin/env python
import gi

from os import path

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "3.0")
from gi.repository import Gtk, WebKit2


class ipWeb(Gtk.Frame):
    def __init__(self, name, url, w, h):
        Gtk.Frame.__init__(self)
        self.set_name = name
        self.view = WebKit2.WebView()
        self.view.load_uri(url)
        self.view.set_size_request(w, h)
        self.add(self.view)


if __name__ == "__main__":
    pass
    # test()
