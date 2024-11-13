import pygame
from pygame.gfxdraw import line,filled_polygon
from ..pygame import got_quit_event
from datetime import datetime
from dataclasses import dataclass
from ...utils import Vector2

@dataclass
class Car:
    pos : Vector2
    orientation : float
    speed : float
    steering_angle : float

def draw_env(screen,env):
    pass

def draw_car(screen,car):
    pass

def display_info(screen,font,car):
    pass

def get_actions(events):
    return None

def run_interactive(env, initial_state=None, scale=50, fullscreen = False):
    print('starting interactive car-parking simulation')
    car_config = env.get_info().car
    env_config = env.get_info().environment
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    if fullscreen:
        pygame.display.toggle_fullscreen()
    else:
        pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    background=0,0,0
    font = pygame.font.SysFont("Arial", 20)
    t0 = t1 = datetime.now()
    
    car = Car()
    while True:
        events = pygame.event.get()
        if got_quit_event(events):
            break
        screen.fill(background)
        actions = get_actions(events)
        car.update(actions,(t1-t0).total_seconds())
        draw_env(screen,env)
        draw_car(screen,car)
        display_info(screen,font,car)
        pygame.display.flip()
        t0 = t1
        t1 = datetime.now()
    pygame.quit()