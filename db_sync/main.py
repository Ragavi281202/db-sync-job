import os
import psycopg2
import logging

logger = logging.getLogger(__name__)

def run(config: dict) -> bool:
    try:
        logger.info("Running DB Sync Job")

        table_name = config.get("table_name")
        name = config.get("name") 

        if not table_name:
            raise ValueError("table name is required")

        host = os.getenv("DB_HOST")
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        port = os.getenv("DB_PORT", 5432)

        logger.info(f"Connecting to DB at {host}")

        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port
        )

        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                name TEXT
            );
        """)

        conn.commit()

        logger.info(f"Table {table_name} ensured.")

        cursor.execute(
            f"INSERT INTO {table_name} (name) VALUES (%s) RETURNING id;",
            (name,) 
        )

        inserted_id = cursor.fetchone()[0]
        conn.commit()

        logger.info(f"Inserted row with id: {inserted_id}")

        cursor.close()
        conn.close()

        logger.info("DB Sync Job completed successfully")

        return True

    except Exception as e:
        logger.error("Error occurred: %s", str(e))
        return False
