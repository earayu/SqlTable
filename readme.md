## SqlBox
This is my personal sql toolBox

### SqlTable
```
it's convenient to use this tool to verify some thoughts, eg. XA+MDL deadlock 

step 1: init transactions with class Trx
[Trx('connection1', '127.0.0.1', 3306, 'username', 'password'), Trx('connection2', '127.0.0.1', 3306, 'username', 'password')]

step 2: define sql table, it will be executed row by row
[
	['use db7',				'use db7'				],
	['select version()',			'select version()'			],
	['update t1 set c2 = 1 where c1 = 1', 	'update t2 set c2 = 1 where c1 = 1'	],
	['update t2 set c2 = 1 where c1 = 1', 	'update t1 set c2 = 1 where c1 = 1'	]
]
```

