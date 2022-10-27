import matplotlib.pyplot as plt
import numpy as np

victory_log = open("life_time_log.txt", "r")
L = victory_log.readline().split(', ')
victory_log.close()
victory_log = open("victory_log.txt", "r")
V = victory_log.readline().split(', ')
victory_log.close()

# xpoints = np.array([0, len(L)-1])


plt.plot(range(0,len(L)), L, 'o')
for b in range(len(V)):
    if V[b]== "True":
        plt.plot(b,L[b],'rx')

plt.xlabel("#matches")
plt.ylabel("survival time")
plt.show()

print(str(V.count("True"))+ " victories out of "+ str(len(V))+" matches")

