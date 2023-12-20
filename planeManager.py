import adsk.core, adsk.fusion, traceback

handlers = []
ui = None
app = adsk.core.Application.get()
if app:
    ui  = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
rootComp = design.rootComponent
planes = rootComp.constructionPlanes

class plane_tools:

    def plane_builder(dist):     
        try:           #offset平面の生成（一枚分）
           distance = adsk.core.ValueInput.createByReal(dist)
           yzplane = rootComp.yZConstructionPlane
           planeInput = planes.createInput()
           planeInput.setByOffset(yzplane, distance)
           PlaneOne = planes.add(planeInput)
           return PlaneOne
        except:
            if ui:
               ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
    
    def createNewComponent(app):
    # Get the active design.
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent
        allOccs = rootComp.occurrences
        newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
        return newOcc.component
    
    def extruder(prof,thickness):
        newcomp = plane_tools.createNewComponent(app)
        dist = adsk.core.ValueInput.createByReal(thickness)
        extrudes = newcomp.features.extrudeFeatures
        operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        ext = extrudes.addSimple(prof,dist,operation)
