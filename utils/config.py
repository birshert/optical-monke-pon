from enum import Enum

import yaml
from pydantic import BaseModel


class DeployEnums(str, Enum):
    cog = 'cog'
    fast_api = 'fast_api'


class DeployConfig(BaseModel):
    deploy_type: DeployEnums
    deploy_port: int


class Config(BaseModel):
    deploy: DeployConfig


with open("config.yaml", "r") as f:
    config = Config(**yaml.safe_load(f.read()))
