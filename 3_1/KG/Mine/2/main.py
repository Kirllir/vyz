import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import numpy as np

class OpenGLShapes:
    def __init__(self):
        self.n = 8  # N-gon vertices count
        self.current_task = 1
        self.mode = 'flat'  # Shading mode
        self.face_mode = 'filled'  # Face rendering mode
        self.triangle_mode = 'triangles'  # New attribute for triangle drawing mode
        self.window = None
        
    def init_glfw(self):
        if not glfw.init():
            raise Exception("GLFW initialization failed")
            
        # Create window hint for antialiasing
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(800, 600, "OpenGL Shapes", None, None)
        
        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")
            
        glfw.make_context_current(self.window)
        
        # Set callbacks
        glfw.set_key_callback(self.window, self.key_callback)
        
        # Initialize OpenGL settings
        glEnable(GL_POINT_SMOOTH)  # Enable point smoothing
        glEnable(GL_BLEND)
        glEnable(GL_MULTISAMPLE)  # Enable multisampling for antialiasing
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Set up the viewport and projection
        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key >= glfw.KEY_1 and key <= glfw.KEY_8:
                self.current_task = key - glfw.KEY_1 + 1
            elif key == glfw.KEY_M:
                self.mode = 'flat' if self.mode == 'smooth' else 'smooth'
            elif key == glfw.KEY_F:
                modes = ['filled', 'vertices', 'wireframe']
                self.face_mode = modes[(modes.index(self.face_mode) + 1) % 3]
            elif key == glfw.KEY_RIGHT and self.current_task == 5:
                # Toggle between triangle modes when right arrow is pressed
                modes = ['triangles', 'triangle_strip', 'triangle_fan']
                self.triangle_mode = modes[(modes.index(self.triangle_mode) + 1) % 3]
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)

    def draw_n_gon_points(self):
        glPointSize(10.0)  # Adjustable point size
        glBegin(GL_POINTS)
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = math.cos(angle)
            y = math.sin(angle)
            glVertex2f(x, y)
        glEnd()

    def draw_n_gon_lines(self):
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n
            x = math.cos(angle)
            y = math.sin(angle)
            glVertex2f(x, y)
        glEnd()

    def draw_figure1(self):  # First figure from variant
        glBegin(GL_LINE_STRIP)
        vertices = [
            (-1.8, -0.5), (-1.2, 1), (-0.9, -1.8),
            (-0.9, 0.4), (0, 0.4), (0, 1), (2, -1)
        ]
        for vertex in vertices:
            glVertex2f(*vertex)
        glEnd()

    def draw_figure2(self):  # Second figure from variant
        glBegin(GL_LINE_LOOP)
        vertices = [
            (-2, -1), (-1.2, 1.5), (1, 2), (0.5, 1), (2, 1.3), (2, 0.3), (0.5, 0.3), (0.5, -1.4), (-0.7, 0.3)
        ]
        for vertex in vertices:
            glVertex2f(*vertex)
        glEnd()

    def draw_figure2_triangles(self, primitive_type):
        vertices = [
            # Triangle 1
            (-2, -1), (-1.2, 1.5), (1, 2),
            # Triangle 2 
            (0.16, 1.16), (-0.7, 0.3), (2, 0.3),
            # Triangle 3
            (0.5, 1), (2, 1.3), (2, 0.3),
            # Triangle 4
            (0.16, 1.16), (1, 2), (0.5, 1),
            # Triangle 5
            (0.5, 0.3), (0.5, -1.4), (-0.7, 0.3)
        ]
        
        if primitive_type == 'triangles':
            glBegin(GL_TRIANGLES)
            for i in range(0, len(vertices), 3):
                glColor3f(random.random(), random.random(), random.random())
                for j in range(3):
                    glVertex2f(*vertices[i+j])
        elif primitive_type == 'triangle_strip':
            glBegin(GL_TRIANGLE_STRIP)
            for vertex in vertices:
                glColor3f(random.random(), random.random(), random.random())
                glVertex2f(*vertex)
        elif primitive_type == 'triangle_fan':
            glBegin(GL_TRIANGLE_FAN)
            # Use the first vertex as the center point
            glVertex2f(*vertices[0])
            for vertex in vertices[1:]:
                glColor3f(random.random(), random.random(), random.random())
                glVertex2f(*vertex)
        glEnd()

    def draw_figure3(self):  # Third figure from variant
        vertices = [
            (-1.5, -1.5), (-1, -0.5), (-0.5, -1.6),
            (-0.71, -1.15), (-0.5, -1.6), (0.5, -1.7),
            (-0.71, -1.15), (0.7, -1.15), (0.5, -1.7),
            (0, -1.15), (0.25, 0.5), (0.7, -1.15),
            (0.7, -1.15), (0.25, 0.5), (0.8, 0.42),
            (0, -1.15), (0.25, 0.5), (-0.5, 0.6),
            (-1.5, -0.5), (-0.5, 0.6), (-0.5, -0.5),
            (-1.5, -0.5), (-1.5, 0.7), (-0.5, 0.6),
            (-1.5, 0.6), (0.8, 0.7), (-0.5, 1.5),
        ]
        
        if self.face_mode == 'vertices':
            glPointSize(5.0)
            glBegin(GL_POINTS)
            for vertex in vertices:
                glVertex2f(*vertex)
            glEnd()
        elif self.face_mode == 'filled':
            glBegin(GL_TRIANGLES)
            for i in range(0, len(vertices)-2, 3):
                glColor3f(random.random(), random.random(), random.random())
                for j in range(3):
                    glVertex2f(*vertices[i+j])
            glEnd()
        else:  # wireframe
            glBegin(GL_LINE_LOOP)
            for vertex in vertices:
                glVertex2f(*vertex)
            glEnd()

    def draw_n_gon_fan(self):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)  # Center point
        for i in range(self.n + 1):
            angle = 2 * math.pi * i / self.n
            x = math.cos(angle)
            y = math.sin(angle)
            glColor3f(random.random(), random.random(), random.random())
            glVertex2f(x, y)
        glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        
        if self.mode == 'smooth':
            glShadeModel(GL_SMOOTH)
        else:
            glShadeModel(GL_FLAT)
            
        if self.current_task == 1:
            self.draw_n_gon_points()
        elif self.current_task == 2:
            self.draw_n_gon_lines()
        elif self.current_task == 3:
            self.draw_figure1()
        elif self.current_task == 4:
            self.draw_figure2()
        elif self.current_task == 5:
            self.draw_figure2_triangles(self.triangle_mode)  # Use current triangle mode
        elif self.current_task == 6:
            self.draw_n_gon_fan()
        elif self.current_task == 7 or self.current_task == 8:
            self.draw_figure3()

    def main(self):
        self.init_glfw()
        
        while not glfw.window_should_close(self.window):
            self.display()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
        glfw.terminate()

if __name__ == "__main__":
    app = OpenGLShapes()
    app.main()