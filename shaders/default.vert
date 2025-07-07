
#version 330

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;


in vec3 in_vert;
in vec3 in_normals;


out vec3 normalInterp;
out vec3 vertPos;

void main() {

    gl_Position = projection * view * model * vec4(in_vert, 1.0);
    vec4 vertPos4 = model * vec4(in_vert, 1.0);
    vertPos = vec3(vertPos4) / vertPos4.w;
    normalInterp = mat3(transpose(inverse(model))) * in_normals;

}
