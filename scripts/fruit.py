def addFruit(cont):
    own = cont.owner
    if cont.sensors["collide"].positive:
        own.scene.objects["Player"]["fruits"] += 1
        own.endObject()
