#version 330 core

layout (location = 0) in vec3 vPosition; 
layout (location = 1) in vec3 vColor;

uniform float x_offset;
out vec4 vertexColor;

void main()
{
    gl_Position = vec4(vPosition.x + x_offset, vPosition.y * -1 , vPosition.z, 1.0);
    vertexColor = vec4(vColor, 1.0);
}
