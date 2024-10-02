--Multiple triggers for Sqlite3 

CREATE TRIGGER log_myapps_bookss_operations
AFTER INSERT ON myapps_bookss 
FOR EACH ROW 
BEGIN
    INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed) 
    VALUES (
        'INSERT INTO myapps_bookss (title, author, published_date) VALUES (''' || NEW.title || ''', ''' || NEW.author || ''', ''' || NEW.published_date || ''')',
        CURRENT_TIMESTAMP,
        0
    );
END;

CREATE TRIGGER log_myapps_bookss_operations_update
AFTER UPDATE ON myapps_bookss 
FOR EACH ROW 
BEGIN
    INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed) 
    VALUES (
        'UPDATE myapps_bookss SET title=''' || NEW.title || ''', author=''' || NEW.author || ''', published_date=''' || NEW.published_date || ''' WHERE id=' || NEW.id,
        CURRENT_TIMESTAMP,
        0
    );
END;

CREATE TRIGGER log_myapps_bookss_operations_delete 
AFTER DELETE ON myapps_bookss 
FOR EACH ROW 
BEGIN
    INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed) 
    VALUES (
        'DELETE FROM myapps_bookss WHERE id=' || OLD.id,
        CURRENT_TIMESTAMP,
        0
    );
END;







--- single trigger for Postgres

CREATE OR REPLACE FUNCTION log_myapps_bookss_operations()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed) 
        VALUES (
            CONCAT('INSERT INTO myapps_bookss (title, author, published_date) VALUES (''', NEW.title, ''', ''', NEW.author, ''', ''', NEW.published_date, ''')'),
            CURRENT_TIMESTAMP,
            0
        );
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed) 
        VALUES (
            CONCAT('UPDATE myapps_bookss SET title=''', NEW.title, ''', author=''', NEW.author, ''', published_date=''', NEW.published_date, ''' WHERE id=', NEW.id),
            CURRENT_TIMESTAMP,
            0
        );
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed) 
        VALUES (
            CONCAT('DELETE FROM myapps_bookss WHERE id=', OLD.id),
            CURRENT_TIMESTAMP,
            0
        );
    END IF;
    RETURN NULL; -- No need to return anything
END;
$$ LANGUAGE plpgsql;





-- Multiple trigger in MYSQL



DELIMITER $$

CREATE TRIGGER log_myapps_bookss_operations_insert
AFTER INSERT ON myapps_bookss
FOR EACH ROW
BEGIN
  INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed)
  VALUES (
    CONCAT('INSERT INTO myapps_bookss (title, author, published_date) VALUES (\'', NEW.title, '\', \'', NEW.author, '\', \'', NEW.published_date, '\')'),
    CURRENT_TIMESTAMP,
    0
  );
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER log_myapps_bookss_operations_update
AFTER UPDATE ON myapps_bookss
FOR EACH ROW
BEGIN
  INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed)
  VALUES (
    CONCAT('UPDATE myapps_bookss SET title=\'', NEW.title, '\', author=\'', NEW.author, '\', published_date=\'', NEW.published_date, '\' WHERE id=', NEW.id),
    CURRENT_TIMESTAMP,
    0
  );
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER log_myapps_bookss_operations_delete
AFTER DELETE ON myapps_bookss
FOR EACH ROW
BEGIN
  INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed)
  VALUES (
    CONCAT('DELETE FROM myapps_bookss WHERE id=', OLD.id),
    CURRENT_TIMESTAMP,
    0
  );
END$$

DELIMITER ;



---for Checking

-- DELIMITER $$

-- CREATE TRIGGER log_{model_name}_operations_{operation}
-- AFTER {operation} ON {model_name}
-- FOR EACH ROW
-- BEGIN
--   INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed)
--   VALUES (
--     CONCAT('{sql_query}'),
--     CURRENT_TIMESTAMP,
--     0
--   );
-- END$$

-- DELIMITER ;



DELIMITER $$

CREATE PROCEDURE log_table_operations(
    IN model_name VARCHAR(255),
    IN operation_type VARCHAR(50),
    IN raw_sql_query TEXT
)
BEGIN
    -- Log the operation with the model name, operation type, and the raw SQL query
    INSERT INTO myapps_operationquery (sql_query, created_datetime, is_processed)
    VALUES (
        CONCAT(raw_sql_query),
        CURRENT_TIMESTAMP,
        0
    );
END$$

DELIMITER ;