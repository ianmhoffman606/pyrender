#version 330 core

in vec3 normalInterp;
in vec3 vertPos;

out vec4 fragColor;

uniform vec3 lightPos;
uniform vec3 viewPos;

uniform vec3 lightAmbient;
uniform vec3 lightDiffuse;
uniform vec3 lightSpecular;


uniform vec3 materialAmbient;
uniform vec3 materialDiffuse;
uniform vec3 materialSpecular;
uniform float shininess;

void main()
{

    vec3 norm = normalize(normalInterp);

    
    vec3 lightDir = normalize(lightPos - vertPos);


    vec3 viewDir = normalize(viewPos - vertPos);


    vec3 halfVector = normalize(lightDir + viewDir);


    vec3 ambient = lightAmbient * materialAmbient;


    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = lightDiffuse * materialDiffuse * diff;


    float spec = pow(max(dot(norm, halfVector), 0.0), shininess);
    vec3 specular = lightSpecular * materialSpecular * spec;
    

    fragColor = vec4(ambient + diffuse + specular, 1.0);
}
