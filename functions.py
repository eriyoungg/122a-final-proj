import mysql.connector

DB = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)

print(DB)

def get_connection():
    return mysql.connector.connect(**DB)

def import_data(folder_name):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # drop tables, create tables
        # read CSVs in folder_name, insert records

        conn.commit()
        return True
    except:
        return False
    finally:
        cur.close()
        conn.close()

def insertAgentClient(uid, username, email, card_number,
                      card_holder, expiration_date, cvv,
                      zip_code, interests):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # insert into relevant tables

        conn.commit()
        return True
    except:
        return False
    finally:
        cur.close()
        conn.close()

def addCustomizedModel(mid, bmid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # insert into customized model table

        conn.commit()
        return True
    except:
        return False
    finally:
        cur.close()
        conn.close()

def deleteBaseModel(bmid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # delete base model (cascade)

        conn.commit()
        return True
    except:
        return False
    finally:
        cur.close()
        conn.close()

def listInternetService(bmid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SELECT sid, endpoint, provider 

        rows = [] 
        return rows
    except:
        return []
    finally:
        cur.close()
        conn.close()

def countCustomizedModel(bmid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SELECT bmid, description, count

        rows = []
        return rows
    except:
        return []
    finally:
        cur.close()
        conn.close()

def topNDurationConfig(uid, N):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SELECT uid, cid, label, content, duration 

        rows = []
        return rows
    except:
        return []
    finally:
        cur.close()
        conn.close()

def listBaseModelKeyWord(keyword):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SELECT bmid, sid, provider, domain

        rows = []
        return rows
    except:
        return []
    finally:
        cur.close()
        conn.close()

def printNL2SQLresult():
    try:
        conn = get_connection()
        cur = conn.cursor()

        # read csv
        # return rows for print

        rows = []
        return rows
    except:
        return []
    finally:
        cur.close()
        conn.close()
