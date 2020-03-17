from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# connection = sqlite3.connect('dms.db')
# cursor = connection.cursor()
#
# create_user_table = ''' CREATE TABLE IF NOT EXISTS users(
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     email_address VARCHAR (50) NOT NULL UNIQUE,
#     password VARCHAR (20) NOT NULL,
#     role_id INT NOT NULL,
#     project_id INT NOT NULL,
#     create_date DATE,
#     update_date DATE,
#     delete_date DATE
#     )
# '''
#
# create_type_table = '''CREATE TABLE IF NOT EXISTS type(
#     id INTEGER PRIMARY KEY,
#     type_name VARCHAR(20) NOT NULL UNIQUE,
#     type_description VARCHAR (50) NOT NULL UNIQUE,
#     create_date DATE,
#     update_date DATE,
#     delete_date DATE
#     )
# '''
# cursor.execute(create_user_table)
# connection.commit()
#
# connection.close()
