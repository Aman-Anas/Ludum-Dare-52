from mathutils import Vector


def main(cont):
    own = cont.owner
    w = cont.sensors["w"]
    a = cont.sensors["a"]
    s = cont.sensors["s"]
    d = cont.sensors["d"]

    up = cont.sensors["up"]
    down = cont.sensors["down"]
    left = cont.sensors["left"]
    right = cont.sensors["right"]

    space = cont.sensors["space"]

    wPos = w.positive or up.positive
    aPos = a.positive or left.positive
    sPos = s.positive or down.positive
    dPos = d.positive or right.positive

    maxSpeed = own["maxSpeed"]

    if wPos or sPos:
        if wPos:
            if (own["yDisp"] < own["maxSpeed"]):
                own["yDisp"] += own["accel"]
        if sPos:
            if (own["yDisp"] > -own["maxSpeed"]):
                own["yDisp"] -= own["accel"]
    else:
        own["yDisp"] = 0

    if dPos or aPos:
        if dPos:
            if (own["xDisp"] < own["maxSpeed"]):
                own["xDisp"] += own["accel"]
        if aPos:
            if (own["xDisp"] > -own["maxSpeed"]):
                own["xDisp"] -= own["accel"]
    else:
        own["xDisp"] = 0

    own.localLinearVelocity.y = own["yDisp"]
    own.localLinearVelocity.x = own["xDisp"]

    if cont.sensors["floor"].positive:
        own["touchGround"] = True
    else:
        own["touchGround"] = False

    if (own["touchGround"] and space.positive):
        own.localLinearVelocity.z = own["jumpVel"]

    turn = own.scene.objects["turnTar"]
    turnRot = turn.worldOrientation.to_euler()
    turnRot.z = own.scene.objects["CameraTar"].worldOrientation.to_euler().z
    turn.worldOrientation = turnRot

    if wPos or aPos or dPos or sPos:
        alignAxisTo(
            own, own.scene.objects["forwardTar"], Vector((0, 1, 0)), 0.2)
        own["running"] = True
    else:
        own["running"] = False

    # animation control
    if own["running"]:
        cont.deactivate(cont.actuators["stand"])
        cont.activate(cont.actuators["run"])
        own.scene.objects["EmitterRun"]["emit"] = True
        cont.activate(cont.actuators["runSFX"])

    else:
        cont.activate(cont.actuators["stand"])
        cont.deactivate(cont.actuators["run"])
        own.scene.objects["EmitterRun"]["emit"] = False
        cont.deactivate(cont.actuators["runSFX"])

    leftClick = cont.sensors["LeftClick"]

    if own["weapon"] == "bonk":
        own.scene.objects["bonkstick"].visible = True
        own.scene.objects["bonkstick"].restorePhysics()
    else:
        own.scene.objects["bonkstick"].visible = False
        own.scene.objects["bonkstick"].suspendPhysics()

    if own["weapon"] == "shooter":
        own.scene.objects["enemyShooter"].visible = True
    else:
        own.scene.objects["enemyShooter"].visible = False
    if leftClick.positive:
        # cont.activate(cont.actuators["attack"])
        if own["weapon"] == "bonk":
            cont.activate(cont.actuators["bonk"])

        if own["weapon"] == "shooter":

            if own["farmers"] > 0:
                own.scene.addObject(
                    "farmer", own.scene.objects["enemyShooter"], 1200)
                own["farmers"] -= 1

    else:
        cont.deactivate(cont.actuators["bonk"])

    if own.getDistanceTo(own.scene.objects["food"]) > 14:
        own.scene.objects["food"].worldPosition = own.worldPosition + \
            Vector((0, 0, 2))

    if cont.sensors["T"].positive:
        if own["weapon"] == "bonk":
            own["weapon"] = "shooter"
        else:
            own["weapon"] = "bonk"

    if cont.sensors["hurt"].positive:
        own["health"] -= 10

    if cont.sensors["warp"].positive:
        own.scene.objects["Camera"]["nextLevel"] = True


def alignAxisTo(own, obj, axis, rate):

    alignVec = axis

    # Now get the world vector to the other object
    objVec = own.getVectTo(obj)[1]

    # Get the quaternion difference
    difference = alignVec.rotation_difference(objVec)

    # Interpolate
    rotate = own.worldOrientation.to_quaternion().slerp(difference, rate)

    # Apply the rotation
    own.worldOrientation = rotate.to_matrix()
