#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
from . import csvReader as cr
from . import planeManager as Pl
from . import splineDrawer as Foil

thickness = 1.0

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootcomp = design.rootComponent
        lst = cr.csvReader.Reader()
        check = cr.csvReader.FileFormatCertification(lst)
        if check == False:
            ui.messageBox('Wrong csv file!')
            exit()
        del lst[0]
        #ui.messageBox(format(mess)) ←消すな！messagebox の使い方
        for ii in range(len(lst)):
            name = lst[ii][0]
            chordinate = []
            for jj in range(3):
               chordinate.append(float(lst[ii][jj + 1]))
            chord = lst[ii][4]
            attack = lst[ii][5]
            #Pl.plane_tools.plane_builder(chordinate[0])
            sketchPlane = Pl.plane_tools.plane_builder(chordinate[0])
            sketch = Foil.Airfoil.Execute(name,sketchPlane,chordinate,chord,attack)
            Pl.plane_tools.extruder(sketch,thickness)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
