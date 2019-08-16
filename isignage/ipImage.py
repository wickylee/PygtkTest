import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


class ipImage(Gtk.Image):
    def __init__(self, name, filePath, width, height):
        Gtk.Image.__init__(self)
        self.set_name(name)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filePath)
        pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        # transparent = pixbuf.add_alpha(True, 0xFF, 0xFF, 0xFF)
        self.set_from_pixbuf(pixbuf)


if __name__ == "__main__":
    pass
    # test()
