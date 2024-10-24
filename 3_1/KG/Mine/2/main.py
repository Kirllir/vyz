import time
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import numpy as np

class OpenGLShapes:
    def __init__(self):
        self.n = 8
        self.current_task = 1
        self.shading_mode = 'flat'
        self.face_mode = 'normal'
        self.triangle_mode = 'triangle_fan'
        self.window = None
        
    def init_glfw(self):
        if not glfw.init():
            raise Exception("GLFW initialization failed")
            
        glfw.window_hint(glfw.SAMPLES, 4)
        self.window = glfw.create_window(800, 600, "OpenGL Shapes", None, None)
        
        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")
            
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)
        
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glEnable(GL_MULTISAMPLE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
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
            elif key == glfw.KEY_F and self.current_task == 8:
                modes = ['normal', 'vertices_front', 'filled_front_wire_back', 'wireframe']
                self.face_mode = modes[(modes.index(self.face_mode) + 1) % 4]
            elif key == glfw.KEY_RIGHT and self.current_task == 5:
                modes = ['triangles', 'triangle_strip', 'triangle_fan']
                self.triangle_mode = modes[(modes.index(self.triangle_mode) + 1) % 3]
            elif key == glfw.KEY_S:
                self.shading_mode = 'smooth' if self.shading_mode == 'flat' else 'flat'
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)

    def draw_n_gon_points(self):
        glPointSize(10.0)
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

    def draw_figure1(self):
        glBegin(GL_LINE_STRIP)
        vertices = [
            (-1.8, -0.5), (-1.2, 1), (-0.9, -1.8),
            (-0.9, 0.4), (0, 0.4), (0, 1), (2, -1)
        ]
        for vertex in vertices:
            glVertex2f(*vertex)
        glEnd()

    def draw_figure2(self):
        glBegin(GL_LINE_LOOP)
        vertices = [
            (-2, -1), (-1.2, 1.5), (1, 2), (0.5, 1), (2, 1.3), (2, 0.3), (0.5, 0.3), (0.5, -1.4), (-0.7, 0.3)
        ]
        for vertex in vertices:
            glVertex2f(*vertex)
        glEnd()

    def draw_figure2_triangles(self, primitive_type):
        # Set shading mode
        if self.shading_mode == 'flat':
            glShadeModel(GL_FLAT)
        else:
            glShadeModel(GL_SMOOTH)

        if primitive_type == 'triangles':
            print("Drawing individual triangles")
            vertices = [
                (-2, -1), (-1.2, 1.5), (1, 2),
                (0.16, 1.16), (-0.7, 0.3), (2, 0.3),
                (0.5, 1), (2, 1.3), (2, 0.3),
                (0.16, 1.16), (1, 2), (0.5, 1),
                (0.5, 0.3), (0.5, -1.4), (-0.7, 0.3)
            ]
            
            glBegin(GL_TRIANGLES)
            for i in range(0, len(vertices), 3):
                color = (random.random(), random.random(), random.random())
                for j in range(3):
                    glColor3f(*color)
                    glVertex2f(*vertices[i+j])
            glEnd()

        elif primitive_type == 'triangle_strip':
            print("Drawing triangle strip")
            strip1 = [
                (-2, -1),
                (-1.2, 1.5), 
                (-0.7, 0.3),
                (1, 2),
                (-1, 0.6),
                (0.5, 1),    
            ]

            strip2 = [
                (2, 1.3),   
                (2, 0.3),   
                (-0.5, 0.8),
                (-1, 0.3), 
            ]

            strip3 = [
               (-0.7, 0.3),
               (0.5, -1.4),
               (0.5, 0.3),
            ]

            def draw_strip(vertices):
                glBegin(GL_TRIANGLE_STRIP)
                for vertex in vertices:
                    if self.shading_mode == 'smooth':
                        glColor3f(random.random(), random.random(), random.random())
                    else:
                        # For flat shading, color entire primitive
                        if vertices.index(vertex) % 2 == 0:
                            glColor3f(random.random(), random.random(), random.random())
                    glVertex2f(*vertex)
                glEnd()

            draw_strip(strip1)
            draw_strip(strip2)
            draw_strip(strip3)

        elif primitive_type == 'triangle_fan':
            print("Drawing triangle fan")
            fans = [
                {   
                    'center': (-0.7, 0.3),
                    'vertices': [
                        (-2, -1),
                        (-1.2, 1.5)
                    ]
                },
                {   
                    'center': (-1.2, 1.5),
                    'vertices': [
                        (-0.7, 0.3),
                        (1, 2)
                    ]
                },
                {   # Fan 3 (Triangle C)
                    'center': (-0.7, 0.3),
                    'vertices': [
                        (1, 2),
                        (-1, 0.6)
                    ]
                },
                {   
                    'center': (-1, 0.6),
                    'vertices': [
                        (1, 2),
                        (0.5, 1)
                    ]
                },
                {   
                    'center': (-0.5, 0.8),
                    'vertices': [
                        (2, 1.3),
                        (2, 0.3),
                        (-1, 0.3)
                    ]
                },
                {   
                    'center': (-0.7, 0.3),
                    'vertices': [
                        (0.5, -1.4),
                        (0.5, 0.3)
                    ]
                }
            ]

            def draw_fan(center, vertices):
                glBegin(GL_TRIANGLE_FAN)
                # Draw center point
                if not self.shading_mode == 'smooth':
                    glColor3f(random.random(), random.random(), random.random())
                glVertex2f(*center)

                for vertex in vertices:
                    if self.shading_mode == 'smooth':
                        glColor3f(random.random(), random.random(), random.random())
                    glVertex2f(*vertex)
                glEnd()

            for fan in fans:
                draw_fan(fan['center'], fan['vertices'])

    def draw_figure3(self):
        triangles = [
        [(-1.5, -1.5), (-1.0, -0.5), (-0.5, -1.6)],
        [(-0.71, -1.15), (-0.5, -1.6), (0.5, -1.7)],
        [(0.5, -1.7), (-0.71, -1.15), (0.7, -1.15)],
        [(0.0, -1.15), (0.25, 0.52), (0.7, -1.15)],
        [(0.7, -1.15), (0.25, 0.52), (1.2, 0.42)],
        [(0.0, -1.15), (0.25, 0.52), (-0.5, 0.6)],
        [(-1.5, -0.5), (-0.5, 0.6), (-0.5, -0.5)],
        [(-1.5, -0.5), (-1.5, 0.7), (-0.5, 0.6)],
        [(-1.5, 0.7), (1.2, 0.42), (-1.5, 0.9)],
        [(-1.5, 0.9), (1.2, 0.42), (1.25, 0.6)]
    ]

        if self.face_mode == 'normal':
            # Normal mode: all faces filled
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
            glBegin(GL_TRIANGLES)
            for triangle in triangles:
                glColor3f(random.random(), random.random(), random.random())
                for vertex in triangle:
                    glVertex2f(*vertex)
            glEnd()
            
            glDisable(GL_CULL_FACE)

        elif self.face_mode == 'vertices_front':
            # Mode A: front faces as vertices only
            glEnable(GL_CULL_FACE)
            
            # Draw front faces (vertices only)
            glCullFace(GL_BACK)
            glPolygonMode(GL_FRONT, GL_POINT)
            glPointSize(5.0)  # Make vertices more visible
            
            glBegin(GL_TRIANGLES)
            for triangle in triangles:
                glColor3f(random.random(), random.random(), random.random())
                for vertex in triangle:
                    glVertex2f(*vertex)
            glEnd()
            
            glDisable(GL_CULL_FACE)

        elif self.face_mode == 'filled_front_wire_back':
            # Mode B: front faces filled, back faces as wireframe
            
            # First draw back faces as wireframe
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)
            glPolygonMode(GL_BACK, GL_LINE)
            glLineWidth(1.0)
            
            glBegin(GL_TRIANGLES)
            for triangle in triangles:
                glColor3f(0.5, 0.5, 0.5)  # Grey color for back faces
                for vertex in triangle:
                    glVertex2f(*vertex)
            glEnd()
            
            # Then draw front faces filled
            glCullFace(GL_BACK)
            glPolygonMode(GL_FRONT, GL_FILL)
            
            glBegin(GL_TRIANGLES)
            for triangle in triangles:
                glColor3f(random.random(), random.random(), random.random())
                for vertex in triangle:
                    glVertex2f(*vertex)
            glEnd()
            
            glDisable(GL_CULL_FACE)

        else: 
            # Mode C: all faces as wireframe
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(1.0)
            
            glBegin(GL_TRIANGLES)
            for triangle in triangles:
                glColor3f(random.random(), random.random(), random.random())
                for vertex in triangle:
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
        
            
        if self.current_task == 1:
            self.draw_n_gon_points()
        elif self.current_task == 2:
            self.draw_n_gon_lines()
        elif self.current_task == 3:
            self.draw_figure1()
        elif self.current_task == 4:
            self.draw_figure2()
        elif self.current_task == 5:
            self.draw_figure2_triangles(self.triangle_mode)
        elif self.current_task == 6:
            self.draw_n_gon_fan()
        elif self.current_task == 7 or self.current_task == 8:
            self.draw_figure3()

    def main(self):
        self.init_glfw()

        
        fps = 30
        frame_duration = 1.0 / fps
        
        while not glfw.window_should_close(self.window):
            start_time = time.time()
            
            self.display()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
            elapsed_time = time.time() - start_time
            sleep_time = frame_duration - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        while not glfw.window_should_close(self.window):
            self.display()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
        glfw.terminate()

if __name__ == "__main__":
    app = OpenGLShapes()
    app.main()