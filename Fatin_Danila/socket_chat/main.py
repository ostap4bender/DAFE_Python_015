import threading

# from client.consumer import run_client
from server_app.consumer import run_server


if __name__ == '__main__':
    run_server()
    # server = threading.Thread(target=run_server, args=(1,))
    # client = threading.Thread(target=run_client, args=(1,))
    # server.start()
    # client.start()
    # server.join()
    # client.join()
    # todo.append(threading.Thread(target=lambda: PID_VAV('B2').Controls, daemon=False))
    # todo.append(threading.Thread(target=lambda: PID_VAV('B4').mqttConnection, daemon=False))
    # for th in todo:
    #     th.start()
    # for th in todo:
    #     th.join()
