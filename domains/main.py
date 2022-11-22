from infrastructure.mysql.main import get_connection
connection = get_connection()

def save_students(students):
  idstudent = students["idstudent"]
  name = students["name"]
  DOB = students["DOB"]
  phone = students["phone"]

  cursor = connection.cursor()
  sql = f"""INSERT INTO students (idstudent, name, DOB, phone) VALUES ("{idstudent}", {name}", "{DOB}", "{phone}");"""
  try: 
    #executing the SQL command 
    cursor.execute(sql)

    #Commit your changes in the database
    connection.commit()
  
  except:
    #Rolling back in case of error 
    connection.rollback()

  #Closing the connection 
  connection.close()

  return

def save_classes(classes):
  idclass = classes["idclass"]
  nameOfClass = classes["nameOfClass"]
  nameOfTeacher = classes["nameOfTeacher"]

  cursor = connection.cursor()
  sql = f"""INSERT INTO `class` (idclass, nameOfClass, nameOfTeacher) VALUES ("{idclass}", "{nameOfClass}", "{nameOfTeacher}");"""
  print(sql)

  try: 
    #executing the SQL command 
    cursor.execute(sql)

    #Commit your changes in the database
    connection.commit()
  
  except:
    #Rolling back in case of error 
    connection.rollback()

  #Closing the connection 
  connection.close()
  return

def save_headcount(headcount):
  idheadcount = headcount["idheadcount"]
  idclass = headcount["idclass"]
  idstudent = headcount["idstudent"]
  timestamp = headcount["timestamp"]

  cursor = connection.cursor()
  sql = f"""INSERT INTO headcount (idheadcount, idclass, idstudent, timestamp) VALUES ("{idheadcount}", "{idclass}", "{idstudent}", "{timestamp}");"""
  try: 
    #executing the SQL command 
    cursor.execute(sql)

    #Commit your changes in the database
    connection.commit()
  
  except:
    #Rolling back in case of error 
    connection.rollback()

  #Closing the connection 
  connection.close()
  return

