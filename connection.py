import mysql.connector
def connect():
    global mydb
    try:
        mydb = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12614791",
            password="tZYJXUm7WH",
            database = "sql12614791"
            )
        print(mydb)
    except:
        return False
    
# checkserver
def checkserver(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM last WHERE server_id = '%s'",(id,))
    myresult = mycursor.fetchall()
    if(len(myresult)<3):
        return True
    else:
        return False
    
# check checkchannel in server
def checkchannel(server,channel):
    cur = mydb.cursor()
    cur.execute("SELECT * FROM last WHERE server_id = '%s' AND channel_id = '%s'",(server,channel))
    myresult = cur.fetchall()
    if(len(myresult)==0):
        return True
    else:
        return False

# insert data last
def insert_last(data):
    cur = mydb.cursor()
    sql = "INSERT INTO last (req_message,server_id,channel_id,message_id ) VALUES (%s,%s,%s,%s)"
    val = (data["req_message"],data["server_id"],data["channel_id"],data["message_id"])
    cur.execute(sql, val)
    mydb.commit()
    return True
    
# delete_last
def delete_last(server,channel):
    cur = mydb.cursor()
    sql = f"DELETE FROM last WHERE server_id = '{server}' AND channel_id = '{channel}'"
    cur.execute(sql)
    mydb.commit()
    return True

# get all last
def get_all_last():
    cur = mydb.cursor()
    sql = "SELECT * FROM last"
    cur.execute(sql)
    myresult = cur.fetchall()
    return myresult

# update last
def update_last(id,mess_id):
    cur = mydb.cursor()
    sql = f"UPDATE last SET message_id = '{mess_id}' WHERE id_last = '{id}'"    
    cur.execute(sql)
    mydb.commit()
    return True

# get one last
def get_one_last(server,channel):
    cur = mydb.cursor()
    sql = f"SELECT * FROM last WHERE server_id = '{server}' AND channel_id = '{channel}'"
    cur.execute(sql)
    myresult = cur.fetchall()
    return myresult

# check server welcome 
def checkwelcome(server):
    cur = mydb.cursor()
    sql = f"SELECT * FROM welcome WHERE server_id = '{server}'"
    cur.execute(sql)
    myresult = cur.fetchall()
    return myresult

# insert welcome
def insert_welcome(data):
    cur = mydb.cursor()
    sql = "INSERT INTO welcome (req_message,server_id,channel_id,w_status ) VALUES (%s,%s,%s,%s)"
    val = (data["req_message"],data["server_id"],data["channel_id"],data["w_status"])
    cur.execute(sql, val)
    mydb.commit()
    return True

# delete welcome
def delete_welcome(server):
    cur = mydb.cursor()
    sql = f"DELETE FROM welcome WHERE server_id = '{server}'"
    cur.execute(sql)
    mydb.commit()
    return True


