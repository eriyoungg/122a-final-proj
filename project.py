import sys
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)

print(mydb)

def process_stream(stream, fout):
    for raw in stream:
        line = raw.strip()
        if not line:
            continue
        
        function = line[0]
        params = line[1:]

    pass

if __name__ == '__main__':
    # Assume input will ALWAYS be in correct format
    try:
        while True:
            line = input()
            if not line:
                continue
            if process_stream([line], sys.stdout) == -1:
                break
    except EOFError:
        pass