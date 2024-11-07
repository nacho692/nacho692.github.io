---
layout: post
title:  "Making Waves! - Ecuaciones diferenciales ordinarias"
date:   2024-11-06 11:15:00 -0300
categories: shaders
tags: shaders "ecuaciones diferenciales"
---


Este es el cuarto artículo de una serie sobre shaders y ecuaciones diferenciales.

Anterior: [Making Waves! Detección de bordes]({% post_url 2024-10-01-making-waves-laplace-filter %})

Hasta este momento todas las transformaciones que venimos aplicando a las imágenes son "estáticas".
Las herramientas que utilizamos van a sernos útiles para generar visualizaciones que cambian a través del tiempo.
En este artículo vamos a hacer una introducción[^1] al concepto de ecuaciones diferenciales y divertirnos un poco con distintas visualizaciones.

[^1]: No tengo un entendimiento super profundo pero me gustaría transmitir aunque sea la intuición que fuí conseguiendo a medida que investigaba e implementaba. 


## Ecuaciones diferenciales

Una ecuación diferencial en el sentido más abstracto es una ecuación en la que se relacionan una o más funciones con sus derivadas.
Un poco más coloquialmente, son ecuaciones cuya solución es una función y suelen ser utiles cuando lo que se quiere modelar es el cambio, generalmente a través del tiempo.

Por ejemplo la ecuación

$$f''(t) = a$$

tiene como solución una función $f$ tal que la segunda derivada sea la constante $a$.
Una manera de resolver esto es integrando:

$$
\begin{align}
    \int f''(t) dt = \int a dt \\
    f'(t) = at + v_0 \label{eq:integration:1} \\
    \int f'(t) = \int at + v_0 dt \\
    f(t) = \frac{at^2}{2} + v_0t + p_0 \label{eq:integration:2} \\
\end{align}
$$


