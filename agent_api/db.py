from typing import Optional,Dict

from sqlmodel import Field, SQLModel


class Catalog(SQLModel, table=True):
    agent_name: str 
    process_id : int 
    conf:Dict
    
