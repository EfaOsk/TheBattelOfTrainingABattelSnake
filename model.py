# import a lot of stuff some usefull some not 
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim

from torchsummary import summary



# set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



Actions = ["up", "down", "left", "right"]
# Transition represents a single transition in our environment. 
# Maping (state, action) to its resulting (next_state, reward)
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):
    def __init__(self, capacity= 10000):
        self.memory = deque([],maxlen=capacity)

    def push(self, state, action, next_state, reward):
        '''Save a transition'''
        self.memory.append(Transition(state, action, next_state, reward))

    def sample(self, batch_size):
        '''Returns a random sample of the memory, of size batch_size'''
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)



class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        # in: {1, bs} x 11 x 11 out: 4
        self.model = nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(11*11, 32),
            nn.ReLU(),
            nn.Linear(32, 4))


    def forward(self, x):
        x = self.model(x)
        return nn.functional.log_softmax(x, dim=1)

model= SimpleModel()
summary(model,(1, 1, 11, 11))





# Train
BATCH_SIZE = 128
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10


policy_net = SimpleModel().to(device)
policy_net = policy_net.float()
target_net = SimpleModel().to(device)
target_net = target_net.float()
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.RMSprop(policy_net.parameters())
memory = ReplayMemory()

steps_done= 0


def reward(game_state):
    reward =0.0
    # If I won: reward = 100 else: reward = -100
    if game_state["you"]["health"]== 100:
        reward+=10.0
    else:
        reward+=1.0
    return reward


def select_action(game_state):
    global steps_done
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1

    # with high probabilty ask the model for the best action
    if random.random() > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            print(torch.tensor([[torch.argmax(policy_net(game_state.float()))]], device=device, dtype=torch.long))
            # print(torch.tensor([[a]], device=device, dtype=torch.long))


            # a= torch.tensor([[random.randrange(4)]], device=device, dtype=torch.long)
            # print(a)
            # return a
            # return a
            return torch.tensor([[torch.argmax(policy_net(game_state.float()))]], device=device, dtype=torch.long)
    else:   # Otherwise select random action
        a= torch.tensor([[random.randrange(4)]], device=device, dtype=torch.long)
        # print(a)
        return a

episode_durations = list()




def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    # if True:
    #     return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_net(state_batch.float()).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = target_net(non_final_next_states.float()).max(1)[0].detach()
    # next_state_values[non_final_mask] = target_net(non_final_next_states.float()).max(1)[0].detach()
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()

