# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    #create a plane 
    geometry = THREE.PlaneGeometry.new(2000, 2000)
    geometry.rotateX(- math.pi / 2)

    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.5
    plane = THREE.Mesh.new(geometry, material)
    plane.position.y = -20
    plane.receiveShadow = True
    scene.add(plane)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    my_axiom_system = system(0, 1, "d")

    console.log(my_axiom_system)

    #draw_system((my_axiom_system), THREE.Vector3.new(0,-20,0))
    max_it = 1
    number_trees = 5
    tree_height = 2
    for tree in range(0, number_trees):
        coordinate_string = translate_coordinates(0, max_it, "gh")
        g, h = use_coordinates(coordinate_string)
        my_axiom_system = system(0, tree_height, "d")
        draw_system((my_axiom_system), THREE.Vector3.new(g,-20,h))
        #negative round
        coordinate_string = translate_coordinates(0, max_it, "ik")
        g, h = use_coordinates(coordinate_string)
        my_axiom_system = system(0, tree_height, "d")
        draw_system((my_axiom_system), THREE.Vector3.new(g,-20,h))
        max_it = max_it + 1
        tree_height = tree_height + 1


    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    """ gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'size', 10,100,1)
    param_folder.add(geom1_params, 'x', 2,100,1)
    param_folder.add(geom1_params, 'rotation', 0,180)
    param_folder.open()"""
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# define rules for coordinates for draw_system
def generate_coordinates(symbol):
    if symbol == "g":
        return "gg"
    elif symbol == "h":
        return "hh"
    if symbol == "i":
        return "ii"
    elif symbol == "k":
        return "kk"

def translate_coordinates(current_iteration, max_iterations, axiom):
    current_iteration += 1
    new_axiom = ""
    for symbol in axiom:
        new_axiom += generate_coordinates(symbol)
    if current_iteration >= max_iterations:
        return new_axiom
    else:
        return translate_coordinates(current_iteration, max_iterations, new_axiom)

def use_coordinates(axiom):
    start_g = 0
    start_h = 0
    for symbol in axiom:
        if symbol == "g":
            start_g = start_g + 25
        if symbol == "h":
            start_h = start_h + 10
        if symbol == "i":
            start_g = start_g - 25
        if symbol == "k":
            start_h = start_h - 10
    return start_g, start_h


#-----------------------------------------------------------------------
# Define RULES in a function which takes one SYMBOL and applies rules generation
def generate(symbol):
    if symbol == "d":
        return "abcdfbedfabedfcd"
    elif symbol == "a":
        return "aa"
    elif symbol == "b" or symbol == "c" or symbol == "e" or symbol == "f":
        return symbol
    
# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol
def system(current_iteration, max_iterations, axiom):
    current_iteration += 1
    new_axiom = ""
    for symbol in axiom:
        new_axiom += generate(symbol)
    if current_iteration >= max_iterations:
        return new_axiom
    else:
        return system(current_iteration, max_iterations, new_axiom)

def draw_system(axiom, initial_point):
    #move vec beschreibt wie hoch jede einzelne linie ist 
    move_vec = THREE.Vector3.new(0,15,0)
    old_states = []
    old_move_vecs = []
    lines = []

    for symbol in axiom:
        # zeichnet bzw. speichert anfangs- und endpunkt
        if symbol == "a" or symbol == "d":
            start_point = THREE.Vector3.new(initial_point.x, initial_point.y, initial_point.z)
            #initial_point = initial_point.add(move_vec)
            end_point = THREE.Vector3.new(initial_point.x, initial_point.y, initial_point.z)
            end_point = end_point.add(move_vec)
            line = []
            line.append(start_point)
            line.append(end_point)
            lines.append(line)

            initial_point = end_point

        # b speichert nur 
        elif symbol == "b":
            old_state = THREE.Vector3.new(initial_point.x, initial_point.y, initial_point.z)
            old_move_vec = THREE.Vector3.new(move_vec.x, move_vec.y, move_vec.z)
            old_states.append(old_state)
            old_move_vecs.append(old_move_vec)

        # applies a rotation to move_vec
        elif symbol == "c": 
            move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), math.pi/7)
        # applies a rotation to move_vec
        elif symbol == "e":
            move_vec.applyAxisAngle(THREE.Vector3.new(0,0,1), -math.pi/7)
        
        #verschiebt den Anfangspunkt auf den letzten Stand 
        elif symbol == "f":
            initial_point = THREE.Vector3.new(old_states[-1].x, old_states[-1].y, old_states[-1].z)
            move_vec = THREE.Vector3.new(old_move_vecs[-1].x, old_move_vecs[-1].y, old_move_vecs[-1].z)
            old_states.pop(-1)
            old_move_vecs.pop(-1)

    global scene
    line_material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        console.log(points)

        line_geom.setFromPoints(points)
        vis_line = THREE.Line.new(line_geom, line_material)

        scene.add(vis_line)

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    #controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()