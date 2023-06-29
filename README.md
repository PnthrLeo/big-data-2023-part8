# Витрина данных на Spark

## Цель работы
Целью данной работы является получение навыков разработки витрины данных и последующей её интеграции.

## Выполнение работы
1. В Dockerfile приложения был установлен SBT to build Scala projects.
2. На Scala был реализован функционал для работы с базой данных.
3. На Scala был реализован функционал для предобработки данных.
4. На Scala был реализован объект витрины данных.
5. Объект витрины данных был интегрирован в приложение на Python путём добавления собранного jar-файла в конфигурацию Spark.

## Запуск среды
Для запуска базы данных нужно выполнить следующую команду из корня репозитория:
1. `docker compose -f database/docker-compose.yaml up -d`

Для запуска среды приложения нужно выполнить следующие команды из корня репозитория:
1. `docker-compose build`
2. `docker-compose up -d`
3. `docker exec -i -t [container id] bash`

Далее, для запуска Jupyter Notebook (ноутбук будет доступен на порту 8888):
1. `jupyter notebook --ip 0.0.0.0 --no-browser --allow-root`

Для запуска скриптов нужно перейти в папку src Docker контейнера и выполнить команду:
1. `python [script name]`

Перед запуском `src/kmeans.py` нужно запустить `src/load_data_to_db.py` для заполнения базы данных.

Во время запущенного Jupyter Notebook вы можете перейти по адресу `localhost:4444` для доступа к Spark веб-интерфейсу.
Также доступ можно получить и при запуске `src`-кода, для этого нужно добавить вызов функции `keep_spark_web_ui_alive` из `utils.spark` перед закрытием `SparkSession`.

## Результаты работы
1. Была реализована и интегрирована витрина данных на Scala.
2. Был получен опыт написания скриптов на Scala.
3. Был получен опыт интеграции Scala-кода в PySpark-приложение.


minikube start --memory=12g --cpus=10
minikube mount ./:/app
kubectl apply -f proxy-net-networkpolicy.yaml,database-service.yaml,spark-service.yaml,database-deployment.yaml,spark-deployment.yaml
kubectl exec --stdin --tty [pod-name] -- /bin/bash
