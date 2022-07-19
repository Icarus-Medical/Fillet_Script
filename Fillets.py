#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    app = adsk.core.Application.get()
    ui  = app.userInterface
    des = app.activeProduct
    root = des.rootComponent
    occ = root.occurrences.itemByName('LOGO:1')

    body1 = root.bRepBodies.item(0)
    body2 = root.bRepBodies.item(1)

    if body1.volume > body2.volume:
        tframe = body1
        bframe = body2
    else:
        tframe = body2
        bframe = body1



    strap_slots = adsk.core.ObjectCollection.create()

    icarus = occ.component.bRepBodies.itemByName('I')
    iCent = icarus.faces.item(0).centroid

    for face in tframe.faces:
        if 50<face.area<70:
            if face.centroid.x < 0:
                leftPipe = face
            else:
                rightPipe = face
        elif face.area > 350:
            tframeFace = face
        elif 3.75<face.area<5.5:
            strap_slots.add(face)

    for slotFace in strap_slots:
        if slotFace.centroid.x < 0 and 6<slotFace.centroid.z < 9 and slotFace.centroid.y < iCent.y:
            frontLeftSlot = slotFace
        elif slotFace.centroid.x > 0 and 6<slotFace.centroid.z < 9 and slotFace.centroid.y < iCent.y:
            frontRightSlot = slotFace


    for bface in bframe.faces:
        if 10<bface.area<15:
            if bface.centroid.x < 0 and bface.centroid.z > -5:
                leftElastic = bface
            elif bface.centroid.x > 0 and bface.centroid.z > -5:
                rightElastic = bface
        elif bface.area > 200:
            bframeFace = bface 
    measurments = adsk.core.ObjectCollection.create()

    frameToLP = app.measureManager.measureMinimumDistance(tframeFace,leftPipe)
    measurments.add(frameToLP)
    frameToRP = app.measureManager.measureMinimumDistance(tframeFace,rightPipe)
    measurments.add(frameToRP)
    FLStoLP = app.measureManager.measureMinimumDistance(leftPipe,frontLeftSlot)
    measurments.add(FLStoLP)
    FRStoRP = app.measureManager.measureMinimumDistance(rightPipe,frontRightSlot)
    measurments.add(FRStoRP)
    bframeToRE = app.measureManager.measureMinimumDistance(bframeFace,rightElastic)
    measurments.add(bframeToRE)
    bframeToLE = app.measureManager.measureMinimumDistance(bframeFace,leftElastic)
    measurments.add(bframeToLE)

    pts = adsk.core.ObjectCollection.create()
    alert = False
    for measure in measurments:
        if measure.value/2.54 < 0.02:
            pts.add(measure.positionOne)
            alert = True


    #add sphere in point of concern if less than 0.02

    #calculate how many strap slots there are 
    strapEdge = adsk.core.ObjectCollection.create()
    for edge in tframe.edges:
        if 3.53 < edge.length < 3.81:
            strapEdge.add(edge)






    tframeMessage = 'Tframe to left pipe path: ' + str(frameToLP.value/2.54) + ' in.' + '\n' + 'Tframe to right pipe path: ' + str(frameToRP.value/2.54) + ' in.' + '\n' + 'Pipe to front left strap: ' + str(FLStoLP.value/2.54) + ' in.' + '\n' + 'Pipe to front right strap: ' + str(FRStoRP.value/2.54) + ' in.'
    bframeMessage = '\n' + 'Bframe to left elastic path: ' + str(bframeToLE.value/2.54) + ' in.' + '\n' + 'Bframe to right elastic path: ' + str(bframeToRE.value/2.54) + ' in.'

    if alert:
        alertMessage = '\n' + '\n' + 'ALERT ALERT ALERT:   SLOPPY MODELING DETECTED' + '\n' + 'ACTION NEEDED ASAPPPPPP'
    else:
        alertMessage = ''


    ui.messageBox(tframeMessage + bframeMessage + alertMessage)

    if alert:
        for sPt in pts:
            temp = sPt.y
            sPt.y = sPt.z
            sPt.z = temp
            sPt.y = -sPt.y
            xzPlane = root.xZConstructionPlane
            sk = root.sketches.add(xzPlane)
            circles = sk.sketchCurves.sketchCircles
            circ = circles.addByCenterRadius(sPt,2.5)
            lines = sk.sketchCurves.sketchLines
            axis = lines.addByTwoPoints(adsk.core.Point3D.create(sPt.x + 2.5,sPt.y,sPt.z), adsk.core.Point3D.create(sPt.x - 2.5,sPt.y,sPt.z))
            prof = sk.profiles.item(0)
            revInput = root.features.revolveFeatures.createInput(prof,axis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            angle = adsk.core.ValueInput.createByReal(2*math.pi)
            revInput.setAngleExtent(False,angle)
            root.features.revolveFeatures.add(revInput)

            num = root.bRepBodies.count
            spBod = root.bRepBodies.item(num-1)

            lib = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
            redPaint = lib.appearances.itemByName('Paint - Enamel Glossy (Red)')
            spBod.appearance = redPaint
            app.activeViewport.refresh()
