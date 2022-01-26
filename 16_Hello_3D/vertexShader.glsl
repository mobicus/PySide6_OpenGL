#version 330 core

layout (location = 0) in vec3 vPosition; 
layout (location = 1) in vec3 vColor;
layout (location = 2) in vec2 vTexCoord;

out vec4 vertexColor;
out vec2 texCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(vPosition, 1.0);
    vertexColor = vec4(vColor, 0.0);
    texCoords = vTexCoord;
}



