import os


def get_db_config() -> dict:
    return {
        "db_adress": os.environ["DB_ADRESS"],
        "db_ip": os.environ["DB_IP"],
        "db_port": os.environ["DB_PORT"],
        "db_database": os.environ["DB_DATABASE"],
        "db_username": os.environ["DB_USERNAME"],
        "db_password": os.environ["DB_PASSWORD"],
    }
