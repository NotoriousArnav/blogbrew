"""
gunicorn WSGI server configuration.
"""
from multiprocessing import cpu_count
from os import environ, path

def check_db(db_name='db.sqlite3'):
    import sqlite3

    # Replace 'your_database.db' with the path to your SQLite database file
    database_file = db_name

    # Try to connect to the SQLite database
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        # Check for the presence of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if tables:
            print("The database contains the following tables:")
            for table in tables:
                print(table[0])
            return True
        else:
            print("The database does not contain any tables.")
            return False

    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")
        raise e

    finally:
        if conn:
            conn.close()

if (not check_db()) or (not path.exists('.skip_message')):
    print("""
Welcome to Bromine.
We advise you to run migrations, if you are using default settings for Database (sqlite3),
Otherwise you can Ignore this Message and continue.

To skip this message:
    $ touch .skip_message
    """)
bind = '0.0.0.0:' + environ.get('PORT', '8000')
# workers = cpu_count()

# Add the --reload option
reload = True

# Specify the default application
default_proc_name = 'blogapp.wsgi:application'

# Add the Gevent worker class
worker_class = 'gevent'
