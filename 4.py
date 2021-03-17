import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR', user='root', password='1234', autocommit=True)

cursor = connection.cursor()
cursor.execute('select version();')
result = cursor.fetchone()

print('mysql version : {}'.format(result))

connection.close()