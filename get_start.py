import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello PyObject")
        imgH, imgW = [800, 600]
        self.set_default_size(imgH, imgW)  # set_size_request(imgH, imgW)
        # set hiden window bar
        self.set_decorated(False)
        # keyname = Gdk.keyval_name(self.key)
        self.connect("key-press-event", self.on_key_press_event)

        # cssProvider = Gtk.CssProvider()
        # cssProvider.load_from_path("theme.css")
        # Gtk.StyleContext.add_provider_for_screen(
        #     Gdk.Screen.get_default(),
        #     cssProvider,
        #     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        # )

        # Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        # context = Gtk.StyleContext(self)
        # Gtk.StyleContext.add_provider_for_screen(
        #     styleContext.get_screen(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        # )

        # Gtk.StyleContext.add_provider_for_screen(
        #     self,
        #     # Gdk.Screen.get_default(),
        #     style_provider,
        #     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        # )

        # # test UI Box
        self.box = Gtk.Box()
        self.add(self.box)
        # # test UI Grid
        # # add a label to box
        # self.label = Gtk.Label()
        # self.label.set_label("First Label")
        # self.label.set_angle(25)
        # self.label.set_halign(Gtk.Align.END)
        # self.add(self.label)
        # self.box.pack_start(self.label, True, True, 0)
        # # add a button to box
        # self.button = Gtk.Button(label="你好嗎!")
        # self.button.connect("clicked", self.on_button_clicked)
        # self.add(self.button)
        # self.box.pack_start(self.button, True, True, 0)

        # #new Grid
        # grid = Gtk.Grid()
        # self.add(grid)
        # # new Button
        # buttonA = Gtk.Button(label="Button A")
        # buttonA.connect("clicked", self.on_button_clicked)
        # buttonB = Gtk.Button(label="Button B")
        # # add button to grid
        # grid.add(buttonA)
        # grid.attach(buttonB, 1, 0, 4, 3)

        # image widget test
        imageFile = "medias/temp1.jpg"
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(imageFile)
        # imgH, imgW = [pixbuf.get_width() / 2, pixbuf.get_height() / 2]
        pixbuf = pixbuf.scale_simple(
            imgH * 0.8, imgW * 0.8, GdkPixbuf.InterpType.BILINEAR
        )
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        # image.props(opacity=0.5)
        image.opacity = 0.1
        # self.box.add(image)

        # self.evbox = Gtk.EventBox()
        # make a gdk.color for red
        # map = self.box.get_colormap()
        # color = map.alloc_color("red")
        # copy the current style and replace the background
        # style = self.box.get_style().copy()
        # style.bg[Gtk.STATE_NORMAL] = color

        # set the button's style to the one you created
        # self.box.set_style(style)

        self.box.override_background_color(0, Gdk.RGBA(0.5, 0.5, 0.5, 1))
        self.box.add(image)
        # self.box.pack_start(self.evbox, True, True, 0)

    def on_button_clicked(self, widget):
        print("你好嗎!")

    def on_key_press_event(self, widget, event):
        # print("Key press on widget: ", widget)
        # print("          Modifiers: ", event.state)
        # print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_q:
            print("Quit App")
            Gtk.main_quit()


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
# print(dir(win.button.props))
# win.set_size_request(800, 600)
win.set_position(Gtk.WindowPosition.CENTER)
win.set_resizable(False)
win.show_all()
Gtk.main()
