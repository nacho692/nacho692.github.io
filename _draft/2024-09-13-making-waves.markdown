---
layout: post
title:  "Making Waves! - Detección de bordes"
date:   2024-09-09 01:00:13 -0700
categories: shaders
tags: shaders "ecuaciones diferenciales"
---

Hace poco me incribí en el curso de [_La génesis digital de las formas_][genesis-digital] de [Sol Sarratea][sol-sarratea]. Las primeras horas de presentación me maravillaron con un mundo matemático completamente desconocido y me abrió las puertas a ver la realidad de una manera distinta.

La idea de este post es compartir el camino por el que pasé explicando con cierto detalle el trasfondo matemático.

# Detección de bordes

## Detección de bordes

La detección de bordes es una técnica utilizada en procesamiento de imágenes para identificar los límites entre diferentes regiones en una imagen. Esto es útil para tareas como segmentación de objetos, reconocimiento de formas y extracción de características.

El filtro de Laplace es un filtro de convolución que resalta los cambios bruscos en la intensidad de la imagen. Se utiliza para detectar bordes en imágenes con alto contraste.

Dependiendo de la aplicación y los requisitos específicos, se puede elegir el algoritmo más adecuado para la detección de bordes. Es importante experimentar con diferentes técnicas y ajustar los parámetros para obtener los mejores resultados.

En el siguiente código se muestra un ejemplo de cómo aplicar el operador de Sobel para la detección de bordes en una imagen utilizando Python y la biblioteca OpenCV:


## Convolución

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

# Rotación RGB

Un píxel es un vector de 4 dimensiones: (r,g,b,a) con valores entre 0 y 1. 
Tomando el pixel entrante, podemos devolver un pixel con los valores rgb rotados:

`(r,g,b,a) -> (g,b,r,a)` 

|![Base]({{site.baseurl}}/assets/making-waves/base.png)|![RGBRotation]({{site.baseurl}}/assets/making-waves/rotation.png)
|:--:|
| *Imagen Base* |*Rotación RGB* |

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

|![Base]({{site.baseurl}}/assets/making-waves/base.png)|![Desenfoque gaussiano]({{site.baseurl}}/assets/making-waves/blur.png)|![Detección de bordes]({{site.baseurl}}/assets/making-waves/edge.png)|
|:--:|
| *Imagen Base* | *Desenfoque gaussiano* | *Detección de bordes* |

En [CustomFilters][cables-custom-filters] se puede ver una implementación simple de estos tres shaders sobre la plataforma [cables.gl][cables-gl].
Esta plataforma permite computar shaders sin instalar software especial en nuestro sistema y sin necesariamente saber programar.
Para ver las distintas implementaciones hay que abrir el _patch_ en el editor de cables y editar el custom shader.

En los próximos artículos se van a desarrollar los filtros de desenfoque gaussiano, detección de bordes y una introducción a ecuaciones diferenciales.

[genesis-digital]: https://genesis-digital.solsarratea.world/clases/dia-1
[sol-sarratea]: https://solsarratea.world/
[cables-custom-filters]: https://cables.gl/p/0tYQZn
[cables-gl]: https://cables.gl/