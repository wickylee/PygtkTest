#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("EvinceView", "3.0")
from gi.repository import Gtk, GLib, EvinceView, EvinceDocument


class ipPdf(Gtk.ScrolledWindow):
    def __init__(self, name, filePath, w, h, pagetime=5):
        # Setup pdf window
        Gtk.ScrolledWindow.__init__(self)
        self.doc = EvinceDocument.Document.factory_get_document("file:///" + filePath)
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
        self.nextScheduler = None

        if self.model.get_page() > 0:
            self.nextScheduler = BackgroundScheduler()
            self.nextScheduler.add_job(
                self.nextPageOnTime, "interval", seconds=pagetime
            )
            self.nextScheduler.start()

    def nextPageOnTime(self):
        if self.model.get_page() < (self.doc.get_n_pages() - 1):
            self.view.next_page()
        else:
            self.model.set_page(0)
        self.model.set_sizing_mode(EvinceView.PageLayout.SINGLE)
        self.model.set_page_layout(EvinceView.SizingMode.FIT_PAGE)


if __name__ == "__main__":
    pass
    # test()
