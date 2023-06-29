package datamart

import sys.env

class EnvReader {
    val db_adress = env("DB_ADRESS")
    val db_ip = env("DB_IP")
    val db_port = env("DB_PORT")
    val db_database = env("DB_DATABASE")
    val db_username = env("DB_USERNAME")
    val db_password = env("DB_PASSWORD")
}
