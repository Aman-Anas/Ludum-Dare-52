from mathutils import Vector

def main(cont):
    own = cont.owner
    scene = own.scene
    obj = scene.objects["Cube"]
    
    # First choose the alignment vector
    # add a negative before the whole thing to get
    # -x, -y, or -z
    axis = Vector((0,0,1))
    alignAxisTo(own, obj, axis, 0.1)
    
    
    
    
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