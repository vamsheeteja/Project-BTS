import sqlite3
from sqlite3 import Error

# the sqlite database
def create_connection(db_file):
    """ creates a db connection and returns connection object """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn 

# creates the table create_table_sql
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)

def main():
    database = r"C:\Users\Vamshee Teja\OneDrive\Desktop\testerdb.db"
    sql_create_bank_accounts = """ 
                            CREATE TABLE IF NOT EXISTS bank_accounts (
                                s_no INTEGER AUTO INCREMENT,
                                account INTEGER,
                                pin INTEGER, 
                                name TEXT,
                                age INTEGER,
                                balance INTEGER 
                            );
                        """
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_bank_accounts)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

def updateSqliteTable():
    print("in upd sql table")
    conn = create_connection("testerdb.db")
    cursor = conn.cursor()
    print("Connected to SQLite")
    pin = 342
    cursor.execute("SELECT * FROM bank_accounts WHERE pin=?", (pin,))

    rows = cursor.fetchall()
    print("rows")
    for row in rows:
        print(row)

    # sql_update_query = """UPDATE bank_accounts SET BALANCE = 10000 where id = 4"""
    # cursor.execute(sql_update_query)
    # sqliteConnection.commit()
    # print("Record Updated successfully ")
    cursor.close()
    print("The SQLite connection is closed")



updateSqliteTable()