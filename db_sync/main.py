def run(config: dict) -> bool:
    try:
        print("Running DB Sync Job")

        table = config.get("table")
        batch_size = config.get("batch_size", 100)

        if not table:
            raise ValueError("table is required")

        print(f"Syncing table {table} with batch size {batch_size}")

        return True

    except Exception as e:
        print("Error:", str(e))
        return False
