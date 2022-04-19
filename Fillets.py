#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        def create_fillet(body, radius, upLimit, loLimit):
            '''
            body is the body to be filleted by checking edge lengths (string)
            radius is the fillet radius (string)
            upLimit is the upper limit of edge length (float)
            loLimit is lowee limit of edge length (float)
            this method searches a body for edge length between certain length. those edges are then filleted to the radius
            '''
            app = adsk.core.Application.get()
            ui  = app.userInterface
            des = app.activeProduct
            root = des.rootComponent
            fillets = root.features.filletFeatures

            edgeCollection = adsk.core.ObjectCollection.create()
            frame = root.bRepBodies.itemByName(body)

            for face in frame.faces:
                for edge in face.edges:
                    if edge.length > loLimit and edge.length < upLimit:
                        edgeCollection.add(edge)

            radius_input = adsk.core.ValueInput.createByString(radius)
            finput = fillets.createInput()
            finput.addConstantRadiusEdgeSet(edgeCollection, radius_input, True) 
            finput.isG2 = False
            finput.isRollingBallCorner = True

            return fillets.add(finput)

        #create_fillet('top_frame', "0.04 in", .3, .3)
        #create_fillet('bottom_frame', "0.01 in", .31, .3)


        create_fillet('top_frame', "0.04 in", 3.75, 3.5)
        create_fillet('bottom_frame', "0.04 in", 3.75, 3.5)

        des = app.activeProduct
        root = des.rootComponent
        fillets = root.features.filletFeatures

        bframe = root.bRepBodies.itemByName("bottom_frame")

        bip1 = root.sketches.itemByName("BIP-14")
        bip2 = root.sketches.itemByName("BIP-24")

        circle1 = bip1.sketchCurves.sketchCircles.item(0).centerSketchPoint
        circle2= bip2.sketchCurves.sketchCircles.item(0).centerSketchPoint

        circle1box = circle1.worldGeometry
        circle2box = circle2.worldGeometry

        circle1x=circle1box.x
        circle1y=circle1box.y
        circle1z=circle1box.z
        circle2x=circle2box.x
        circle2y=circle2box.y
        circle2z=circle2box.z

        c1xp = circle1x + .7
        c1xn = circle1x -.7
        c1yp = circle1y +.7
        c1yn = circle1y -.7
        c1zp = circle1z +.4
        c1zn = circle1z -.4
        c2xp = circle2x + .7
        c2xn = circle2x -.7
        c2yp = circle2y +.7
        c2yn = circle2y -.7
        c2zp = circle2z +.4
        c2zn = circle2z -.4
        fillet_edge = adsk.core.ObjectCollection.create()

        
        for face in bframe.faces:
            for edge in face.edges:
                if  c1xn < edge.startVertex.geometry.x < c1xp:
                    if c1yn < edge.startVertex.geometry.y < c1yp:
                        if c1zn < edge.startVertex.geometry.z < c1zp:
                            if .25 < edge.length < .4:
                                fillet_edge.add(edge)
                            elif .57 < edge.length < .67:
                                fillet_edge.add(edge)
                            elif .85 < edge.length < 1:
                                fillet_edge.add(edge)
        for face in bframe.faces:
            for edge in face.edges:
                if  c2xn < edge.startVertex.geometry.x < c2xp:
                    if c2yn < edge.startVertex.geometry.y < c2yp:
                        if c2zn < edge.startVertex.geometry.z < c2zp:
                            if .25 < edge.length < .4:
                                fillet_edge.add(edge)
                            elif .57 < edge.length < .67:
                                fillet_edge.add(edge)
                            elif .85 < edge.length < 1:
                                fillet_edge.add(edge)


        radius_input = adsk.core.ValueInput.createByString(".01 in")
        finput = fillets.createInput()
        finput.addConstantRadiusEdgeSet(fillet_edge,radius_input, True)
        finput.isG2 = False
        finput.isRollingBallCorner = True
        fillets.add(finput)


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

