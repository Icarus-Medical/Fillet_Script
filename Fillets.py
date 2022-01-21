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


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
