#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pdb

ANCHO = 10
ALTO = 15
H = 0.2


def crear_caja(ancho, alto, h):
    '''recibe las dimensiones de la caja  y el tamaño del reticulado
     y la inicia en puros ceros '''
    ancho_efectivo = ancho / h + 1
    alto_efectivo = alto / h + 1
    caja = np.zeros((ancho_efectivo, alto_efectivo))

    return caja


def poner_condiciones_borde(caja):
    '''conecta a tierra el perímetro de la caja, la segunda iteración
    (bordes laterales) se itera desde borde+1, hasta borde para evitar pasar
    2 veces por las esquinas'''
    borde_inferior = np.array([np.array([-5, -7.5]), np.array([5, -7.5])])
    borde_superior = np.array([np.array([-5, 7.5]), np.array([5, 7.5])])
    borde_inferior[0] = transformar(borde_inferior[0])
    borde_inferior[1] = transformar(borde_inferior[1])
    borde_superior[0] = transformar(borde_superior[0])
    borde_superior[1] = transformar(borde_superior[1])
    for i in range(int(borde_inferior[0][0]), int(borde_inferior[1][0]) + 1):
        caja[i, borde_inferior[0][1]] = 0
        caja[i, borde_superior[0][1]] = 0
    for i in range(int(borde_inferior[0][1])+1, int(borde_superior[0][1])):
        caja[borde_inferior[0][0], i] = 0
        caja[borde_superior[1][0], i] = 0
    return caja


def esta_fuera_letra(i, j):
    '''devuelve True si la coordenada está fuera de el bloque que contiene
    la letra'''
    if (i < 3 / H or i > 7 / H):
        return True
    elif (j < 4 / H or j > 11 / H):
        return True
    return False


def esta_cerca_linea(i, j):
    '''Devuele true si la coordenada no es adyacente a la linea
    con condiciones de borde derivativas '''
    if (j == 2 / H + 1 or j == 2 / H - 1):
        if(2 / H < i and i < 8 / H):
            return True
    return False


def iteracion_resto(caja, caja_next, caja_carga, numero_pasos, h, w=1):
    '''avanza el algoritmo de sobre relajación 1 vez, fuera del rectangulo
    interior y lejos de la linea'''
    rango_x = np.array([0 / h, 10 / h])
    rango_y = np.array([0 / h, 15 / h])
    for i in range(int(rango_x[0]) + 1, int(rango_x[1])):
        for j in range(int(rango_y[0]) + 1, int(rango_y[1])):
            if (esta_fuera_letra(i, j) and not(esta_cerca_linea(i, j))):
                caja_next[i, j] = ((1 - w) * caja[i, j] +
                                   w / 4 * (caja[i + 1, j] +
                                   caja_next[i - 1, j] +
                                   caja[i, j+1] + caja_next[i, j-1]))


def iteracion_letra(caja, caja_next, caja_carga, numero_pasos, h, w=1):
    '''avanza el algoritmo de sobre relajación 1 vez, en el casillero interior
    que contiene la letra'''
    rango_x = np.array([3 / h, 7 / h])
    rango_y = np.array([4 / h, 11 / h])
    for i in range(int(rango_x[0]), int(rango_x[1] + 1)):
        for j in range(int(rango_y[0]), int(rango_y[1] + 1)):
            caja_next[i, j] = ((1 - w) * caja[i, j] +
                               w / 4 * (caja[i+1, j] + caja_next[i-1, j] +
                                        caja[i, j+1] + caja_next[i, j-1] +
                                        h**2 * caja_carga[i, j]))


def iteracion_linea(caja, caja_next, caja_carga, numero_pasos, h, w=1):
    '''avanza el algoritmo de sobre relajación 1 vez en los
    casilleros cercanos a la línea'''
    rango_x = np.array([2/h, 8/h])
    rango_y = np.array([1/h, 3/h])
    g_1 = -1
    g_2 = 1

    for i in range(int(rango_x[0]), int(rango_x[1]+1)):
        caja_next[i, int(rango_y[0])] = ((1-w)*caja[i, int(rango_y[0])] +
                                         w/3*(caja_next[i-1, int(rango_y[0])] +
                                         caja[i+1, int(rango_y[0])] +
                                         caja_next[i, int(rango_y[0])-1] +
                                         h*g_1))
        caja_next[i, int(rango_y[0])+1] = caja_next[i, int(rango_y[0])] + h*g_1

    for i in range(int(rango_x[0]), int(rango_x[1]+1)):
        caja_next[i, int(rango_y[1])] = caja_next[i, int(rango_y[0])+1] + h*g_2


def convergio(caja, caja_next, tolerancia):
    '''compara 2 estados de la malla, y decide si converge según la tolerancia
    pedida'''


def f_caja_carga(x, y):
    '''función auxilar para plotear, recibe la coordenada x e y y devuelve
    el valor de la malla de carga en esas coordenadas'''
    return caja_carga[x, y]


def f_caja_potencial_next(x, y):
    '''función auxilar para plotear, recibe la coordenada x e y y devuelve
    el valor de la malla de potencial en esas coordenadas'''
    return caja_potencial_next[x, y]


