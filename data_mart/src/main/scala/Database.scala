package datamart

import java.sql.DriverManager
import java.sql.Connection
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.DataFrame
import datamart.EnvReader


class Database {
    var spark: SparkSession = null;

    private var connection: Connection = null;
    private var db_ip: String = null;
    private var db_port: String = null;
    private var db_database: String = null;
    private var db_username: String = null;
    private var db_password: String = null;

    def this(config: EnvReader) = {
        this()
        db_ip = config.db_ip
        db_port = config.db_port
        db_database = config.db_database
        db_username = config.db_username
        db_password = config.db_password
        init_db()
    }

    def this(db_ip: String, db_port: String, db_database: String, db_username: String, db_password: String) = {
        this()
        this.db_ip = db_ip
        this.db_port = db_port
        this.db_database = db_database
        this.db_username = db_username
        this.db_password = db_password
        init_db()
    }

    def init_db(): Unit = {
        val url = s"""jdbc:sqlserver://$db_ip:$db_port;
                databaseName=master;
                user=$db_username;
                password=$db_password;
                encrypt=false;"""
        connection = DriverManager.getConnection(url)
        spark = SparkSession.builder().master("local[*]")
            .appName("KMeansClustering")
            .config("spark.num.executors", "2")
            .config("spark.executor.cores", "5")
            .config("spark.executor.memory", "5g")
            .config("spark.driver.memory", "5g")
            .getOrCreate()

        DriverManager.registerDriver(new com.microsoft.sqlserver.jdbc.SQLServerDriver());
        // we can form this below URL in different forms to encrypt our password and DBName

        try {
            val statement = connection.createStatement()
            val resultSet = statement.executeQuery(s"CREATE DATABASE $db_database")
            println(s"Created database $db_database")
        } catch {
            case e: Exception => println(s"Database $db_database already exists")
        }
    }

    def set_data(df: DataFrame, schema_name: String, table_name: String): Unit = {
        try {
            val statement = connection.createStatement()
            val resultSet = statement.executeQuery("CREATE SCHEMA " + schema_name)
            println("Created schema " + schema_name)
        } catch {
            case e: Exception => println("Writing to existing schema " + schema_name)
        }

        df.write
            .format("jdbc")
            .mode("overwrite")
            .option("url", s"jdbc:sqlserver://$db_ip:$db_port;databaseName=$db_database;")
            .option("dbtable", s"$schema_name.$table_name")
            .option("user", db_username)
            .option("password", db_password)
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
            .option("encrypt", "false")
            .save()
    }

    def get_data(schema_name: String, table_name: String): DataFrame = {
        val df = spark.read
            .format("jdbc")
            .option("url", s"jdbc:sqlserver://$db_ip:$db_port;databaseName=$db_database;")
            .option("dbtable", s"$schema_name.$table_name")
            .option("user", db_username)
            .option("password", db_password)
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
            .option("encrypt", "false")
            .load()
        return df
    }
}
