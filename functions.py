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

        # disable foreign key checks
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")

        # reset/delete tables if exists
        cmds = [
            "DROP TABLE IF EXISTS ModelConfigurations",
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
                email VARCHAR(50) NOT NULL UNIQUE,
                username VARCHAR(50) NOT NULL
            )""",
            """CREATE TABLE AgentCreator (
                uid INTEGER PRIMARY KEY,
                bio VARCHAR(255),
                payout VARCHAR(100) NOT NULL,
                FOREIGN KEY (uid) REFERENCES User (uid) ON DELETE CASCADE
            )""",
            """CREATE TABLE AgentClient (
                uid INTEGER PRIMARY KEY,
                interests VARCHAR(255),
                cardholder VARCHAR(100) NOT NULL,
                expire DATE NOT NULL,
                cardno CHAR(19) NOT NULL,
                cvv CHAR(5) NOT NULL,
                zip VARCHAR(10) NOT NULL,
                FOREIGN KEY (uid) REFERENCES User (uid) ON DELETE CASCADE
            )""",
            """CREATE TABLE BaseModel (
                bmid INTEGER PRIMARY KEY,
                creator_uid INTEGER NOT NULL,
                description VARCHAR(255),
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
                client_uid INTEGER NOT NULL,
                content TEXT NOT NULL,
                labels VARCHAR(100),
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
            """CREATE TABLE ModelConfigurations (
                bmid INTEGER NOT NULL,
                mid INTEGER NOT NULL,
                cid INTEGER NOT NULL,
                duration INTEGER NOT NULL,
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
            "AgentClient": "AgentClient.csv",
            "AgentCreator": "AgentCreator.csv",
            "InternetService": "InternetService.csv",
            "BaseModel": "BaseModel.csv",
            "LLMService" : "LLMService.csv",
            "DataStorage": "DataStorage.csv",
            "CustomizedModel": "CustomizedModel.csv",
            "Configuration": "Configuration.csv",
            "ModelServices": "ModelServices.csv",
            "ModelConfigurations": "ModelConfigurations.csv",
        }

        for table, filename in table_files.items():
            path = os.path.join(folder_name, filename)
            if not os.path.exists(path):
                print(f"Missing file: {path}")
                return False
            
            with open(path, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)[1:] # skip header row

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

def insertAgentClient(uid, username, email, cardno,
                      card_holder, expiration_date, cvv,
                      zip_code, interests):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql_command = """INSERT INTO User (uid, email, username)
                         VALUES (%s, %s, %s)
                         """

        sql_command2 = """INSERT INTO AgentClient (uid, interests, cardholder, expire, cardno, cvv, zip)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                          """
        cur.execute(sql_command, (uid, email, username))
        cur.execute(sql_command2, (uid, interests, card_holder, expiration_date, cardno, cvv, zip_code))
        conn.commit()
        return True
    except Exception as e:
        print(f"Failed to insert client: {e}")

        # rollback changes in case of error
        if 'conn' in locals() and conn:
            conn.rollback()

        # in case of duplicate primary key, print all users in database to debug
        print('All users:')
        try:
            cur.execute("SELECT * FROM User")
            users = cur.fetchall()
            for user in users:
                print(user)
        except Exception as e:
            print(f"Failed to fetch users: {e}")
        
        
            
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
