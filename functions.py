import os
import csv
import mysql.connector
from load_env import load_env

ENV = load_env(".env")

DB_CONFIG = {
    "host": ENV.get("host"),
    "user": ENV.get("user"),
    "password": ENV.get("password"), 
    "database": "cs122a"
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
            "DROP TABLE IF EXISTS ModelServices",
            "DROP TABLE IF EXISTS CustomizedModel",
            "DROP TABLE IF EXISTS Configuration",
            "DROP TABLE IF EXISTS LLMService",
            "DROP TABLE IF EXISTS DataStorage",
            "DROP TABLE IF EXISTS InternetService",
            "DROP TABLE IF EXISTS BaseModel",
            "DROP TABLE IF EXISTS AgentClient",
            "DROP TABLE IF EXISTS AgentCreator",
            "DROP TABLE IF EXISTS User"
        ]

        for cmd in cmds:
            cur.execute(cmd)

        # create predefined tables from hw2
            
        create_tables =[
            """CREATE TABLE User (
                uid INTEGER PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE
            )""",
            """CREATE TABLE AgentCreator (
                uid INTEGER PRIMARY KEY,
                payout_account VARCHAR(100) NOT NULL,
                bio VARCHAR(255),
                FOREIGN KEY (uid) REFERENCES User (uid) ON DELETE CASCADE
            )""",
            """CREATE TABLE AgentClient (
                uid INTEGER PRIMARY KEY,
                card_number CHAR(19) NOT NULL,
                cardholder_name VARCHAR(100) NOT NULL,
                expiration DATE NOT NULL,
                cvv CHAR(4) NOT NULL,
                zip VARCHAR(10) NOT NULL,
                interests VARCHAR(255),
                FOREIGN KEY (uid) REFERENCES User (uid) ON DELETE CASCADE
            )""",
            """CREATE TABLE BaseModel (
                bmid INTEGER PRIMARY KEY,
                description VARCHAR(255),
                creator_uid INTEGER NOT NULL,
                FOREIGN KEY (creator_uid) REFERENCES AgentCreator (uid) ON DELETE RESTRICT
            )""",
            """CREATE TABLE InternetService (
                sid INTEGER PRIMARY KEY,
                provider VARCHAR(100) NOT NULL,
                endpoints VARCHAR(255) NOT NULL
            )""",
            """CREATE TABLE LLMService (
                sid INTEGER PRIMARY KEY,
                domain VARCHAR(100) NOT NULL,
                FOREIGN KEY (sid) REFERENCES InternetService (sid) ON DELETE CASCADE
            )""",
            """CREATE TABLE DataStorage (
                sid INTEGER PRIMARY KEY,
                type VARCHAR(50) NOT NULL,
                FOREIGN KEY (sid) REFERENCES InternetService (sid) ON DELETE CASCADE
            )""",
            """CREATE TABLE CustomizedModel (
                bmid INTEGER NOT NULL,
                mid INTEGER NOT NULL,
                PRIMARY KEY (bmid, mid),
                FOREIGN KEY (bmid) REFERENCES BaseModel (bmid) ON DELETE CASCADE
            )""",
            """CREATE TABLE Configuration (
                cid INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                labels VARCHAR(255),
                client_uid INTEGER NOT NULL,
                FOREIGN KEY (client_uid) REFERENCES AgentClient (uid) ON DELETE CASCADE
            )""",
            """CREATE TABLE ModelServices (
                bmid INTEGER NOT NULL,
                sid INTEGER NOT NULL,
                version VARCHAR(50),
                PRIMARY KEY (bmid, sid),
                FOREIGN KEY (bmid) REFERENCES BaseModel (bmid) ON DELETE CASCADE,
                FOREIGN KEY (sid) REFERENCES InternetService (sid) ON DELETE RESTRICT
            )""",
            """CREATE TABLE ModelConfiguration (
                cid INTEGER NOT NULL,
                bmid INTEGER NOT NULL,
                mid INTEGER NOT NULL,
                duration_seconds INTEGER NOT NULL,
                PRIMARY KEY (cid, bmid, mid),
                FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE,
                FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel (bmid, mid) ON DELETE CASCADE
            )"""
        ]

        for cmd in create_tables:
            cur.execute(cmd)

        # populate tables
        table_files = {
            "User": "User.csv",
            "AgentCreator": "AgentCreator.csv",
            "AgentClient": "AgentClient.csv",
            "LLMService" : "LLMService.csv",
            "DataStorage": "DataStorage.csv",
            "Configuration": "Configuration.csv",
            "ModelServices": "ModelServices.csv",
            "BaseModel": "BaseModel.csv",
            "InternetService": "InternetService.csv",
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
