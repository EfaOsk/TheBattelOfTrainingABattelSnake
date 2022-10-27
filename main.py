# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
from model import *
from process_state import process_state

prev_move = None
prev_state = None

# BATCH_SIZE = 10
# GAMMA = 0.999
# EPS_START = 0.9
# EPS_END = 0.05
# EPS_DECAY = 200
# TARGET_UPDATE = 10


# policy_net = SimpleModel().to(device)
# target_net = SimpleModel().to(device)
# target_net.load_state_dict(policy_net.state_dict())
# target_net.eval()

# optimizer = optim.RMSprop(policy_net.parameters())
# memory = ReplayMemory()

# steps_done= 0




# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "EfaOsk",
        "color": "#FF1493", 
        "head": "safe",
        "tail": "block-bum", 
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    # if Im still alive I won!
    i_won = False
    R=-100.0
    for snake in game_state["board"]["snakes"]:
        if game_state["you"]["id"] == snake["id"]:
            i_won= True
    if i_won:
        R= 100.0
    R = torch.tensor([R], device=device)
    memory.push(prev_state, prev_move, process_state(game_state), R)
    optimize_model()
    target_net.load_state_dict(policy_net.state_dict())
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    global prev_move
    global prev_state
    if not (prev_move == None):
        R = torch.tensor([reward(game_state)], device=device)
        memory.push(prev_state, prev_move, process_state(game_state),R)
        optimize_model()
        target_net.load_state_dict(policy_net.state_dict())

    prev_state = process_state(game_state)
    next_move = select_action(prev_state)
    prev_move = next_move
    
    print(f"MOVE {game_state['turn']}: {Actions[int(next_move)]}")
    return {"move": Actions[int(next_move)]}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
