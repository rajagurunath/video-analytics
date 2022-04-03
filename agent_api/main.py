from fastapi.applications import FastAPI
from agent_api.models import AgentType, Start
from agent_api.models import Conf
from agent_api.func import Mqtt,MqttProducer,SystemMonitor
from fastapi.exceptions import HTTPException
from fastapi import BackgroundTasks
app = FastAPI(title="Agent")



"""

Agent was deployed as daemon

Agent has following abilities
-----------------------------
- deploy/kill/restart following agents
    - producer
    - device tracker
    - monitor 

- Modify configurations
    - modify configurations and restart the agents

"""
def exec_action(agent,action):
    if hasattr(agent,action):
        getattr(agent,action)()
    agent.process.wait()
    agent.process.communicate()

mqtt_agent = Mqtt()
mqtt_prod_agent = MqttProducer()
system_mon_agent = SystemMonitor()

@app.post("/agent/v1/deploy")
def deploy(conf:AgentType,background_tasks: BackgroundTasks):
    if conf.lower() =="mqtt":
        background_tasks.add_task(exec_action,mqtt_agent,"start")
    
    elif conf.lower() =="mqttproducer":
        # logger.info("starting mqttproducer")
        background_tasks.add_task(exec_action,mqtt_prod_agent,"start")
    
    elif conf.lower() =="systemmonitor":
        print("starting .....")
        background_tasks.add_task(exec_action,system_mon_agent,"start")
    
    else:
        raise HTTPException(status_code=404,detail="Given Agent not found")
    

    
@app.get("/agent/v1/restart/{id}")
def restart(conf:AgentType,background_tasks: BackgroundTasks):
    if conf.lower() =="mqtt":
        background_tasks.add_task(exec_action,mqtt_agent,"restart")
    
    elif conf.lower() =="mqttproducer":
        # logger.info("starting mqttproducer")
        background_tasks.add_task(exec_action,mqtt_prod_agent,"restart")
    
    elif conf.lower() =="systemmonitor":
        print("starting .....")
        background_tasks.add_task(exec_action,system_mon_agent,"restart")
    
    else:
        raise HTTPException(status_code=404,detail="Given Agent not found")
     

@app.delete("/agent/v1/{id}")
def delete(conf:AgentType,background_tasks: BackgroundTasks):
    if conf.lower() =="mqtt":
        background_tasks.add_task(exec_action,mqtt_agent,"kill")
    
    elif conf.lower() =="mqttproducer":
        # logger.info("starting mqttproducer")
        background_tasks.add_task(exec_action,mqtt_prod_agent,"kill")
    
    elif conf.lower() =="systemmonitor":
        print("starting .....")
        background_tasks.add_task(exec_action,system_mon_agent,"kill")
    
    else:
        raise HTTPException(status_code=404,detail="Given Agent not found")
     

def start():
    pass



