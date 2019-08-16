import gi

gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Pango, PangoCairo


class ipTicker(Gtk.DrawingArea):
    def __init__(self, name, msg, width, height):
        Gtk.DrawingArea.__init__(self)
        # self.set_size_request(w, h)
        self.connect("draw", self.on_draw)
        self.connect("realize", self.on_realize)
        self.connect("unrealize", self.on_unrealize)
        self.set_size_request(width, height)
        self.name = name
        self.startdraw = False
        self.timer = True
        self.fristPosX = 0
        self.msg = msg
        self.fsize = 32
        self.padding = 200

    def on_timer(self):
        if not self.timer:
            return False

        self.queue_draw()
        return True

    def on_draw(self, widget, cr):
        areaW = self.get_allocation().width
        # areaH = self.get_allocation().height
        # fill background color
        cr.set_source_rgb(0.5, 0.1, 0.1)
        cr.paint()
        # try to get the text block size
        cr.set_font_size(self.fsize)
        cr.select_font_face("Microsoft JhengHei UI Bold")
        (x, y, width, height, dx, dy) = cr.text_extents(self.msg)
        contentWidth = width + self.padding

        # count nunmber will Repeat
        msgRepeat = int(areaW / contentWidth) + 2
        # set layout font
        desc = Pango.font_description_from_string(
            "Microsoft JhengHei UI Bold" + " " + str(self.fsize)
        )
        # set text color
        cr.set_source_rgba(0.0, 1.0, 0.0, 1.0)
        # start draw text block
        drawX = self.fristPosX
        for n in range(msgRepeat + 2):
            layout = PangoCairo.create_layout(cr)
            layout.set_font_description(desc)
            cr.move_to(drawX, height / 2)
            layout.set_text(self.msg, -1)
            PangoCairo.show_layout(cr, layout)
            drawX = drawX + contentWidth

        if abs(self.fristPosX) < contentWidth:
            self.fristPosX = self.fristPosX - 1
        else:
            self.fristPosX = 0

        cr.clip()

    def on_realize(self, widget, data=None):
        GLib.timeout_add(5, self.on_timer)

    def on_unrealize(self, widget, data=None):
        self.timer = False


if __name__ == "__main__":
    pass
    # test()
