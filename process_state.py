import numpy as np
import torch

def process_state(state):
    """
    Transfroms state to a tensore
        state: 
        {"game": {}
            "id":,
            "ruleset":{"name":"standard","version":"cli",
            "settings":{...},
        "turn": ?,
        "board":{
            "height":11,
            "width":11,
            "snakes":[
                {"id": <snake ID>,
                    "name": <snake name>,
                    "latency":"0",
                    "health": [0:100],
                    "body":[{"x":a,"y":b},{"x":?,"y":?},..],
                    "head":{"x":a,"y":b},
                    "length":n,
                    "shout":"", # Does not seem to have any usefull info
                    "squad":"", # Not using this one
                    "customizations":{"color":"#FF1493","head":"safe","tail":"block-bum"} # Does not seem to have any usefull info
                }, { <snake 2 info> },
                 ... ],
            "food": [{"x":?,"y":?}, ...],
            "hazards":[] # Not using this one
            },
        "you": {"id":"dfc56876-9620-4c07-82fa-f1d206ac4e25","name":"Snake1", ...}
    """
    ret= np.zeros((3, 11,11))

    my_snake= ret[0]
    other_snakes= ret[1]
    food_table= ret[2]
    for snake in state["board"]["snakes"]:
        if snake["id"]== state["you"]["id"]:
            my_snake[10-snake["head"]["y"]][snake["head"]["x"]]=1
        else: 
            other_snakes[10-snake["head"]["y"]][snake["head"]["x"]]=1
        for body_part in snake["body"][1:]:
            if snake["id"]== state["you"]["id"]:
                my_snake[10-body_part["y"]][body_part["x"]]=0.5
            else: 
                other_snakes[10-body_part["y"]][body_part["x"]]=0.5
    
    for food in state["board"]["food"]:
        food_table[10-food["y"]][food["x"]]=1
    


    return torch.from_numpy(ret)
