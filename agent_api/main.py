from fastapi.applications import FastAPI


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