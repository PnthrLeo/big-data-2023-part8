from py4j.java_gateway import JavaGateway

# Open JVM interface with the JDBC Jar
jdbc_jar_path = '/home/spark/jars/spark-mssql-connector.jar'
gateway = JavaGateway.launch_gateway(classpath=jdbc_jar_path) 

# Load the JDBC Jar
jdbc_class = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
gateway.jvm.Class.forName(jdbc_class)

# Initiate connection
jdbc_uri = "jdbc:sqlserver://database:1433"
con =  gateway.jvm.DriverManager.getConnection(jdbc_uri)

# Run a query
sql = "select this from that"
stmt = con.createStatement(sql)
rs = stmt.executeQuery()
while rs.next():
    rs.getInt(1)
    rs.getFloat(2)

rs.close()
stmt.close()
