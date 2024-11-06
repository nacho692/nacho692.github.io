---
layout: post
title:  "Making Waves! - Rotación RGB"
date:   2024-09-09 01:00:13 -0300
categories: shaders
tags: shaders "ecuaciones diferenciales"
---

Hace poco me incribí en el curso de [_La génesis digital de las formas_][genesis-digital] de [Sol Sarratea][sol-sarratea]. Las primeras horas de presentación me maravillaron con un mundo matemático completamente desconocido y me mostró otra perspectiva con la que entender las cosas.

La idea de _Making Waves!_ (Haciendo Olas) es compartir el camino por el que pasé explicando con cierto detalle el trasfondo matemático, desde filtros básicos en imágenes hasta efectos de ondas dados por ecuaciones diferenciales.

Este artícul es una introducción a los conceptos que voy a estar explicando a lo largo de los artículos 
Siguiente: [Making Waves! Desenfoque gaussiano]({% post_url 2024-09-17-making-waves-gaussian %})

## Shaders

Internet está llena de explicaciones del concepto de shader mucho mejores de lo que puedo desarrollar. 
En términos simples un shader es un algoritmo que corre en la GPU y determina como se van a terminar visualizando la pantalla. Hacen calculos para iluminación, sombras y efectos. Hay muchos tipos de shaders, algunos trabajan con objetos 3d (*Vertex Shaders*), otros con geometrías (*Geometry Shaders*) y, sobre los que se vá a enfocar el artículo, shaders que trabajan sobre píxeles (*Fragment Shaders*).

Un shader de píxeles ejecuta una vez por cada pixel que forma parte de una textura y tiene como resultado un vector que indica el color de ese pixel. Para poder ejecutar de manera paralela se prohibe saber el estado de la ejecución del shader para los ótros píxeles, es decir, no se comparte información.
A alto nivel, un shader funciona de la siguiente manera:

{% highlight python %}
# texture es la textura base a modificar
# new_texture es la salida 
def apply_shader(shader, texture):
    for (x,y) in texture.range():
        new_texture[x][y] = shader(texture, (x,y))

    return new_texture
{% endhighlight %}

Si se está procesando un video, un juego o algo que requiera actualizaciones constantes visuales, se suele ejecutar el shader una vez por frame, por lo que tiene que ser una operación rápida.

## Rotación RGB

Un píxel es un vector de 4 dimensiones: (r,g,b,a) con valores entre 0 y 1. 
Tomando el pixel entrante, podemos devolver un pixel con los valores rgb rotados:

`(r,g,b,a) -> (g,b,r,a)` 

<table style="text-align: center">
<colgroup>
<col width="50%" />
<col width="50%" />
</colgroup>
<tbody>
<tr>
<td markdown="span">![Base]({{site.baseurl}}/assets/making-waves/base.png)</td>
<td markdown="span">![RGBRotation]({{site.baseurl}}/assets/making-waves/rotation.png)</td>
</tr>
<tr>
<td markdown="span">*Imagen Base*</td>
<td markdown="span">*Rotación RGB*</td>
</tr>
</tbody>
</table>


A continuación se puede ver una implementación del shader de rotación RGB en GLSL, un lenguaje de shading similar a C definido por OpenGL.

{% highlight glsl %}
// Rotacion RGB: Ejemplo de shader en glsl

// textura base sobre la que se trabaja, constante para todos los pixeles
uniform sampler2D baseTex;
// coordenadas del pixel sobre el que se está ejecutando el shader 
IN vec2 texCoord;

void main()
{
    // texture2D toma el pixel en la posición texCoord de la textura baseTex
    vec4 pixel = texture2D(baseTex, texCoord);
    // la salida, en outColor rota los colores rgb -> gbr y el canal alpha 
    // queda igual
    outColor = vec4(pixel.g, pixel.b, pixel.r, pixel.a);
}
{% endhighlight %}

Los ejemplos clásicos con los que vamos a trabajar son el desenfoque gaussiano, o _gaussian blur_, y la detección de bordes o _laplace filter_.

<table style="text-align: center">
<colgroup>
<col width="33%" />
<col width="33%" />
<col width="33%" />
</colgroup>
<tbody>
<tr>
<td markdown="span">![Base]({{site.baseurl}}/assets/making-waves/base.png)</td>
<td markdown="span">![Desenfoque gaussiano]({{site.baseurl}}/assets/making-waves/blur.png)</td>
<td markdown="span">![Detección de bordes]({{site.baseurl}}/assets/making-waves/edge.png)</td>
</tr>
<tr>
<td markdown="span">*Imagen Base*</td>
<td markdown="span">*Desenfoque gaussiano*</td>
<td markdown="span">*Detección de bordes*</td>
</tr>
</tbody>
</table>

En [CustomFilters][cables-custom-filters] se puede ver una implementación simple de estos tres shaders sobre la plataforma [cables.gl][cables-gl].
Esta plataforma permite computar shaders sin instalar software especial en nuestro sistema y sin necesariamente saber programar.
Para ver las distintas implementaciones hay que abrir el _patch_ en el editor de cables y editar el custom shader.

En los próximos artículos se van a desarrollar los filtros de desenfoque gaussiano, detección de bordes y una introducción a ecuaciones diferenciales.

Siguiente: [Making Waves! Desenfoque gaussiano]({% post_url 2024-09-17-making-waves-gaussian %})

[genesis-digital]: https://genesis-digital.solsarratea.world/clases/dia-1
[sol-sarratea]: https://solsarratea.world/
[cables-custom-filters]: https://cables.gl/p/0tYQZn
[cables-gl]: https://cables.gl/