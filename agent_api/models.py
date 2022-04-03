from enum import Enum
from pydantic import BaseModel
from typing import Optional




class AgentType(str,Enum):
    MQTT = "mqtt"
    MqttProducer = "mqttproducer"
    SystemMonitor = "systemmonitor"




class Kill(BaseModel):
    pid: int


class Start(BaseModel):
    component: AgentType  # producer /monitor
    conf: dict

class ReStart(BaseModel):
    component: str
    conf: dict

class Conf(BaseModel):
    broker: str
    port: int
    client_id: str
    username:  Optional[str]
    password: Optional[str]
    producer_topic: Optional[str]
    tracker_topic: Optional[str]
    monitor_topic: Optional[str]


class DetectorsConf(BaseModel):
    cd_class: str
    cd_threshold: int
    face_detection_model: str

    
