def next(cont):
    if cont.sensors["next"].positive:
        own = cont.owner
        own.scene.suspend()

        for obj in own.scene.objects:
            if ("level"+str(own["level"])) in obj:
                if obj.parent == None:
                    obj.endObject()
        own["level"] += 1
        for obj in own.scene.objectsInactive:
            if ("level"+str(own["level"])) in obj:
                newObj = own.scene.addObject(obj)
                # hopefully this workey
        own["nextLevel"] = False
        own.scene.resume()