#!/usr/bin/env python
#-*- coding: utf8 -*-

class QueryHandler(object):
    def query(self, data):
        """ Retorna True si la consulta devuelve resultados, sino False
        data es la expresión generada por Squler"""
        pass

def adivinaint(handler, rango):
	""" Intenta adivinar el valor de un entero mayor perteneciente a
	range(*rango). Handler debe ser una instancia de QueryHandler """
	diferencia = 4 # hacemos un bucle tipo do..while
	while diferencia > 3:
		diferencia = rango[1] - rango[0]
		medio = rango[0] + diferencia/2
		#print medio,
		if handler.query('<=%s'%medio):
			# n <= medio
			rango[1] = medio
			#print rango
		else:
			# n > medio
			rango[0] = medio + 1
			#print rango
	for i in range(rango[0],rango[1]+1):
		#print i
		if handler.query('=%s'%i):
			return i
	raise ValueError
