#!BPY
""" Registration info for Blender menus:
Name: 'X-Plane Object (.obj)...'
Blender: 243
Group: 'Import'
Tooltip: 'Import an X-Plane scenery or cockpit object (.obj)'
"""
__author__ = "Jonathan Harris"
__email__ = "Jonathan Harris, Jonathan Harris <x-plane:marginal*org*uk>"
__url__ = "XPlane2Blender, http://marginal.org.uk/x-planescenery/"
__version__ = "3.09"
__bpydoc__ = """\
This script imports X-Plane v6, v7 and v8 .obj scenery files into Blender.

Limitations:<br>
  * smoke_black and smoke_white X-Plane primitives are ignored.<br>
  * ambient, blend and specular attributes are ignored.<br>
  * Can't work out which faces are partially or wholly transparent.<br>
"""

from XPlaneImport_util import *

#------------------------------------------------------------------------
def file_callback (filename):
    obj=OBJimport(filename)
    try:
        obj.doimport()
    except ParseError, e:
        Window.WaitCursor(0)
        Window.DrawProgressBar(0, 'ERROR')
        if e.type == ParseError.HEADER:
            msg='This is not a valid X-Plane v6, v7 or v8 OBJ file'
        elif e.type == ParseError.PANEL:
            msg='Cannot read cockpit panel texture'
        elif e.type == ParseError.NAME:
            msg='Missing dataref or light name at line %s\n' % obj.lineno
        elif e.type == ParseError.MISC:
            msg='%s at line %s' % (e.value, obj.lineno)
        else:
            thing=ParseError.TEXT[e.type]
            if e.value:
                msg='Expecting a %s, found "%s" at line %s' % (thing, e.value, obj.lineno)
            else:
                msg='Missing %s at line %s' % (thing, obj.lineno)
        print "ERROR:\t%s\n" % msg
        Draw.PupMenu("ERROR%%t|%s" % msg)
        Window.RedrawAll()
        Window.DrawProgressBar(1, 'ERROR')
    obj.file.close()

#------------------------------------------------------------------------
# main routine
#------------------------------------------------------------------------
try:
    for o in Blender.Scene.GetCurrent().objects: o.select(0)
    (datarefs,foo)=getDatarefs()
except IOError, e:
    Window.DrawProgressBar(0, 'ERROR')
    print "ERROR:\t%s\n" % e.strerror
    Draw.PupMenu("ERROR%%t|%s" % e.strerror)
    Window.DrawProgressBar(1, 'ERROR')
else:
    Window.FileSelector(file_callback,"Import OBJ")
