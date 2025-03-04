from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List

class UserBase(SQLModel):
    name: str = Field(index=True, unique=True)
    password: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    servers: List["Server"] = Relationship(back_populates="owner")

class ServerBase(SQLModel):
    name: str
    owner_id: Optional[int] = Field(foreign_key="user.id")

class Server(ServerBase, table=True):
    server_id: Optional[int] = Field(default=None, primary_key=True)
    owner: Optional[User] = Relationship(back_populates="servers")
    sensor_data: List["SensorData"] = Relationship(back_populates="server")

class SensorDataBase(SQLModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None
    server_id: Optional[int] = Field(foreign_key="server.server_id")

class SensorData(SensorDataBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    server: Optional[Server] = Relationship(back_populates="sensor_data")