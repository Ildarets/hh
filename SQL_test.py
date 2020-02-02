import sqlite3
from class_hh_sql import Parser_HH
from main_sql import Input_SQL

test_Q = Input_SQL('Java', 'Набережные Челлны')
test_Q_list = test_Q.select_table_sql('Java', 'Набережные Челлны')

print(test_Q_list)