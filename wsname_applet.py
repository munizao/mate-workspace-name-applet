#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Uncomment to debug. If you aren't me, I bet you want to change the paths, too.
import sys
from wsnamelet import wsnamelet_globals
if wsnamelet_globals.debug:
    sys.stdout = open ("/home/munizao/hacks/wsnamelet/debug.stdout", "w", buffering=1)
    sys.stderr = open ("/home/munizao/hacks/wsnamelet/debug.stderr", "w", buffering=1)

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("MatePanelApplet", "4.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Pango
from gi.repository import MatePanelApplet
gi.require_version ("Wnck", "3.0")
from gi.repository import Wnck
from gi.repository import Gio



 
#Internationalize
import locale
import gettext
gettext.bindtextdomain('wsnamelet', wsnamelet_globals.localedir)
gettext.textdomain('wsnamelet')
locale.bindtextdomain('wsnamelet', wsnamelet_globals.localedir)
locale.textdomain('wsnamelet')
gettext.install('wsnamelet', wsnamelet_globals.localedir)

#screen = None

class WSNamePrefs(object):    
    def __init__(self, applet):
        self.applet = applet
        self.dialog = Gtk.Dialog("Workspace Name Applet Preferences",
                                 None,
                                 Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                 (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE))
        self.dialog.set_border_width(10)
        width_spin_label = Gtk.Label(label=_("Applet width in pixels:"))
        width_adj = Gtk.Adjustment(lower=30, upper=500, step_incr=1)
        self.width_spin_button = Gtk.SpinButton.new(width_adj, 0.0, 0)
        self.applet.settings.bind("width", self.width_spin_button, "value", Gio.SettingsBindFlags.DEFAULT)
        width_spin_hbox = Gtk.HBox()
        width_spin_hbox.pack_start(width_spin_label, True, True, 0)
        width_spin_hbox.pack_start(self.width_spin_button, True, True, 0)
        self.dialog.vbox.add(width_spin_hbox)
        

class WSNameEntry(Gtk.Entry):
    def __init__(self, applet):
        Gtk.Widget.__init__(self)
        self.connect("activate", self._on_activate)
        self.connect("key-release-event", self._on_key_release)
        self.applet = applet

    def _on_activate(self, event):
        text = self.get_text()
        self.applet.workspace.change_name(text)
        self.applet.label.set_text(text)
        self.applet.exit_editing()

    def _on_key_release(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.applet.exit_editing()


class WSNameApplet(MatePanelApplet.Applet):
    _name_change_handler_id = None
    workspace = None
    settings = None
    prefs = None
    width = 100
    editing = False
    
    def __init__(self, applet):
        self.applet = applet;
        menuxml = """
        <menuitem name="Prefs" action="Prefs" />
        <menuitem name="About" action="About" />
 
        """

        actions = [("Prefs", Gtk.STOCK_PREFERENCES, "Preferences", None, None, self._display_prefs), 
                   ("About", Gtk.STOCK_ABOUT, "About", None, None, self._display_about)]
        actiongroup = Gtk.ActionGroup.new("WsnameActions")
        actiongroup.add_actions(actions, None)
        applet.setup_menu(menuxml, actiongroup)
        self.init()

    def _display_about(self, action):
        about = Gtk.AboutDialog()
        about.set_program_name("Workspace Name Applet")
        about.set_version(wsnamelet_globals.version)
        about.set_copyright("© 2006 - 2015 Alexandre Muñiz")
        about.set_comments("View and change the name of the current workspace.\n\nTo change the workspace name, click on the applet, type the new name, and press Enter.")
        about.set_website("https://github.com/munizao/mate-workspace-name-applet")
        about.connect ("response", lambda self, *args: self.destroy ())
        about.show_all()

    def _display_prefs(self, action):
        self.prefs.dialog.show_all()
        self.prefs.dialog.run()
        self.prefs.dialog.hide()
        
    def set_width(self, width):
        self.width = width
        self.button.set_size_request(width, -1)
        self.button.queue_resize()
        self.entry.set_size_request(width, -1)
        self.entry.queue_resize()

    def on_width_changed(self, settings, key):
        width = settings.get_int(key)
        self.set_width(width)

    def init(self):
        self.button = Gtk.Button()
        self.button.connect("button-press-event", self._on_button_press)
        self.button.connect("button-release-event", self._on_button_release)
        self.label = Gtk.Label()
        self.label.set_ellipsize(Pango.EllipsizeMode.END)
        self.applet.add(self.button)
        self.button.add(self.label)
        self.entry = WSNameEntry(self)
        self.entry.connect("button-press-event", self._on_entry_button_press)
        try:
            self.settings = Gio.Settings.new("com.puzzleapper.wsname-applet-py")
            self.set_width(self.settings.get_int("width"))
            self.settings.connect("changed::width", self.on_width_changed)
        except:
            self.set_width(100)
        self.screen = Wnck.Screen.get_default()
        self.workspace = really_get_active_workspace(self.screen)
        self.screen.connect("active_workspace_changed", self._on_workspace_changed)
        self.button.set_tooltip_text(_("Click to change the name of the current workspace"))
        self._name_change_handler_id = None
        self.prefs = WSNamePrefs(self)
        self.show_workspace_name()
        self.applet.show_all()
        return True	    

    def _on_button_press(self, button, event, data=None):
        if event.button != 1:
            button.stop_emission("button-press-event")

    def _on_button_release(self, button, event, data=None):
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
            self.editing = True
            self.applet.remove(self.button)
            self.applet.add(self.entry)
            self.entry.set_text(self.workspace.get_name())
            self.entry.set_position(-1)            
            self.entry.select_region(0, -1)
            self.applet.request_focus(event.time)
            GObject.timeout_add(0, self.entry.grab_focus)
            self.applet.show_all()

    def _on_entry_button_press(self, entry, event, data=None):
        self.applet.request_focus(event.time)

    def _on_workspace_changed(self, event, old_workspace):
        if self.editing:
            self.exit_editing()
        if (self._name_change_handler_id):
            self.workspace.disconnect(self._name_change_handler_id)
            self.workspace = really_get_active_workspace(self.screen)
        self._name_change_handler_id = self.workspace.connect("name-changed", self._on_workspace_name_changed)
        self.show_workspace_name()

    def _on_workspace_name_changed(self, event):
	    self.show_workspace_name()

    def show_workspace_name(self):
        if self.workspace:
            self.label.set_text(self.workspace.get_name())
        self.applet.show_all()

    def exit_editing(self):
        self.editing = False
        self.applet.remove(self.entry)
        self.applet.add(self.button)


def really_get_active_workspace(screen):
    # This bit is needed because wnck is asynchronous.
    while Gtk.events_pending():
        Gtk.main_iteration() 
    return screen.get_active_workspace()

def applet_factory(applet, iid, data):
    WSNameApplet(applet)
    return True

MatePanelApplet.Applet.factory_main("WsnameAppletFactory", 
                                    True,
                                    MatePanelApplet.Applet.__gtype__,
                                    applet_factory, 
                                    None)
