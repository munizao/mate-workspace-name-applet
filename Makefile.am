#APPLET_LOCATION = $(libexecdir)/wsnamelet
APPLET_LOCATION = $(bindir)
#python_PYTHON = wsname_applet.py

appletdir = $(datadir)/mate-panel/applets
applet_in_files = org.mate.panel.WsnameApplet.mate-panel-applet.in
applet_DATA = $(applet_in_files:.mate-panel-applet.in=.mate-panel-applet)

$(applet_in_files): $(applet_in_files).in Makefile
	$(AM_V_GEN)sed \
	-e "s|\@LOCATION\@|$(APPLET_LOCATION)|" \
	$< > $@

@PANEL_INTLTOOL_MATE_PANEL_APPLET_RULE@

servicedir = $(DBUS_SERVICES_DIR)
service_in_files = org.mate.panel.applet.WsnameAppletFactory.service.in
service_DATA = $(service_in_files:.service.in=.service)
org.mate.panel.applet.WsnameAppletFactory.service: $(service_in_files)
	$(AM_V_GEN)sed \
	-e "s|\@LOCATION\@|$(APPLET_LOCATION)|" \
	$< > $@

@INTLTOOL_XML_NOMERGE_RULE@
gsettings_SCHEMAS = com.puzzlezapper.wsname-applet-py.gschema.xml
@GSETTINGS_RULES@

#%.gschema.xml.in: %.gschema.xml.in.in Makefile
#	$(AM_V_GEN) $(SED) -e 's^\@GETTEXT_PACKAGE\@^$(GETTEXT_PACKAGE)^g' < $< > $@



#@INTLTOOL_SERVER_RULE@


bin_SCRIPTS = wsname_applet.py

wsnameletdir = $(pythondir)/wsnamelet
wsnamelet_PYTHON = 		\
	wsnamelet_globals.py    \
	aligned_window.py       \
        __init__.py


pixmapsdir = $(datadir)/pixmaps
pixmaps_DATA = wsnamelet.png

DISTCLEANFILES =                \
	$(server_DATA)	        \
        intltool-extract        \
        intltool-merge          \
        intltool-update         \
        po/Makefile.in          \
        po/.intltool-merge-cache



EXTRA_DIST =  			\
	$(pixmaps_DATA)		\
        intltool-update.in      \
        intltool-extract.in     \
        intltool-merge.in       \
	org.mate.panel.WsnameApplet.mate-panel-applet.in.in \
	$(service_in_files) \
	com.puzzlezapper.wsname-applet-py.gschema.xml \
        po/Makefile.in.in \
	po/POTFILES.in \
	$(wsnamelet_PYTHON)


CLEANFILES = $(applet_DATA) $(service_DATA) *.gschema.valid wsnamelet_globals.py
