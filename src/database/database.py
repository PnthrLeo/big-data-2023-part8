import pyodbc
from pyspark.sql import DataFrame, SparkSession

from database.db_config_generator import get_db_config


class Database:
    def __init__(self, config: dict = None):
        if config is None:
            config = get_db_config()

        cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server}'
                              +';SERVER='+config['db_ip']
                              +';PORT='+config['db_port']
                              +';DATABASE=master'
                              +';ENCRYPT=yes'
                              +';UID='+config['db_username']
                              +';PWD='+config['db_password'], autocommit=True)
        cursor = cnxn.cursor()
        
        try: 
            cursor.execute(f"CREATE DATABASE {config['db_database']}")
            print(f"Created database {config['db_database']}")
        except:
            print(f"Working with existing database {config['db_database']}")
        cursor.execute(f"USE {config['db_database']}")
                            
        self.cursor = cnxn.cursor()
        self.config = config
    
    def set_data(self, df: DataFrame, schema_name: str, table_name: str):
        try:
            self.cursor.execute(f"CREATE SCHEMA {schema_name}")
            print(f"Created schema {schema_name}")
        except:
            print(f"Writing to existing schema {schema_name}")
        
        # pyspark write data to sql server
        df.write \
            .format("jdbc") \
            .mode("overwrite") \
            .option("url", f"jdbc:sqlserver://{self.config['db_adress']};databaseName={self.config['db_database']};") \
            .option("dbtable", f"{schema_name}.{table_name}") \
            .option("user", self.config['db_username']) \
            .option("password", self.config['db_password']) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .save()
    
    def get_data(self, spark: SparkSession, schema_name: str, table_name: str) -> DataFrame:
        df = spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:sqlserver://{self.config['db_adress']};databaseName={self.config['db_database']};") \
            .option("dbtable", f"{schema_name}.{table_name}") \
            .option("user", self.config['db_username']) \
            .option("password", self.config['db_password']) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .load()
        return df
