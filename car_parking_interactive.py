from yarl.environments import make_environment
from yarl.presentation.car_parking import run_interactive

env = make_environment('car-parking',car='small',env='perpendicular')

run_interactive(env)

