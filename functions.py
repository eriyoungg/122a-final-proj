import os
import csv
import mysql.connector
from load_env import load_env

ENV = load_env(".env")

DB_CONFIG = {
    "host": "localhost",
    "user": "test",
    "password": "password",
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

'''
Inserts new row into User and AgentClient
'''
def insertAgentClient(uid, username, email, cardno,
                      card_holder, expiration_date, cvv,
                      zip_code, interests):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # check if uid primary key already exists
        cur.execute("SELECT 1 FROM User WHERE uid = %s", (uid,))
        users = cur.fetchone()

        if users:
            print("[DEBUG] User with uid '{uid}' already exists/")
            raise ValueError
        
        # check if uid primary key already exists
        cur.execute("SELECT 1 FROM AgentClient WHERE uid = %s", (uid,))
        agents = cur.fetchone()

        if agents:
            print("[DEBUG] AgentClient with uid '{uid}' already exists.")
            raise ValueError

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
        print(f"Failed to insert client.\n{e}")

        # rollback changes in case of error
        if 'conn' in locals() and conn:
            conn.rollback()
        
        return False
    
    finally:
        cur.close()
        conn.close()

'''
Inserts new row into CustomizedModel
'''
def addCustomizedModel(mid, bmid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # check if bmid exists
        cur.execute("SELECT 1 FROM BaseModel WHERE bmid = %s", (bmid,))
        bmids = cur.fetchone()

        if not bmids:
            print(f"[DEBUG] BaseModel with bmid '{bmid}' does not exist.")
            raise ValueError
        
        # check if primary key (bmid, mid) exists
        cur.execute("SELECT 1 FROM CustomizedModel WHERE bmid = %s AND mid = %s", (bmid, mid))
        customized_models = cur.fetchone()

        if customized_models:
            print(f"[DEBUG] CustomizedModel with bmid '{bmid}' and mid '{mid}' already exists.")
            raise ValueError

        sql_command = """INSERT INTO CustomizedModel (bmid, mid)
                         VALUES (%s, %s)
                         """
        cur.execute(sql_command, (bmid, mid))
        conn.commit()
        return True
    except Exception as e:
        # Ed discussion said to return false if Base model that is referenced does not exist
        print(f"Failed to add CustomizedModel.\n{e}")

        # rollback changes in case of error
        if 'conn' in locals() and conn:
            conn.rollback()
        
        return False
    finally:
        cur.close()
        conn.close()

'''
Delete a base model and all referenced rows
'''
def deleteBaseModel(bmid):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # check if base model exists
        cur.execute("SELECT 1 FROM BaseModel WHERE bmid = %s", (bmid,))
        if not cur.fetchone():
            print(f"[DEBUG] BaseModel with bmid '{bmid}' does not exist.")
            return False
        
        # delete base model (cascade)
        cur.execute("DELETE FROM BaseModel WHERE bmid = %s", (bmid,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Failed to delete base model.\n{e}")

        # rollback changes in case of error
        if 'conn' in locals() and conn:
            conn.rollback()
            
        return False
    finally:
        cur.close()
        conn.close()

'''
Lists internet services used by base model
'''
def listInternetService(bmid):
    # e.g. test sql terminal command:
    """
    SELECT i.sid, i.endpoints, i.provider
        FROM InternetService AS i
        JOIN ModelServices AS ms ON ms.sid = i.sid
        WHERE ms.bmid = 2
        ORDER BY i.provider ASC;
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SELECT sid, endpoint, provider 
        # PROBLEM ITS NOT PRINTING IN ORDER AHH
        cur.execute(
            """
            SELECT i.sid, i.endpoints, i.provider
            FROM InternetService AS i
            JOIN ModelServices AS ms ON ms.sid = i.sid
            WHERE ms.bmid = %s
            ORDER BY i.provider ASC
            """,
            (bmid,)
        )

        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Failed to list internet service.\n{e}")  
        return []
    finally:
        cur.close()
        conn.close()

'''
Counts customized models per base model
'''
def countCustomizedModel(*bmids):
    # e.g. sql terminal command:
    """
    SELECT b.bmid, b.description, COUNT(c.mid) AS customizedModelCount
        FROM BaseModel AS b
        LEFT JOIN CustomizedModel AS c ON b.bmid = c.bmid
        WHERE b.bmid IN (2,3,1,0)
        GROUP BY b.bmid, b.description
        ORDER BY b.bmid ASC;
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        bmid_list = [int(x) for x in bmids]

        bmid_params = ",".join(["%s"] * len(bmid_list)) # since unknown amt of bmids

        # SELECT bmid, description, count
        sql_command =  f"""
        SELECT b.bmid, b.description, COUNT(c.mid) AS customizedModelCount
        FROM BaseModel AS b
        LEFT JOIN CustomizedModel AS c ON b.bmid = c.bmid
        WHERE b.bmid IN ({bmid_params})
        GROUP BY b.bmid, b.description
        ORDER BY b.bmid ASC
        """

        cur.execute(sql_command, tuple(bmid_list))

        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Failed to count customized model.\n{e}")
        return []
    finally:
        cur.close()
        conn.close()

'''
Shows top N longest duration configurations for a client
'''
def topNDurationConfig(uid, N):
    # e.g. sql terminal command:
    """
    SELECT c.client_uid AS uid, c.cid, c.labels, c.content, m.duration
        FROM Configuration AS c
        JOIN ModelConfigurations AS m ON c.cid = m.cid
        WHERE c.client_uid = 1
        ORDER BY m.duration DESC, c.cid ASC
        LIMIT 5;
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        uid = int(uid)
        N = int(N)

        # check that uid exists
        cur.execute("SELECT 1 FROM AgentClient WHERE uid = %s", (uid,))
        if not cur.fetchone():
            print(f"[DEBUG] Client with the uid '{uid}' does not exist.")
            return []

        # SELECT uid, cid, label, content, duration 
        sql_command = """
        SELECT c.client_uid AS uid, c.cid, c.labels, c.content, m.duration
        FROM Configuration AS c
        JOIN ModelConfigurations AS m ON c.cid = m.cid
        WHERE c.client_uid = %s 
        ORDER BY m.duration DESC, c.cid ASC
        LIMIT %s
        """

        cur.execute(sql_command, (uid, N))

        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Failed to get top N duration config.\n{e}")
        return []
    finally:
        cur.close()
        conn.close()

'''
Shows top 5 of base models for keyword search over LLMService
'''
def listBaseModelKeyWord(keyword):
    # e.g. sql terminal command:
    """
    SELECT b.bmid, i.sid, i.provider, l.domain
        FROM BaseModel AS b
        JOIN ModelServices AS m ON b.bmid = m.bmid
        JOIN LLMService AS l ON m.sid = l.sid
        JOIN InternetService AS i ON l.sid = i.sid
        WHERE l.domain LIKE 'video'
        ORDER BY b.bmid ASC
        LIMIT 5;
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        pattern = f"%{keyword}%"

        # SELECT bmid, sid, provider, domain
        sql_command = """
        SELECT b.bmid, i.sid, i.provider, l.domain
        FROM BaseModel AS b
        JOIN ModelServices AS m ON b.bmid = m.bmid
        JOIN LLMService AS l ON m.sid = l.sid
        JOIN InternetService AS i ON l.sid = i.sid
        WHERE l.domain LIKE %s
        ORDER BY b.bmid ASC
        LIMIT 5
        """

        cur.execute(sql_command, (pattern,))

        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Failed to list base model keyword.\n{e}")
        return []
    finally:
        cur.close()
        conn.close()

'''
Print NL2SQL results
'''
def printNL2SQLresult():
    csv_path = "NL2SQL.csv"

    if not os.path.exists(csv_path):
        return []

    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    return rows
