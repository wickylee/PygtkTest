import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_name("MyWindow")
        self.set_default_size(600, 300)

        self.box = Gtk.HBox()
        self.box.set_halign(Gtk.Align.CENTER)
        self.box.set_valign(Gtk.Align.CENTER)
        self.add(self.box)

        self.button1 = Gtk.Button(name="but1", label="Hello")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.box.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="Goodbye")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.box.pack_start(self.button2, True, True, 0)

    def on_button1_clicked(self, widget):
        print("Hello")

    def on_button2_clicked(self, widget):
        print("Goodbye")

    def gtk_style(widget):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path("hello.css")

        # Gtk.StyleContext.add_provider_for_screen(
        Gtk.StyleContext.add_provider(
            widget.get_style_context(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


def main(argv):
    win = MyWindow()

    style_provider = Gtk.CssProvider()
    style_provider.load_from_path("helloCss.css")

    Gtk.StyleContext.add_provider(
        win.get_style_context(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    # style_provider = Gtk.CssProvider()
    # style_provider.load_from_path("PygtkTest/hello.css")
    #
    # Gtk.StyleContext.add_provider_for_screen(
    #     Gdk.Screen.get_default(),
    #     style_provider,
    #     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    # )

    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main(sys.argv)
