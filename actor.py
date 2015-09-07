
import multiprocessing
import os
import random
import time
from util.core import str_utcnow

class ActorEngine(object): # spawns and controls workers and services

    def __init__(self):
        self.actor_count = 0
        self.actor_dict = {} # name : actor_object
        self.worker_jobs = []

    def new_actor(self, **kwargs):
        if not 'target' in kwargs:
            raise Exception("C'mon bra. I need a target function.")
        target = kwargs['target']
        if not 'args' in kwargs:
            p = multiprocessing.Process(target=target)
        else:
            args = kwargs['args']
            p = multiprocessing.Process(target=target, args=args)
        self.worker_jobs.append(p)
        print("WAIT, MY REAL NAME IS ", p.name)
        name = 'Worker' + str(self.actor_count)
        self.actor_count += 1
        self.actor_dict[name] = p
        p.start()

    def worker(self, **kwargs):
        pid = os.getpid()
        name = 'Actor ' + str(self.actor_count) +  ' PID: ' + str(pid)
        print('{} starting up, Timestamp:'.format(name), str_utcnow())
        for i in range(15):
            print(name, 'checking in', str_utcnow())
            rand = random.randint(1,5)
            print(name, "Sleeping for", str(rand), "seconds...")
            time.sleep(rand)
        print(name, 'shutting down', str_utcnow())
        return

if __name__ == '__main__':
    eng = ActorEngine()
    for i in range(5):
        eng.new_actor(target=eng.worker)