def mostrar(f_caja, caja, titulo):
    '''plotea la solución en 3D'''
    (ancho, alto) = caja.shape
    x = np.linspace(0, ancho-1, ancho)
    y = np.linspace(0, alto-1, alto)
    xg, yg = np.meshgrid(x, y)
    vector_f = np.vectorize(f_caja)
    z = vector_f(xg, yg)
    '''
    fig = plt.figure(1)
    fig.clf()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xg,yg,z, rstride=1, cstride=1)
    '''
    fig2 = plt.figure()
    fig2.clf()
    ax2 = fig2.add_subplot(111)
    ax2.imshow(z, origin='bottom', interpolation='nearest')
    ax2.contour(z, origin='lower')


def es_horizontal(ini, fin):
        '''retorna true si el trazo es horizontal, o false si es vertical'''
        return (ini[1] == fin[1])


def trazo(ini, fin, ancho):
    '''recibe la coordenada de inicio del trazo, el final y el ancho del
    trazo, devuelve un arreglo con las coordenadas de los puntos que lo
    conformman. Sólo funciona para trazos rectos.
    (recibe los puntos más izquierdos, o más  abajo del trazo)'''
    ancho = int(ancho)+1
    actual = ini
    if es_horizontal(ini, fin):
        paso = np.array([1, 0])
        ancho_1 = np.array([0, 1])
        rango = int(np.fabs(fin[0]-ini[0]))+1
    else:
        paso = np.array([0, 1])
        ancho_1 = np.array([1, 0])
        rango = int(np.fabs(fin[1]-ini[1]))

    trazo = np.zeros([(rango)*(ancho), 2])
    for a in range(ancho):
        for i in range(rango):
            trazo[i+(rango)*a] = np.array([actual])
            actual += paso
        actual = ini
        actual += (a+1)*ancho_1

    return trazo


def transformar(coordenada):
    ''' recibe coordenadas considerando 0,0 como el centro y
    las dimensiones originales en centímetros, a las unidades de la grilla
    . Notar que se utiliza Ancho+1 porque el arreglo se define desde 0'''

    x, y = coordenada[0], coordenada[1]
    x_tran = int((x + (ANCHO)/2)/H)
    y_tran = int((y + (ALTO)/2)/H)
    return x_tran, y_tran


def armar_letra():
    '''devuelve el arreglo de coordenaas que conforman la letra, las coordenadas
     ini y fin se dan considerando 0,0 en el centro y
     las dimensiones en centímetros'''
    ancho = 1
    ini = np.array([1, -3.5])
    fin = np.array([1, 3.5])
    ini2 = np.array([-2, -3.5])
    fin2 = np.array([1, -3.5])
    ini3 = np.array([-2, -2.5])
    fin3 = np.array([-2, 0])

    ancho_transf = ancho / H
    ini, fin = transformar(ini), transformar(fin)
    ini2, fin2 = transformar(ini2), transformar(fin2)
    ini3, fin3 = transformar(ini3), transformar(fin3)

    trazo_1 = trazo(ini, fin, ancho_transf)
    trazo_2 = trazo(ini2, fin2, ancho_transf)
    trazo_3 = trazo(ini3, fin3, ancho_transf)
    letra = np.append(trazo_1, trazo_2, axis=0)
    letra = np.append(letra, trazo_3, axis=0)
    return letra


def poner_carga(caja, coordenadas, total):
    '''recibe la caja a modificar, la carga total a colocar y
     las coordenadas para setear el arreglo de cargas inicial '''
    carga_en_un_punto = total / len(coordenadas)
    for par in coordenadas:
        caja[par[0], par[1]] = carga_en_un_punto
    return caja


# main
w = 1.8
numero_pasos = np.array([ANCHO/H + 1, ALTO/H + 1])
coordenadas_carga = armar_letra()
carga_total = 1.

caja_carga = crear_caja(ANCHO, ALTO, H)
caja_potencial = crear_caja(ANCHO, ALTO, H)
caja_potencial_next = crear_caja(ANCHO, ALTO, H)

caja_carga = poner_carga(caja_carga, coordenadas_carga, carga_total)

caja_potencial = poner_condiciones_borde(caja_potencial)

iteracion_letra(caja_potencial, caja_potencial_next, caja_carga,
                numero_pasos, H, w)
iteracion_linea(caja_potencial, caja_potencial_next, caja_carga,
                numero_pasos, H, w)
iteracion_resto(caja_potencial, caja_potencial_next, caja_carga,
                numero_pasos, H, w)

contador = 1
tolerancia = 1e-100
while (contador < 800 and not convergio(caja_potencial, caja_potencial_next,
                                        tolerancia)):
    caja_potencial = caja_potencial_next.copy()
    iteracion_letra(caja_potencial, caja_potencial_next, caja_carga,
                    numero_pasos, H, w)
    iteracion_linea(caja_potencial, caja_potencial_next, caja_carga,
                    numero_pasos, H, w)
    iteracion_resto(caja_potencial, caja_potencial_next, caja_carga,
                    numero_pasos, H, w)
    contador += 1
print("numero iteraciones: "+str(contador))
mostrar(f_caja_carga, caja_carga, "distribucion carga")
mostrar(f_caja_potencial_next, caja_potencial_next, "potencial")
plt.show()
