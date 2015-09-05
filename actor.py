import threading
import time

def worker():
    print(threading.currentThread().getName(), 'Starting')
    time.sleep(2)
    print(threading.currentThread().getName(), 'Exiting')

def my_service():
    print(threading.currentThread().getName(), 'Starting')
    time.sleep(3)
    print(threading.currentThread().getName(), 'Exiting')

class ActorEngine(object): # spawns and controls workers and services

    def __init__(self):
        self.actor_count = 0
        self.actor_dict = {}

    def new_actor(self, name, target):
        if name in self.actor_dict:
            raise Exception(
                'New actor creation failed, actor named "' + 
                str(name) +
                '" already exists. actor.name must be unique.'
                )
        actor = threading.Thread(name=name, target=target)
        actor.start()
        self.actor_count += 1
        self.actor_dict[name] = actor
        return actor
# t = threading.Thread(name='my_service', target=my_service)
# w = threading.Thread(name='worker', target=worker)
# w2 = threading.Thread(target=worker) # use default name

# w.start()
# w2.start()
# t.start()

# USE
# from actor import ActorEngine, worker
# eng = ActorEngine()
# worker01 = eng.new_actor("worker01", worker)