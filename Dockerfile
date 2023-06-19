FROM python:3.9.1

# Versions
ENV SPARK_VERSION=3.3.2 \
    HADOOP_VERSION=3 \
    JAVA_VERSION=11 \
    PY4J_VERSION=0.10.9.7 \
    SCALA_VERSION=2.12.18

ENV JAVA_FULL_VERSION=${JAVA_VERSION}.0.2

RUN apt-get update \
    && apt-get install ca-certificates curl wget \
    && apt-get install -y lsb-release \
    && apt-get clean

RUN pip install --upgrade pip  \
    && pip install pandas \
    && pip install py4j==${PY4J_VERSION} \
    && pip install notebook findspark

# Install Mucrosoft ODBC Driver for debian
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get install -y unixodbc-dev

# Set Java environment variables
ENV JAVA_HOME="/home/jdk-${JAVA_FULL_VERSION}"
ENV PATH = "${PATH}:${JAVA_HOME}/bin"

# Download JDK and install
RUN DOWNLOAD_URL="https://download.java.net/java/GA/jdk${JAVA_VERSION}/9/GPL/openjdk-${JAVA_FULL_VERSION}_linux-x64_bin.tar.gz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl "${DOWNLOAD_URL}" --output "${TMP_DIR}/openjdk.tar.gz" \
    && mkdir -p "${JAVA_HOME}" \
    && tar -xzf "${TMP_DIR}/openjdk.tar.gz" -C "${JAVA_HOME}" --strip-components=1 \
    && rm -rf "${TMP_DIR}" \
    && java --version

# Set Spark environment variables
ENV SPARK_HOME="/home/spark"
ENV PATH="${PATH}:${SPARK_HOME}/bin"

# Download Spark and install
RUN DOWNLOAD_URL="https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl "${DOWNLOAD_URL}" --output "${TMP_DIR}/spark.tgz" \
    && mkdir -p "${SPARK_HOME}" \
    && tar -xzf "${TMP_DIR}/spark.tgz" -C "${SPARK_HOME}" --strip-components=1 \
    && rm -rf "${TMP_DIR}" \
    && spark-submit --version

# Set pyspark environment variables
ENV PYTHONPATH="${SPARK_HOME}/python:${PYTHONPATH}"

# Set Scala environment variables
ENV SCALA_HOME="/home/scala"
ENV PATH="${PATH}:${SCALA_HOME}/bin"

# Download Scala and install
RUN DOWNLOAD_URL="https://downloads.lightbend.com/scala/2.12.18/scala-2.12.18.tgz" \
    && TMP_DIR="$(mktemp -d)" \
    && curl "${DOWNLOAD_URL}" --output "${TMP_DIR}/scala.tgz" \
    && mkdir -p "${SCALA_HOME}" \
    && tar -xzf "${TMP_DIR}/scala.tgz" -C "${SCALA_HOME}" --strip-components=1 \
    && rm -rf "${TMP_DIR}" \
    && scala -version

# Download mssql connector for pyspark
RUN DOWNLOAD_URL="https://repo1.maven.org/maven2/com/microsoft/azure/spark-mssql-connector_2.12/1.3.0-BETA/spark-mssql-connector_2.12-1.3.0-BETA.jar" \
    && TMP_DIR="$(mktemp -d)" \
    && curl "${DOWNLOAD_URL}" --output "${TMP_DIR}/spark-mssql-connector.jar" \
    && mkdir -p "${SPARK_HOME}/jars" \
    && mv "${TMP_DIR}/spark-mssql-connector.jar" "${SPARK_HOME}/jars" \
    && rm -rf "${TMP_DIR}"

RUN DOWNLOAD_URL="https://github.com/microsoft/mssql-jdbc/releases/download/v11.2.0/mssql-jdbc-11.2.0.jre11.jar" \
    && TMP_DIR="$(mktemp -d)" \
    && curl "${DOWNLOAD_URL}" --output "${TMP_DIR}/ojdbc11.jar" \
    && mkdir -p "${SPARK_HOME}/jars" \
    && mv "${TMP_DIR}/ojdbc11.jar" "${SPARK_HOME}/jars" \
    && rm -rf "${TMP_DIR}"

# Add folder with mssql connector to PATH
ENV PATH="${PATH}:${SPARK_HOME}/jars"

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Container will run as a non-root user by default
USER $NB_UID
