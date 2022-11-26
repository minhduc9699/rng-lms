from random import randint
import uuid
from infrastructure.mysql.main import get_connection
connection = get_connection()

def save_students(students):
  idstudent = students["idstudent"]
  name = students["name"]
  DOB = str(students["DOB"])
  phone = students["phone"]

  cursor = connection.cursor()
  remove_sql = f"""DELETE FROM students WHERE students.idstudent = {idstudent}; """
  sql = f"""INSERT INTO students (idstudent, name, DOB, phone) VALUES ("{idstudent}", "{name}", "{DOB}", "{phone}");"""
  print(sql)
  #executing the SQL command 
  cursor.execute(remove_sql)
  cursor.execute(sql)

  #Commit your changes in the database
  connection.commit()

  #Rolling back in case of error 

  return

def save_classes(classes):
  idclass = classes["idclass"]
  nameOfClass = f'CMC{idclass}'
  nameOfTeacher = 'teacher'

  cursor = connection.cursor()
  remove_sql = f"""DELETE FROM class WHERE class.idclass = {idclass}; """
  sql = f"""INSERT INTO `class` (idclass, nameOfClass, nameOfTeacher) VALUES ("{idclass}", "{nameOfClass}", "{nameOfTeacher}");"""

  #executing the SQL command 
  cursor.execute(remove_sql);
  cursor.execute(sql)

  #Commit your changes in the database
  connection.commit()

  #Rolling back in case of error 
  return

def save_headcount(headcount):
  idclass = headcount["idclass"]
  idstudent = headcount["idstudent"]
  timestamps = headcount["timestamps"]

  cursor = connection.cursor()
  remove_sql = f"""DELETE FROM headcount WHERE headcount.idstudent = {idstudent} AND headcount.idclass = {idclass}; """
  cursor.execute(remove_sql)
  for timestamp in timestamps:
    sql = f"""INSERT INTO headcount (idclass, idstudent, timestamp) VALUES ("{idclass}", "{idstudent}", "{timestamp}");"""
    print(sql)
    #executing the SQL command 
    cursor.execute(sql)

    #Commit your changes in the database
  connection.commit()

  return

