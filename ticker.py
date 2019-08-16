#!/usr/bin/python
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, GLib, Pango, PangoCairo


class PyApp(Gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()

        self.set_title("Puff")
        self.resize(1000, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.startdraw = False
        self.connect("destroy", Gtk.main_quit)

        self.darea = Gtk.DrawingArea()
        # self.darea.connect("show", self.expose)
        self.connect("draw", self.on_draw)
        self.add(self.darea)

        self.timer = True
        self.fristPosX = 0
        self.alpha = 1.0
        self.size = 38
        self.padding = 150

        GLib.timeout_add(10, self.on_timer)

        self.show_all()

    def on_timer(self):
        if not self.timer:
            return False

        self.darea.queue_draw()
        return True

    def on_draw(self, widget, cr):
        areaW = self.get_allocation().width
        areaH = self.get_allocation().height
        # fill background color
        cr.set_source_rgb(0.5, 0.1, 0.1)
        cr.paint()

        cr.set_font_size(self.size)
        cr.select_font_face("Microsoft JhengHei UI Bold")
        (x, y, width, height, dx, dy) = cr.text_extents("香港九龍尖沙咀東")
        contentWidth = width + self.padding
        # Get nunmber will Repeat
        msgRepeat = int(areaW / contentWidth)

        desc = Pango.font_description_from_string(
            "Microsoft JhengHei UI Bold" + " " + str(self.size)
        )
        # set text color
        cr.set_source_rgba(0.0, 1.0, 0.0, 1.0)

        drawX = self.fristPosX
        for n in range(msgRepeat + 2):
            # print(drawX)
            layout = PangoCairo.create_layout(cr)
            layout.set_font_description(desc)
            cr.move_to(drawX, areaH / 2)
            layout.set_text("香港九龍尖沙咀東", -1)
            # cr.text_path("香港")
            PangoCairo.show_layout(cr, layout)
            drawX = drawX + contentWidth

        if abs(self.fristPosX) < contentWidth:
            self.fristPosX = self.fristPosX - 1
        else:
            self.fristPosX = 0
        # print(self.fristPosX)
        # if self.startdraw:
        #     rx = areaW - self.movex
        #     self.movex = self.movex + 1
        # else:
        #     rx = areaW
        #     self.startdraw = True

        # cr.move_to(self.fristPosX, areaH / 2)
        # layout = PangoCairo.create_layout(cr)
        # desc = Pango.font_description_from_string(
        #     "Microsoft JhengHei UI Bold" + " " + str(self.size)
        # )
        # layout.set_font_description(desc)
        # cr.set_source_rgba(0.0, 1.0, 0.0, 1.0)
        # layout.set_text("香港九龍尖沙咀", -1)

        cr.clip()
        # cr.stroke()

        # if rx < 0:
        #    self.timer = False


PyApp()
Gtk.main()
