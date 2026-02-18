import os
import psycopg2


def run(config: dict) -> bool:
    try:
        print("Running DB Sync Job")

        table = config.get("table")
        batch_size = config.get("batch_size", 100)
        name = config.get("name") 

        if not table:
            raise ValueError("table is required")

        # Get DB credentials from environment
        host = os.getenv("DB_HOST")
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        port = os.getenv("DB_PORT", 5432)

        print(f"Connecting to DB at {host}")

        conn = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port
        )

        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                name TEXT
            );
        """)

        conn.commit()

        print(f"Table {table} ensured.")

        cursor.execute(
            f"INSERT INTO {table} (name) VALUES (%s) RETURNING id;",
            (name,) 
        )

        inserted_id = cursor.fetchone()[0]
        conn.commit()

        print(f"Inserted row with id: {inserted_id}")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print("Error:", str(e))
        return False
