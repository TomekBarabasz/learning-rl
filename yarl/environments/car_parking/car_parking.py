from ..environment import environment
from ...utils import readConfig

from math import pi
from pathlib import Path

def bbox_range(bbox,coord):  return bbox[0][coord],bbox[1][coord]
def bbox_xrange(bbox):  return bbox_range(bbox,0)
def bbox_yrange(bbox):  return bbox_range(bbox,1)

class EnvInfo:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)

        self.action_space = [
            ('accelerate' , (-5,0,+5)),
            ('turn' , (-5,0,5))
        ]
        
        self.state_space = [
            ('position_x'    , bbox_xrange(self.environment.bounding_box)),
            ('position_y'    , bbox_yrange(self.environment.bounding_box)),
            ('orientation'   , (0.,360.)),
            ('speed'         , (-self.car.max_speed,self.car.max_speed)),
            ('steering_angle', (-self.car.max_steering_angle,self.car.max_steering_angle))
        ]

class car_parking_env(environment):
    def __init__(self,**kwargs):
        folder = Path(__file__).resolve().parent
        car_name = kwargs.get('car','small')
        car_cfg=readConfig(folder / 'cars' / f'{car_name}.json')
        env_name = kwargs.get('env','perpendicular')
        env_cfg=readConfig(folder / 'env' / f'{env_name}.json')
        self.info = EnvInfo(car=car_cfg.car,\
                            environment=env_cfg.environment,\
                            target_state = env_cfg.target_state)

    def get_info(self):
        return self.info

    def reset_to_random(self):
        raise NotImplementedError

    def initialize(self, *state):
        raise NotImplementedError
    
    def step(self, *actions):
        raise NotImplementedError
