scalaVersion := "2.12.18"

name := "data-mart"
organization := "ch.epfl.scala"
version := "1.0"
fork := true

libraryDependencies += "org.rogach" %% "scallop" % "4.1.0"

// https://mvnrepository.com/artifact/com.microsoft.azure/spark-mssql-connector
libraryDependencies += "com.microsoft.azure" %% "spark-mssql-connector" % "1.3.0-BETA"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.3.2"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.3.2"
libraryDependencies += "org.apache.spark" %% "spark-mllib" % "3.3.2"
