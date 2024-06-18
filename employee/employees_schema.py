import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            department TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS hired_employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            datetime TEXT NOT NULL,
            department_id INTEGER,
            job_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    ''')

    conn.commit()
    conn.close()

#Generic function to insert data into any table 
def insert_data(table_name, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    placeholders = ', '.join(['?'] * len(data[0]))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"

    try:
        cursor.executemany(query, data)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error inserting into {table_name}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

