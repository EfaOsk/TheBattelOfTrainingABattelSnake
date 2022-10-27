# The Battel Of Training A Battel Snake
# TODO: create a header

import typing
from model import *
from process_state import process_state



prev_move = None
prev_state = None


curr_live_time = 0

file_name_policy= "./models/policy_net.pt"
file_name_target= "./models/target_net.pt"



# info is called when you create your Battlesnake on play.battlesnake.com
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "EfaOskWaltteri",
        "color": "#FF1493", 
        "head": "safe",
        "tail": "block-bum", 
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    global curr_live_time
    # if Im still alive I won!
    i_won = False
    R=-100.0
    for snake in game_state["board"]["snakes"]:
        if game_state["you"]["id"] == snake["id"]:
            i_won= True
    if i_won:
        R= 100.0
    print(f"you survived for", curr_live_time ," / ",game_state["turn"], " turns")
    victory_log = open("victory_log_1.txt", "a")
    victory_log.write(str(i_won)+", ")
    victory_log.close()
    life_time_log = open("life_time_log_1.txt", "a")
    life_time_log.write(str(curr_live_time)+", ")
    life_time_log.close()
    curr_live_time=0
    R = torch.tensor([R], device=device)
    memory.push(prev_state, prev_move, process_state(game_state), R)
    optimize_model()
    target_net.load_state_dict(policy_net.state_dict())
    print("GAME OVER\n")
    torch.save(policy_net.state_dict(), file_name_policy)
    torch.save(target_net.state_dict(), file_name_target)


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    global curr_live_time
    global prev_move
    global prev_state
    
    curr_live_time+=1
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
