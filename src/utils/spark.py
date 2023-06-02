from threading import Event


def keep_spark_web_ui_alive():
    print('-------PROGRAM IS FINISHED-------')
    print('-------Press Ctrl+C to exit------')
    Event().wait()
