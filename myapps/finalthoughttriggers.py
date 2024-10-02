# call the procedure through triggers and for that creation of triggers dynamically ----step 2

import MySQLdb

# Connect to the database
db = MySQLdb.connect(host="localhost", user="user", passwd="password", db="your_database")
cursor = db.cursor()

# Get all table names
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    # Create INSERT trigger
    cursor.execute(f"""
        CREATE TRIGGER before_insert_{table}
        BEFORE INSERT ON {table}
        FOR EACH ROW
        BEGIN
            CALL log_table_operations(
                '{table}', 'INSERT',
                CONCAT('INSERT INTO {table} (...) VALUES (...)')
            );
        END;
    """)

    # Create UPDATE trigger
    cursor.execute(f"""
        CREATE TRIGGER before_update_{table}
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        BEGIN
            CALL log_table_operations(
                '{table}', 'UPDATE',
                CONCAT('UPDATE {table} SET ... WHERE id = ', OLD.id)
            );
        END;
    """)

    # Create DELETE trigger
    cursor.execute(f"""
        CREATE TRIGGER before_delete_{table}
        BEFORE DELETE ON {table}
        FOR EACH ROW
        BEGIN
            CALL log_table_operations(
                '{table}', 'DELETE',
                CONCAT('DELETE FROM {table} WHERE id = ', OLD.id)
            );
        END;
    """)

db.commit()
cursor.close()
db.close()



#updated  step - 2


import MySQLdb

# Connect to the database
db = MySQLdb.connect(host="localhost", user="user", passwd="password", db="your_database")
cursor = db.cursor()

# Get all table names
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    # Get column names for the table
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA = 'your_database'")
    columns = [row[0] for row in cursor.fetchall()]

    # Prepare the list of columns and corresponding NEW and OLD values for the triggers
    columns_list = ", ".join(columns)
    new_values_list = ", ".join([f"NEW.{col}" for col in columns])
    old_values_list = ", ".join([f"OLD.{col}" for col in columns])

    # Create INSERT trigger
    cursor.execute(f"""
        CREATE TRIGGER before_insert_{table}
        BEFORE INSERT ON {table}
        FOR EACH ROW
        BEGIN
            CALL log_table_operations(
                '{table}', 'INSERT',
                CONCAT('INSERT INTO {table} ({columns_list}) VALUES (', {new_values_list}, ')')
            );
        END;
    """)

    # Create UPDATE trigger
    cursor.execute(f"""
        CREATE TRIGGER before_update_{table}
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        BEGIN
            CALL log_table_operations(
                '{table}', 'UPDATE',
                CONCAT('UPDATE {table} SET ', 
                    {", ".join([f"{col} = NEW.{col}" for col in columns])}, 
                    ' WHERE id = ', OLD.id)
            );
        END;
    """)

    # Create DELETE trigger
    cursor.execute(f"""
        CREATE TRIGGER before_delete_{table}
        BEFORE DELETE ON {table}
        FOR EACH ROW
        BEGIN
            CALL log_table_operations(
                '{table}', 'DELETE',
                CONCAT('DELETE FROM {table} WHERE id = ', OLD.id)
            );
        END;
    """)

db.commit()
cursor.close()
db.close()









#MYSQL procedure creation   ----- step -1

# DELIMITER $$
# 
# CREATE PROCEDURE log_table_operations(
    # IN table_name VARCHAR(255),
    # IN operation_type VARCHAR(10),
    # IN sql_query TEXT
# )
# BEGIN
    # INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed)
    # VALUES (sql_query, CURRENT_TIMESTAMP, 0);
# END$$
# 
# DELIMITER ;
# 