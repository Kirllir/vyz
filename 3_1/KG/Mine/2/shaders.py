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