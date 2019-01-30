# Toe-Tac-Tic
The reversed rule version of Tic-Tac-Toe. You can win if NPC wins in Tic-Tac-Toe.

For example, if board is like the one below you are the winner.

```
O: You
X: NPC
|X|O|X|
|X|X|O|
|O|O|X|
```


# Play
```
python main.py LEVEL
```

You can choose the level 0 to 2.


# For Reinforcement Learning
Perhaps it could be used as follows for reinforcement learning.

```python
from ToeTacTicEnvironment import main

env = ToeTacTicEnvironment()
env.reset()

done, obs = False, env.reset()

while not done:
    a = agent.act(obs)
    obs, r, done, _ = env.step(a)
    env.render()
```
