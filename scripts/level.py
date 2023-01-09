def nextLevel(cont):
    if cont.sensors["next"].positive:
        own = cont.owner
        own.scene.suspend()

        for obj in own.scene.objects:
            if (("level"+str(own["level"])) in obj) or ("del" in obj):
                if obj.parent == None:
                    obj.endObject()
        own["level"] += 1
        for obj in own.scene.objectsInactive:
            if ("level"+str(own["level"])) in obj:
                newObj = own.scene.addObject(obj)
                # hopefully this workey
        own["nextLevel"] = False
        own.scene.objects["Player"]["thisRunFruit"] = 0
        own.scene.resume()


def restartLevel(cont):
    if cont.sensors["restart"].positive:
        own = cont.owner
        own.scene.objects["Player"].suspendPhysics()
        for obj in own.scene.objects:
            if (("level"+str(own["level"])) in obj) or ("del" in obj):
                if obj.parent == None:
                    obj.endObject()
        for obj in own.scene.objectsInactive:
            if ("level"+str(own["level"])) in obj:
                newObj = own.scene.addObject(obj)
                # hopefully this workey
        own["deaths"] += 1
        own.scene.objects["Player"]["health"] = 50
        own.scene.objects["Player"]["fruits"] -= own.scene.objects["Player"]["thisRunFruit"]
        own.scene.objects["Player"]["thisRunFruit"] = 0

        own.scene.objects["Player"].worldLinearVelocity.x = 0
        own.scene.objects["Player"].worldLinearVelocity.y = 0
        own.scene.objects["Player"].worldLinearVelocity.z = 0
        if own["level"] == 1:
            own.scene.objects["Player"].worldPosition.x = 0
            own.scene.objects["Player"].worldPosition.y = 0
            own.scene.objects["Player"].worldPosition.z = 0
        elif own["level"] == 2:
            own.scene.objects["Player"].worldPosition.x = -19.724
            own.scene.objects["Player"].worldPosition.y = 353.455
            own.scene.objects["Player"].worldPosition.z = 12.0346
        elif own["level"] == 3:
            own.scene.objects["Player"].worldPosition.x = -19.724
            own.scene.objects["Player"].worldPosition.y = 624.08
            own.scene.objects["Player"].worldPosition.z = 12.0346
        own.scene.objects["Player"]["resetTimer"] = 0
