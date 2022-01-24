#version 330 core

in vec4 vertexColor;
in vec2 texCoords;

out vec4 FragColor;

uniform float mixRatio;
uniform sampler2D vTexture1;
uniform sampler2D vTexture2;

void main()
{
    FragColor = mix( texture( vTexture1, texCoords ), texture( vTexture2, texCoords ), mixRatio );
}