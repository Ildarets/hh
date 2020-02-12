import sqlite3
from class_hh_sql import Parser_HH
from main_sql import Input_SQL
from class_Input_SQLAlchemy import Input_SQLAlchemy

# test_Q = Input_SQL('Java', 'Набережные Челлны')
# test_Q_list = test_Q.select_table_sql('Java', 'Набережные Челлны')
#
# print(test_Q_list)

test_Alch = Input_SQLAlchemy('Data', 'Казань')
test_Alch.create_table()

test_Alch.full_table_sql()

sk_list = test_Alch.select_table_sql('Data', 'Казань')
print(sk_list)