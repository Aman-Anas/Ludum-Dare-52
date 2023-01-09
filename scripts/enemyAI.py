def run(cont):
    own = cont.owner
    if own.getDistanceTo(own.scene.objects["Player"]) < 85:
        own["move"] = True
    else:
        own["move"] = False

    if own["move"]:

        if own["shootingTimer"] > 0.5:
            
            cont.deactivate(cont.actuators["run"])
            cont.activate(cont.actuators["shootAnim"])
            cont.activate(cont.actuators["shoot"])
            own["shootingTimer"] = 0.0
        else:
            cont.activate(cont.actuators["run"])
            cont.deactivate(cont.actuators["shootAnim"])


def addEnemyBag(cont):
    if cont.sensors["collide"].positive:
        own = cont.owner
        player = own.scene.objects["Player"]
        player["farmers"] += 1


def die(cont):
    if cont.sensors["Collision"].positive:
        own = cont.owner
        cont.activate(cont.actuators["explode"])
        own.scene.objects["Player"]["farmers"] += 1
        own.endObject()
