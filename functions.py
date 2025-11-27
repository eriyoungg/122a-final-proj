import os
import csv
import mysql.connector
from load_env import load_env

ENV = load_env(".env")

DB_CONFIG = {
    "host": ENV.get("host"),
    "user": ENV.get("user"),
    "password": ENV.get("password"), 
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def import_data(folder_name):
    try:
        conn = get_connection() # connects to sql server
        cur = conn.cursor() # executes commands

        # reset/delete tables if exists
        cmds = [
            "DROP TABLE IF EXISTS ModelConfiguration",
            "DROP TABLE IF EXISTS CustomizedModel",
            "DROP TABLE IF EXISTS BaseModelService",
            "DROP TABLE IF EXISTS InternetService",
            "DROP TABLE IF EXISTS BaseModel",
            "DROP TABLE IF EXISTS AgentInterests",
            "DROP TABLE IF EXISTS PaymentInfo",
            "DROP TABLE IF EXISTS AgentClient"
        ]

        for cmd in cmds:
            cur.execute(cmd)

        path = os.path.join(folder_name, "ddl.sql")
        with open(path, "r") as f:
            script = f.read()
            for cmd in script.split(";"):
                if cmd.strip():
                    cur.execute(cmd)

        # create tables
        table_files = {
            "AgentClient": "AgentClient.csv",
            "PaymentInfo": "PaymentInfo.csv",
            "AgentInterests": "AgentInterests.csv",
            "BaseModel": "BaseModel.csv",
            "InternetService": "InternetService.csv",
            "BaseModelService": "BaseModelService.csv",
            "CustomizedModel": "CustomizedModel.csv",
            "ModelConfiguration": "ModelConfiguration.csv",
        }

        for table, filename in table_files.items():
            path = os.path.join(folder_name, filename)
            if not os.path.exists(path):
                print(f"Missing file: {path}")
                return False
            
            with open(path, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

                if len(rows) == 0:
                    continue
            
                placeholders = ",".join(["%s"] * len(rows[0]))
                cmd = f"INSERT INTO {table} VALUES ({placeholders})"

                cur.executemany(cmd, rows)
        conn.commit()
        return True
    except Exception as e:
        print("ERROR:", e)
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
