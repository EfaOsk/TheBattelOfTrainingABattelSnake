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



Actions = {"up", "down", "left", "right"}
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
        super().__init__()
        # in: 3x11x11 out: 4
        self.model = nn.Sequential(
            # in: 3x11x11 out: 16x10x10
            nn.Conv2d(3, 16, kernel_size=4, padding=1),
            nn.ReLU(),
            # in: 16x10x10 out: 32x8x8
            nn.Conv2d(16, 32, kernel_size=3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32*8*8, 32),
            nn.Linear(32, 4))


    def forward(self, x):
        return nn.functional.log_softmax(self.model(x))

model= SimpleModel()
summary(model,(3, 11, 11))
