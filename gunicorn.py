import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1

bind = '0.0.0.0:5000'

timeout = 60


proc_name = 'app'

pidfile = './app.pid'

errorlog = './gunicorn.log'

worker_connections = 100

# daemon = False

debug = True


