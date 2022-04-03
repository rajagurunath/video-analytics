from agent_api.custom_logger import logger
import subprocess
from subprocess import Popen
from typing import List
import os
import time


def run(cmd:List[str]):
    parent = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=-1,
        universal_newlines=True,
        
    )
    return parent

class BaseProcess(object):
    def __init__(self,**kwargs) -> None:
        self.process = None
    
    def start(self,**kwargs):
        raise NotImplementedError

    def kill(self):
        self.logger.info(f"Killing the process {self.process.pid}")
        self.process.kill()

    def restart(self):
        self.kill()
        self.start()
    
    def monitor(self,timeout=2):
        """
        monitor for given timeout 
        """
        self.logger.info(f"Monitoring the logs {self.process.pid}")
        self.logger.info("===============================")
        start = time.time()
        for out in self.process.stdout:
            if time.time() > start + timeout:
                break
            self.logger.info(out)

class Mqtt(BaseProcess):
    def __init__(self,dir=None,filename=None,conf=None) -> None:
    
        self.dir=os.path.join(os.getcwd(),"mqtt")
        self.filename = "start.sh"
        self.process = None
        self.logger = logger
        self.port = 1883
    
    def start(self):
        self.logger.info("Starting the MQTT")
        # self.process = run(["/bin/sh",os.path.join(self.dir,self.filename)])
        self.process = run(["/usr/local/opt/mosquitto/sbin/mosquitto",
                            "-c", "/usr/local/etc/mosquitto/mosquitto.conf","-d"])
    # def kill(self):
    #     kill_command = "kill -9 $(lsof -i tcp:{} ".format(self.port)
    #     kill_command += "| awk '/mosquitto/ {print $2}')"
    #     self.kill_process = run([kill_command])
        # return self.kill_process.poll()


    def monitor(self, timeout=2):
        raise Exception("Dont use it")

class MqttProducer(BaseProcess):
    def __init__(self,dir=None,filename=None,conf=None) -> None:
        
        self.dir=os.path.join(os.getcwd(),"src")
        self.filename = "eink_producer.py"
        self.process = None
        self.logger = logger


    def start(self):
        self.logger.info("Starting the MQTTProducer")
        self.logger.info(os.path.join(self.dir))
        os.chdir(self.dir)
        self.process = run(["python",os.path.join(self.dir,self.filename)])

class SystemMonitor(BaseProcess):
    def __init__(self, dir=None,filename=None,conf=None) -> None:
        self.dir=os.path.join(os.getcwd(),"monitoring")
        self.filename = "metrics_publisher.py"
        self.process = None
        self.logger = logger
    def start(self):
        self.logger.info("Starting the SystemMonitor")
        self.process = run(["python",os.path.join(self.dir,self.filename)])
        print(self.dir)



if __name__ =="__main__":

    bus = Mqtt()
    bus.start()
    print(bus.process.pid)

    prod = MqttProducer()
    prod.start()
    print(prod.process.pid)
    prod.monitor(timeout=15)
    # prod.kill()
    # prod.restart()
    # prod.monitor()
    # prod.kill()
    # prod.monitor()
    # prod.monitor()
    # prod.monitor()
    # prod2= SystemMonitor()
    # prod2.start()
    # print(prod2.process.pid)
    # prod2.monitor()
    # bus.kill()



