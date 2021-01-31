#!/usr/bin/python3
import threading
import pymysql
import time


"""
it's convenient to use this tool to verify some thoughts, eg. XA+MDL deadlock 

step 1: init transactions with class Trx
[Trx('connection1', '127.0.0.1', 3306, 'username', 'password'), Trx('connection2', '127.0.0.1', 3306, 'username', 'password')]

step 2: define sql table, it will be executed row by row
[
	['use db7',								'use db7'							],
	['select version()',					'select version()'					],
	['update t1 set c2 = 1 where c1 = 1', 	'update t2 set c2 = 1 where c1 = 1'	],
	['update t2 set c2 = 1 where c1 = 1', 	'update t1 set c2 = 1 where c1 = 1'	]
]

"""


class SqlTable:
	def __init__(self, trxList, matrix):
		self.trxList = trxList
		self.matrix = matrix
		self.row = len(matrix)
		assert self.row > 0
		self.column = len(matrix[0])
		assert len(self.trxList) == self.column
		self.threads = []

	def getTrxList(self):
		return self.trxList

	def getMatrix(self):
		return self.matrix

	def executeSqlTable(self):
		for row in self.matrix:
			for index, value in enumerate(row):
				if value is None:
					continue
				if value == '':
					continue
				try:
					trx = self.trxList[index]
					print('%s execute: %s' % (trx.name, value))
					trx.execute(value)
				except Exception as e:
					print(e)
					raise
				else:
					pass
				finally:
					pass

	def executeSqlTableBg(self):
		for row in self.matrix:
			for index, value in enumerate(row):
				if value is None:
					continue
				if value == '':
					continue
				try:
					trx = self.trxList[index]
					print('%s executeBg: %s' % (trx.name, value))
					t = threading.Thread(target=trx.execute, args=(value,))
					t.start()
					time.sleep(1)
				except Exception as e:
					print(e)
					raise
				else:
					pass
				finally:
					pass



def getConnection(host, user, passwd, db):
	return pymysql.connect(host=host, user=user, passwd=passwd, db=db)

def getConnection(host, user, passwd):
	return pymysql.connect(host=host, user=user, passwd=passwd)

def executeSql(cursor, sql):
	print(sql)
	try:
		cursor.execute(sql)
	except Exception as e:
		print(e)
		raise
	else:
		pass
	finally:
		pass

def newThread(cursor, sql):
	t = threading.Thread(target=executeSqlThenPrintDone, args=(cursor, sql))
	return t

class Trx:
	def __init__(self, name, host, port, user, passwd):
		self.name = name
		self.host = host
		self.port = port
		self.user = user
		self.passwd = passwd
		self.connection = pymysql.connect(host=host, port=port, user=user, passwd=passwd)
		self.cursor = self.connection.cursor()

	def begin(self):
		execute('begin')

	def commit(self):
		execute('commit')

	def rollback(self):
		execute('rollback')

	def execute(self, sql):
		self.cursor.execute(sql)

	def executeBg(self, sql):
		print('BackGround Execute: ' + sql)
		t = threading.Thread(target=self.execute, args=(sql,))
		t.start()

	def getConnection(self):
		return self.connection

	def getCursor(self):
		return self.cursor

	def destory(self):
		if self.cursor is not None:
			self.cursor.close()
		if self.connection is not None:
			self.connection.close()

	def __str__(self):
		return '(%s,%s,%s,%s,%s)' % (self.name, self.host, self.port, self.user, self.passwd)




if __name__ == '__main__':
	
	trxList = [Trx('connection1', '127.0.0.1', 3306, 'username', 'password'), Trx('connection2', '127.0.0.1', 3306, 'username', 'password')]
	# expect: pymysql.err.OperationalError: (1213, 'Deadlock found when trying to get lock; try restarting transaction')
	matrix = [
		['use db7','use db7'],
		['select version()','select version()'],
		['update t1 set c2 = 1 where c1 = 1', 'update t2 set c2 = 1 where c1 = 1'],
		['update t2 set c2 = 1 where c1 = 1', 'update t1 set c2 = 1 where c1 = 1']
	]

	a = SqlTable(trxList, matrix)
	a.executeSqlTableBg()


		




