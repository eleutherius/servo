"""
It's a simple script to set up pwm engine
"""
import typer
import toml
import os 
from .default_config import def_config
from .motor_drives import *
from .websocketruner import *

app = typer.Typer(help="Awesome CLI IPMP universal tool.")

import logging
from systemd.journal import JournaldLogHandler



logger = logging.getLogger("pwm_manage")
journald_handler = JournaldLogHandler()

# set a formatter to include the level name
journald_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(message)s'
    ))

# add the journald handler to the current logger
logger.addHandler(journald_handler)
logger.addHandler(logging.StreamHandler())

# optionally set the logging level
logger.setLevel(logging.DEBUG)


@app.command()
def init():
    """
    Create redundancy.toml config file

    Example of using:
    redundancy init
    """
    if not os.path.isfile("config.toml"):
        print(f"Generate config.toml config file")
        with open("config.toml", 'w') as f:
            f.write(def_config)


@app.command()
def start(conf: str = typer.Option("/etc/pwm/config.toml", help="PWM config.", show_default=True)
             ):
    """
    Use for the start PWM manager 

    Example of using:
    pwm start --conf=/etc/pwm/config.toml
    """
    config: str

    if conf is None:
        if os.path.isfile("./config.toml"):
            config =  "./config.toml"
        if not os.path.isfile("./config.toml"):
            print("Config file not exists!")
            exit(2)
    if conf is not None:
        config = conf

    config = toml.load(config)
    if config['pwm_type'] == "standart":
        StandartPWM.logger = logger
        engine = StandartPWM
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

    elif config['pwm_type'] == "L292N":
        StandartPWM.logger = logger
        engine = L298N
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

    elif config['pwm_type'] == "DouL292N":
        StandartPWM.logger = logger
        engine = DL298N
        runner = WebSoketRunner(logger=logger, engine=engine)
        runner.start()

if __name__ == '__main__':
    app()
