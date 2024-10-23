
import glfw
import OpenGL.GL as gl
import numpy as np

# Vertex shader - position only
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec3 position;
void main() {
    gl_Position = vec4(position, 1.0);
}
"""

# Fragment shaders - one for each color
RED_FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red
}
"""

GREEN_FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.0, 1.0, 0.0, 1.0);  // Green
}
"""

BLUE_FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.0, 0.0, 1.0, 1.0);  // Blue
}
"""

def compile_shader(shader_type, source):
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)
    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        raise RuntimeError(gl.glGetShaderInfoLog(shader))
    return shader

def create_shader_program(vertex_shader_source, fragment_shader_source):
    vertex_shader = compile_shader(gl.GL_VERTEX_SHADER, vertex_shader_source)
    fragment_shader = compile_shader(gl.GL_FRAGMENT_SHADER, fragment_shader_source)
    
    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)
    gl.glLinkProgram(program)
    
    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        raise RuntimeError(gl.glGetProgramInfoLog(program))
    
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)
    
    return program

def main():
    # Initialize GLFW

    
    if not glfw.init():
        return
    
    # Configure GLFW
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    # Create window
    window = glfw.create_window(800, 600, "Three Triangles", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    init_opengl()
    
    # Create shader programs
    shader_programs = [
        create_shader_program(VERTEX_SHADER, RED_FRAGMENT_SHADER),
        create_shader_program(VERTEX_SHADER, GREEN_FRAGMENT_SHADER),
        create_shader_program(VERTEX_SHADER, BLUE_FRAGMENT_SHADER)
    ]
    
    # Triangle vertices
    triangles = [
        # Left triangle
        np.array([
            -0.8, -0.5, 0.0,
            -0.4, -0.5, 0.0,
            -0.6,  0.5, 0.0
        ], dtype=np.float32),
        # Middle triangle
        np.array([
            -0.2, -0.5, 0.0,
            0.2, -0.5, 0.0,
            0.0,  0.5, 0.0
        ], dtype=np.float32),
        # Right triangle
        np.array([
            0.4, -0.5, 0.0,
            0.8, -0.5, 0.0,
            0.6,  0.5, 0.0
        ], dtype=np.float32)
    ]
    
    # Create VAOs and VBOs
    vaos = gl.glGenVertexArrays(3)
    vbos = gl.glGenBuffers(3)
    
    for i in range(3):
        gl.glBindVertexArray(vaos[i])
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbos[i])
        gl.glBufferData(gl.GL_ARRAY_BUFFER, triangles[i].nbytes, triangles[i], gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        gl.glEnableVertexAttribArray(0)
    
    # Main loop
    while not glfw.window_should_close(window):
        # Clear the screen
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        # Draw each triangle with its respective shader
        for i in range(3):
            gl.glUseProgram(shader_programs[i])
            gl.glBindVertexArray(vaos[i])
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        
        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # Cleanup
    for vao in vaos:
        gl.glDeleteVertexArrays(1, [vao])
    for vbo in vbos:
        gl.glDeleteBuffers(1, [vbo])
    for program in shader_programs:
        gl.glDeleteProgram(program)
    
    glfw.terminate()

def init_opengl():
    # Get OpenGL version info
    version = gl.glGetString(gl.GL_VERSION)
    print(f"OpenGL Version: {version.decode('utf-8')}")
    
    # Get GLSL version info
    glsl_version = gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
    print(f"GLSL Version: {glsl_version.decode('utf-8')}")
    
    # Get GPU vendor and renderer
    vendor = gl.glGetString(gl.GL_VENDOR)
    renderer = gl.glGetString(gl.GL_RENDERER)
    print(f"Vendor: {vendor.decode('utf-8')}")
    print(f"Renderer: {renderer.decode('utf-8')}")

if __name__ == "__main__":
    main()