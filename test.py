from utils.Model import Model
from main import Run as application
from flask import Flask

application()
# to insert a record in table

# model = Model('worker')
# model.firstName = "qwerty"
# model.lastName = "zoop"
# model.age = 34
# model.phoneNumber = "45678998"
# model.skill = 'cook'
# model.range = '10-50km'
# model.save()

# to create a table
# model.createTable(f'''CREATE TABLE {model.tableName}
#          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#          name           CHAR(255)    NOT NULL,
#          phoneNumber           CHAR(255)    NOT NULL,
#          email           CHAR(255)    NOT NULL,
#          password           CHAR(255)    NOT NULL);''')
# print("testing...😎")
