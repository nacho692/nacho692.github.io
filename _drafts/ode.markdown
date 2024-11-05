---
layout: post
title:  "Making Waves! Ecuaciones diferenciales ordinarias"
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
{% include making-waves/ode/ode.html %}
</div>

Existen tantas funciones solución como velocidades iniciales y posiciones iniciales existen. 
Hay una manera interesante en la que podemos observar como se comporta el sistema para todos los pares $(v_0, p_0)$.
La idea es definir una transformación lineal $T$ tal que $T(v_t, p_t) = (v_{t+1}, p_{t+1})$.
Es decir, dado un estado inicial, $T$ devuelve el paso en el instante siguiente. 
Con un poco de algebra podemos ver como despejar esta fórmula.

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
La posición actual es la misma pero sumada la velocidad actual y una parte de la aceleración, que es lo que se agrega por incrementarse la velocidad linealmente en este "paso".
Veamos un ejemplo con $a = 1, v_0 = 1, p_0 = 1$.

|$t$| $(v_t, p_t)$ | $T(v_t, p_t)$ | $T(v_t, p_t) - (v_t, p_t)$ |
| $0$ | $(1, 1)$ | $(2, 2.5)$ | $(1, 1.5)$ |
| $1$ | $(2, 2.5)$ | $(3, 5)$ | $(1, 2.5)$ |
| $2$ | $(3, 5.75)$ | $(4, 8.5)$ | $(1, 3.5)$ |
| $3$ | $(4, 11.675)$ | $(5, 13)$ | $(1, 4.5)$ |
| $4$ | $(5, 21.4375)$ | $(6, 18.5)$ | $(1, 5.5)$ |

<div style="display: flex; justify-content: center;">
{% include making-waves/ode/pathing.html %}
</div>

El gráfico anterior muestra como, en base al estado del sistema, dado por $(v_t, p_t)$, podemos calcular el estado siguiente.
Calculando la diferencia entre el estado en $t$ y en $t + 1$ podemos ver gráficamente el camino que toma el sistema, incrementando
la posición cuadráticamente.
Un detalle a considerar es que para el dibujo, los vectores de diferencia están corridos, siendo el origen el estado anterior y no $(0, 0)$.
En vez de graficar un solo camino posible para el sistema, se puede armar una grilla y evaluar todos al mismo tiempo.

<div style="display: flex; justify-content: center;">
{% include making-waves/ode/acceleration.html %}
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
{% include making-waves/ode/ode_pop.html %}
</div>

El resultado es cíclico, cuando las presas llegan a determinada población, causan que la población de los predadores incremente a tal punto que se consumen todas, luego la densidad de predadores baja por falta de alimento.


### Links copados

* El visualizador de ecuaciones diferenciales
