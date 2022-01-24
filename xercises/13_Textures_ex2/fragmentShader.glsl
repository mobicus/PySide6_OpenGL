#version 330 core

in vec4 vertexColor;
in vec2 texCoords;

out vec4 FragColor;

uniform sampler2D vTexture1;
uniform sampler2D vTexture2;

void main()
{
    FragColor = mix( texture( vTexture1, texCoords ), texture( vTexture2, vec2(1.0 - texCoords.x, texCoords.y) ), 0.2 );
}