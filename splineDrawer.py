import adsk.core, adsk.fusion, adsk.cam, traceback
from pathlib import Path
import math
ui = None
app = adsk.core.Application.get()
if app:
    ui  = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
class Airfoil:
    def Execute( name,Plane, StartCoordinate,chord,attack):
        coordX = [] # result array for spline
        coordY = [] # result array for spline
        coordX1 = [] # temporary array for Lednicer DAT format
        coordY1 = [] # temporary array for Lednicer DAT format
        coordX2 = [] # temporary array for Lednicer DAT format
        coordY2 = [] # temporary array for Lednicer DAT format
        DATformat = 0 # 1 - Selig, 2 - Lednicer, 0 - undefined
        Lednicer_top = 0
        Lednicer_bottom = 0
        msg = ''       
        ScaleY = chord
        length = float(chord)
        rootComp = design.rootComponent

        
        _fileparent = Path(__file__).resolve().parent
        f = open(_fileparent.joinpath(name),'r')

        root = design.rootComponent
        try:
            entityPlane = Plane
            sketch = root.sketches.add(Plane)
        except RuntimeError:
            ui.messageBox('You should select origin plane or construction plane.', 'Error')
            return

        #normal = sketch.xDirection.crossProduct(sketch.yDirection)
        #normal.transformBy(sketch.transform)
        origin = adsk.core.Point2D.create(0,0)
        # origin = sketch.origin
        #origin.transformBy(sketch.transform)
        rotationMatrix = adsk.core.Matrix2D.create()
        rotationMatrix.setToRotation(math.radians(float(attack)),origin)

            
#        translationMatrix = adsk.core.Matrix3D.create()
#        translationMatrix.translation = adsk.core.Vector3D.create(OffsetX, OffsetY, 0.0)

        points = adsk.core.ObjectCollection.create()

        # Reading first line with airfoil name
        object_name = f.readline()
        object_name = object_name.strip()
        if(len(object_name)==0): object_name = "No_name"
        object_name = object_name.replace(" ", "_")
        object_name = object_name + "_" + str(ScaleY)
        while True:
            try:
                Plane.name = object_name
                break
            except RuntimeError:
                print("Renaming of this type of planes is not supported on this platform...")

        # Reading second line for distinguishing file format
        second_line = f.readline()
        line = second_line.strip(' \t')
        line = line.replace('\t', ' ')
        line = line.replace(',', ' ')
        p1 = line.find(".")
        p2 = line.find(" ")
        p3 = line.rfind(".")
        try:
            x = int(line[0:p1])
        except ValueError:
            ui.messageBox('Wrong file format. Cannot convert first string to number.', 'Error')
            return
        try:
            y = int(line[p2+1:p3])
        except ValueError:
            ui.messageBox('Wrong file format. Cannot convert second string to number.', 'Error')
            return
        #ui.messageBox('Top: {} Bottom: {}' .format(x, y) )
        
        if x > 1:
            # Lednicer DAT format
            DATformat = 2
            Lednicer_top = x
            Lednicer_bottom = y
        #elif x == 1:
            # Selig DAT format
            #DATformat = 1
        else:
            #msg += '\nUnknown DAT format'
            #ui.messageBox(msg, 'Error')
            #return
            DATformat = 1

        # Reading file into array
        if DATformat == 1: # Selig
            while line:
                line = line.strip(' \t')
                line = line.replace('\t', ' ')
                line = line.replace(',', ' ')
                p1 = line.find(" ")
                p2 = line.rfind(" ")
                try:
                    x = float(line[0:p1])
                except ValueError:
                    ui.messageBox('Wrong file format. Cannot convert X coordinate.', 'Error')
                    break
                try:
                    y = float(line[p2+1:])
                except ValueError:
                    ui.messageBox('Wrong file format. Cannot convert Y coordinate.', 'Error')
                    break
                coordX.append(x)
                coordY.append(y)
                # Reading next line with coordinates
                line = f.readline()
            f.close()

        # Reading file into array with following processing
        elif DATformat == 2: # Lednicer

            # Reading empty line without coordinates
            line = f.readline()

            t = 0 # Counter for top lines
            b = 0 # Counter for bottom lines

            while t < Lednicer_top:
                # Reading next line with coordinates
                line = f.readline()
                line = line.strip(' \t')
                line = line.replace('\t', ' ')
                line = line.replace(',', ' ')
                #ui.messageBox(line, 'Debug')
                p1 = line.find(" ")
                p2 = line.rfind(" ")
                try:
                    x = float(line[0:p1])
                except ValueError:
                    ui.messageBox('Wrong file format. Cannot convert X coordinate.', 'Error')
                    break
                try:
                    y = float(line[p2+1:])
                except ValueError:
                    ui.messageBox('Wrong file format. Cannot convert Y coordinate.', 'Error')
                    break
                coordX1.append(x)
                coordY1.append(y)
                t = t + 1
            
            # Reading empty line without coordinates
            line = f.readline()

            for i in range(Lednicer_bottom -1):
                # Reading next line with coordinates
                line = f.readline()
                line = line.strip(' \t')
                line = line.replace('\t', ' ')
                line = line.replace(',', ' ')
                p1 = line.find(" ")
                p2 = line.rfind(" ")
                try:
                    x = float(line[0:p1])
                except ValueError:
                    ui.messageBox('Wrong file format. Cannot convert X coordinate.', 'Error')
                    break
                try:
                    y = float(line[p2+1:])
                except ValueError:
                    ui.messageBox('Wrong file format. Cannot convert Y coordinate.', 'Error')
                    break
                coordX2.append(x)
                coordY2.append(y)
            f.close()

            # Need to join two arrays in correct way
            for i in reversed(range(len(coordX1))):
                coordX.append(coordX1[i])
                coordY.append(coordY1[i])
            for i in range(1, len(coordX2)):
                coordX.append(coordX2[i])
                coordY.append(coordY2[i])
        
        xlist = coordX.copy()
        ylist = coordX.copy()
        zlist = coordX.copy()
        sketchPoints = sketch.sketchPoints
                # YZ plane, normal Y
        for i in range(len(coordX)) :
            xlist[i] = -1*coordY[i] * length            
            ylist[i] = coordX[i] * length + StartCoordinate[1]
        
        points =  adsk.core.ObjectCollection.create()
        for i in range(len(coordX)):
            point = adsk.core.Point2D.create(xlist[i] , ylist[i] )    
            point.transformBy(rotationMatrix)   
            _3point = adsk.core.Point3D.create(point.x,point.y,0)
            points.add(_3point)

        sketch.sketchCurves.sketchFittedSplines.add(points)
              
        sketch.name=object_name
        prof = sketch.profiles.item(0)
        return prof