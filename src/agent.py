import subprocess
import signal
import argparse
import dataclasses
import os
import logging


def _deploy_producer():
    pid = subprocess.Popen(
        ["python", "data_producer.py"]
    )
    return pid


def _deploy_device_tracker():
    subprocess.Popen(
        ["python","data_consumer.py"]
    )

class Agent(object):

    def __init__(self, conf):
        self.conf = conf
        self.pid = 0
        self.logger  = logging.getLogger(__name__)
    
    def start_producer(self):
        self.logger.info("Starting the producer")
        self.pid = _deploy_producer()  
    
    def kill_producer(self):
        if self.pid ==0:
            self.logger.warning("Producer PID was not in running state")
        self.logger.warning("Killing the producer")
        os.kill(self.pid)
        self.pid = 0
    
    def restart_prodcuer(self):
        self.kill_producer()
        self.start_producer()


class ProducerAgent(Agent):
    __name__ = "producer"
    pass


class TrackerAgent(Agent):
    __name__ = "tracker"
    pass

class MonitorAgent(Agent):
    __name__ = "monitor"
    pass

if __name__ == "__main__":

    agent = Agent()
