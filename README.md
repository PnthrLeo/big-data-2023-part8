# Миграция на Kubernetes

## Цель работы
Целью данной работы является получение навыков оркестрации контейнеров с использованием Kubernetes путём миграции сервиса модели на PySpark, сервиса витрины на Spark и сервиса источника данных.

## Выполнение работы
1. Создана среда со Spark и настроена её репликация.
2. Создана среда с базой данных.
3. Проверена работаспособность инфраструктуры на k8s (spark, data mart, database).

## Запуск среды
Для запуска среды нужно выполнить следующие команды:
1. `minikube start --memory=12g --cpus=10`
2. `minikube mount ./:/app`
3. `kubectl apply -f proxy-net-networkpolicy.yaml,database-service.yaml,spark-service.yaml,database-deployment.yaml,spark-deployment.yaml`
4. `kubectl exec --stdin --tty [pod-name] -- /bin/bash`

Далее, для запуска Jupyter Notebook (ноутбук будет доступен на порту 8888):
1. `jupyter notebook --ip 0.0.0.0 --no-browser --allow-root`

Для запуска скриптов нужно перейти в папку src Docker контейнера и выполнить команду:
1. `python [script name]`

Перед запуском `src/kmeans.py` нужно запустить `src/load_data_to_db.py` для заполнения базы данных.

Во время запущенного Jupyter Notebook вы можете перейти по адресу `localhost:4444` для доступа к Spark веб-интерфейсу (перед этим необходимо открыть порт через minikube командой `kubectl port-forward [pod-name] 4444`).
Также доступ можно получить и при запуске `src`-кода, для этого нужно добавить вызов функции `keep_spark_web_ui_alive` из `utils.spark` перед закрытием `SparkSession`.

## Результаты работы
1. Были получены скрипты для реализации Kubernetes-инфраструктуры.
2. Были получены навыки работы с Kubernetes.
