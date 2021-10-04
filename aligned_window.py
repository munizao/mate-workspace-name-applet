#Borrowed from Seth Nickell's gnome-blog applet
#Not actually using this currently, because of stuff being broken in gdk 2.x using glib introspection, which isn't even supposed to work, but Mate requires it. 
#import gtk
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

class AlignedWindow(Gtk.Window):

    def __init__(self, applet):
        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)
        self.applet = applet
        self.alignment = self.applet.get_orient()

	# Skip the taskbar, and the pager, stick and stay on top
        self.set_decorated(False)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.stick()
        self.set_resizable(False)
        print("got through alignedwindow init")


    def positionWindow(self):
        # Get our own dimensions & position
        self.realize()
        Gdk.flush()
        #print self.window.get_geometry()
        #win = self.get_window()
        print("got here pw 1")
        #ought to work when we move to gtk3 and the bindings are unbroken
        # or if I port to gnome flashback
        #ourWidth  = (win.get_geometry())[2]
        #ourHeight = (win.get_geometry())[3]
        (ourWidth, ourHeight) = self.get_size()
        # Get the dimensions/position of the applet
        self.applet.realize()
        #entryX, entryY = self.widgetToAlignWith.window.get_origin()
        #entryWidth  = (self.widgetToAlignWith.window.get_geometry())[2]
        #entryHeight = (self.widgetToAlignWith.window.get_geometry())[3]
        print("got here pw 2")
        #screen = self.applet.get_screen()
        #appletWindow = self.applet.get_window()
        monitor = Gdk.Rectangle(0, 0, 0, 0)
        print("got here pw 2.1")
        appletX = appletY = 0
        (appletX, appletY) = self.applet.window.get_origin()
        print("got here pw 2.2")
        (appletWidth, appletHeight) = self.applet.window.get_size()
        #screen.get_monitor_geometry (screen.get_monitor_at_window (self.applet.window), monitor)
        print("got_here pw 3")
        # Get the screen dimensions
        screenHeight = Gdk.screen_height()
        screenWidth = Gdk.screen_width()

        if appletX + ourWidth < screenWidth:
            # Align to the left of the entry
            newX = appletX
        else:
            # Align to the right of the entry
            newX = (appletX + appletWidth) - ourWidth

        if appletY + appletHeight + ourHeight < screenHeight:
            # Align to the bottom of the entry
            newY = appletY + appletHeight
        else:
            newY = appletY - ourHeight

        # -"Coordinates locked in captain."
        # -"Engage."
        self.move(newX, newY)
        self.show()

