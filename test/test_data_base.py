import os
import sqlite3
from sqlite3 import IntegrityError
from contextlib import closing
import pytest


def test_db_exist(data_base_path):
    assert os.path.exists(data_base_path)

def test_table_exist(data_base_path):
    expected_names = [('habit',),('tracking',)]
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""SELECT name FROM sqlite_master;""")
            table_names = cursor.fetchall()
    assert all(list(map(lambda x: x in table_names,expected_names)))
    assert len(table_names) == len(expected_names)

@pytest.mark.parametrize("table_name, expected_names",[('habit',('id','name','description','frequency','creation_time')),
                                                     ('tracking',('ID','habit_id','completed_dates'))])
def test_column_names(data_base_path,table_name,expected_names):
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute(f"""SELECT * FROM {table_name}""")
            column_names = cursor.description
    for data in column_names:
        assert any(data[0] == name for name in expected_names)
    assert len(column_names) == len(expected_names)

@pytest.mark.parametrize("expected_data",[(1,"Go for a walk","Walking at least 1km a day.")])
def test_read(data_base_path,expected_data):
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""SELECT id, name, description FROM habit WHERE id = 1""")
            data = cursor.fetchall()
    for value in data[0]:
        assert value in expected_data

def test_insert_read_update_delete(data_base_path):
    id_number = 0
    #insert
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""INSERT INTO habit (name, description, frequency,creation_time) VALUES (?, ?, ?,?)""",("name","description",1,"2024-11-11T10:58:50.743272"))
            id_number = cursor.lastrowid
        connect.commit()
    #read
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""SELECT id, name, description,frequency FROM habit WHERE id = ?""",(id_number,))
            data = cursor.fetchall()
    for value in data[0]:
        assert value in (id_number,"name","description",1)
    #update
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""UPDATE habit SET name=?, description=?, frequency=? WHERE id=?""",("new name","new description",2,id_number))
        connect.commit()
    #read update
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""SELECT id, name, description,frequency FROM habit WHERE id = ?""",(id_number,))
            data = cursor.fetchall()
    for value in data[0]:
        assert value in (id_number,"new name","new description",2)
    #delete
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""DELETE FROM habit WHERE id=?""",(id_number,))
        connect.commit()
    #test if deleted
    with closing(sqlite3.connect(database=data_base_path)) as connect:
        with closing(connect.cursor()) as cursor:
            cursor.execute("""
                SELECT id FROM habit
            """)
            assert not id_number in [row[0] for row in cursor.fetchall()]

def test_integrity_error(data_base_path):
    with pytest.raises(IntegrityError):
        with closing(sqlite3.connect(database=data_base_path)) as connect:
            with closing(connect.cursor()) as cursor:
                cursor.execute("""INSERT INTO habit (description, frequency,creation_time) VALUES (?, ?,?)""",("description",1,"2024-11-11T10:58:50.743272"))
                cursor.execute("""INSERT INTO habit (name, frequency,creation_time) VALUES (?,?,?)""",("name",1,"2024-11-11T10:58:50.743272"))
                cursor.execute("""INSERT INTO habit (name, description, creation_time) VALUES (?, ?, ?,?)""",("name","description","2024-11-11T10:58:50.743272"))
                cursor.execute("""INSERT INTO habit (name, description, frequency) VALUES (?, ?, ?)""",("name","description",1))