> En el lado izquierdo de las ecuaciónes $\eqref{eq:integration:1}, \eqref{eq:integration:2}$ estamos abusando un poco [del teorema fundamental del cálculo](https://es.wikipedia.org/wiki/Teorema_fundamental_del_c%C3%A1lculo#Primer_teorema_fundamental_del_c%C3%A1lculo), deberíamos definir un rango desde el que integrar.

Integrando surgieron dos constantes sin valor específico, $v_0$ y $p_0$, esto dice que no hay una única solución, hay infinitas funciones que lo cumplen.
Si consideramos un objeto con una aceleración constante $a$, podemos considerar $f'(t)$ y $f(t)$ como la velocidad y posición en el tiempo $t$, y las constantes $v_0$ y $p_0$ son los valores de velocidad y posición que tiene el objeto en tiempo $0$.


<div style="display: flex; justify-content: center;">
{% include making-waves/ode/motion.html %}
</div>
<div style="text-align: right;" >
    <a style="font-size:12px;" 
    href="https://github.com/nacho692/nacho692.github.io/blob/main/_includes/making-waves/ode/motion.html">Código fuente</a>
</div>

Existen tantas funciones solución como velocidades iniciales y posiciones iniciales existen. 
Hay una manera interesante en la que podemos observar como se comporta el sistema para todos los pares $(v_0, p_0)$.
La idea es definir una transformación lineal $T$ tal que $T(v_t, p_t) = (v_{t+1}, p_{t+1})$.
Es decir, dado un estado inicial, $T$ devuelve el paso en el instante siguiente. 
Con un poco de algebra se puede despejar esta fórmula.

$$
\begin{align*}
T(v_t, p_t) &= T(f'(t), f(t)) = (f'(t+1), f(t+1)) \\[10pt]
f'(t+1) &= a(t+1) + f'(0) \\
&= at + a + f'(0) = a + f'(t)\\[10pt]
f(t+1) &= \frac{a(t+1)^2}{2} + f'(0)(t+1) + f(0)\\
&= \frac{at^2}{2} + f'(0)t + f(0) + at + f'(0) + \frac{a}{2} \\
&=f(t) + f'(t) + \frac{a}{2}\\[10pt]

\boxed{T(v_t, p_t)} &= \boxed{(a + v_t, p_t + v_t + \frac{a}{2})}
\end{align*}
$$

Bien, tiene sentido, la velocidad siguiente es la actual sumandole la aceleración inicial.
La posición siguiente es la actual pero sumada la velocidad actual y una parte de la aceleración, que es lo que se agrega por incrementarse la velocidad linealmente en este "paso".
Veamos un ejemplo con $a = 1, v_0 = 1, p_0 = 1$.

<div style="max-width: 100vw; overflow-x:auto; width:100%;" markdown="1">

|$t$| $(v_t, p_t)$ | $T(v_t, p_t)$ | $T(v_t, p_t) - (v_t, p_t)$ |
| $0$ | $(1, 1)$ | $(2, 2.5)$ | $(1, 1.5)$ |
| $1$ | $(2, 2.5)$ | $(3, 5)$ | $(1, 2.5)$ |
| $2$ | $(3, 5.75)$ | $(4, 8.5)$ | $(1, 3.5)$ |
| $3$ | $(4, 11.675)$ | $(5, 13)$ | $(1, 4.5)$ |
| $4$ | $(5, 21.4375)$ | $(6, 18.5)$ | $(1, 5.5)$ |

</div>

<div style="display: flex; justify-content: center;">
{% include making-waves/ode/linear_t.html %}
</div>
<div style="text-align: right;" >
    <a style="font-size:12px;" 
    href="https://github.com/nacho692/nacho692.github.io/blob/main/_includes/making-waves/ode/linear_t.html">Código fuente</a>
</div>

El gráfico anterior muestra como, en base al estado del sistema, dado por $(v_t, p_t)$, podemos calcular el estado siguiente.
Calculando la diferencia entre el estado en $t$ y en $t + 1$ podemos ver gráficamente el camino que toma el sistema, incrementando
la posición cuadráticamente.
Un detalle a considerar es que para el dibujo, los vectores de diferencia están corridos, siendo el origen el estado anterior y no $(0, 0)$.
En vez de graficar un solo camino posible para el sistema, se puede armar una grilla y evaluar todos al mismo tiempo.

<div style="display: flex; justify-content: center;">
{% include making-waves/ode/vector_field.html %}
</div>
<div style="text-align: right;" >
    <a style="font-size:12px;" 
    href="https://github.com/nacho692/nacho692.github.io/blob/main/_includes/making-waves/ode/vector_field.html">Código fuente</a>
</div>

El gráfico anterior muestra, para cada tupla $(v, p)$, a que estado pasa el sistema. 
Éste tipo de modelado se llama campo vectorial, y es interesante para ver la evolución del sistema dado un estado inicial dado.
En otras palabras, para cada $v_0$, $p_0$, podemos ver como evoluciona el sistema a través del tiempo.

Las ecuaciones diferenciales con una sola variable libre, en este caso $t$, se llaman ecuaciones **diferenciales ordinarias (ODE)**.

### Ecuaciones de predador presa

El sistema de ecuaciones de predador presa, o de Lotka-Volterra, modela el comportamiento de dos poblaciones, en donde el crecimiento de una depende de la otra.

$$
\begin{align*}
    \frac{\partial x(t)}{\partial t} &= x(t)(\alpha - \beta y(t))\\
    \frac{\partial y(t)}{\partial t} &= y(t)(\delta x(t) - \gamma)\\
    x(0) &= x_0\\
    y(0) &= y_0
\end{align*}
$$

En donde $x(t), y(t)$ representan la densidad poblacional de la presa y el predador respectivamente en el tiempo 0, $\alpha, \beta$ son coeficientes de crecimiento y muerte de la presa y $\delta, \gamma$ del depredador.
Lo que piden las ecuaciones es que el crecimiento de la poblacion (la derivada), dependa de la poblacion actual y la competencia partiendo de una densidad $x_0, y_0$.

Honestamente no sé resolver esta ecuación diferencial para tener una formula cerrada cómoda para las funciones $x,y$.
¡Lo divertido es que no es necesario!, tenemos los valores iniciales y sabemos como evolucionan las funciones, también tenemos computadoras para hacer muchos calculos, ¿por qué no graficarlo y tratar de entenderlo de esa manera?

Una manera de realizar esto [aproximando linealmente](https://openstax.org/books/c%C3%A1lculo-volumen-1/pages/4-2-aproximaciones-lineales-y-diferenciales) la función mediante la tangente y caminar de a pasitos.

$$
\begin{align*}
    x(t+\epsilon) &\approx x(t) + \epsilon \frac{\partial x(t)}{\partial t} = x(t) + \epsilon x(t)(\alpha - \beta y(t))\\
    y(t+\epsilon) &\approx y(t) + \epsilon \frac{\partial y(t)}{\partial t} = y(t) + \epsilon y(t)(\delta x(t) - \gamma)
\end{align*}
$$

Para graficar se puede separar el eje horizontal del gráfico en pasos de tamaño $\epsilon$ y calcular paso por paso tanto el valor de $x$ como el de $y$.[^2]

[^2]: Depende de la función a aproximar, es clave que el epsilon sea lo suficientemente chico, en caso contrario la aproximación lineal puede separarse bastante de la solución.

<div style="display: flex; justify-content: center;">
{% include making-waves/ode/predator_prey.html %}
</div>
<div style="text-align: right;" markdown="span">
    <a style="font-size:12px;" 
    href="https://github.com/nacho692/nacho692.github.io/blob/main/_includes/making-waves/ode/predator_prey.html">Código fuente</a>
    <span>[^3]</span>
</div>

[^3]: La idea es que los marcadores sincronicen, si estás usando chrome es posible que la animación no funcione bien. Por algún motivo chrome y firefox animan el marcador a distinto [ritmo](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/calcMode). En chrome spline no funciona, y linear anima como si fuera paced. En firefox parece funcionar bien.  

El resultado es cíclico, cuando las presas llegan a determinada población, causan que la población de los predadores incremente a tal punto que se consumen todas, luego la densidad de predadores baja por falta de alimento.
El segundo gráfico presenta una curva de nivel de las funciones y fue generado de la misma manera que el primero.

Otra manera de generarlo y demostrar la naturaleza cíclica de las ecuaciones es, mediante manipulación algebraica, obtener la ecuación de la curva:

$$
c = \delta x(t) + \beta y(t) - \gamma log(x(t)) - \alpha log(y(t))
$$

> Para ver la derivación de la formula y más información sobre el sistema de ecuaciones, recomiendo el video de Exploring Maths: [Predator-Prey Population Models \|\| Lotka-Volterra Equations](https://www.youtube.com/watch?v=DDEvlLa9z_U)

En este artículo vimos una introducción a ecuaciones diferenciales ordinarias, con una sola variable. 
Pero si queremos hablar de cambio de imagenes a través del tiempo (shaders), necesitamos mínimamente tres variables: $x, y, t$.

En el próximo artículo vamos a salir de los confines de las ODE con la ecuación de calor y la vuelta del laplaciano que utilizamos previamente para detección de bordes.

#### Lecturas recomendadas y referencias

* [ Differential equations, a tourist's guide \| DE1 - 3Blue1Brown](https://www.youtube.com/watch?v=p_di4Zn4wz4): La mejor introducción a ecuaciones diferenciales que encontré
* [Ordinary diferential equations - Physics Courses, Colorado](https://physicscourses.colorado.edu/phys2210/phys2210_fa21/lecture/lec06-odes/)
* [Wikipedia: Lotka–Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)
* [Predator-Prey Population Models \|\| Lotka-Volterra Equations - Exploring Maths](https://www.youtube.com/watch?v=DDEvlLa9z_U): Muy buen video sobre las ecuaciones de Lotka-Volterra
* [1.4 The Lotka-Volterra predator-prey model - Hong Kong University of Science and Technology](https://math.libretexts.org/Bookshelves/Applied_Mathematics/Mathematical_Biology_(Chasnov)/01%3A_Population_Dynamics/1.04%3A_The_Lotka-Volterra_Predator-Prey_Model)
