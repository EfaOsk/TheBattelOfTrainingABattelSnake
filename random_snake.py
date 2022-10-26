import random
import typing


def outofbound(x,y,W,H):
    """Cheacks if x,y is outof bound"""
    if x<0 or x>=W or y<0 or y>=H:
        return True
    return False

def is_snake_there(x,y,snakes, my_length):
    """Cheacks if there is a snake at x,y"""
    for snake in snakes:
        for body_part in range(snake["length"]):
            if (x == snake["body"][body_part]["x"]) and (y== snake["body"][body_part]["y"]):
                return True
    return False

def is_save_location(x,y, snakes, my_length, W, H):
    return not (outofbound(x,y,W,H) or is_snake_there(x,y,snakes, my_length))


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
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    snakes = game_state['board']['snakes']

    # Make the snake un suicidal
    if not is_save_location(my_head["x"]+1, my_head["y"], snakes, game_state["you"]["length"],board_width, board_height):
        is_move_safe["right"]=False
    if not is_save_location(my_head["x"]-1, my_head["y"], snakes, game_state["you"]["length"],board_width, board_height):
        is_move_safe["left"]=False
    if not is_save_location(my_head["x"], my_head["y"]+1, snakes, game_state["you"]["length"],board_width, board_height):  
        is_move_safe["up"]=False
    if not is_save_location(my_head["x"], my_head["y"]-1, snakes, game_state["you"]["length"],board_width, board_height):
        is_move_safe["down"]=False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: DeRandomize
    next_move = random.choice(safe_moves)


    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
