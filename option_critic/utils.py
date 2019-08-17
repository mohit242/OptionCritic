import torch
import numpy as np
import gym


def soft_update(target, source, polyak=0.001):
    for target_param, local_param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(polyak * local_param.data + (1.0 - polyak) * target_param.data)


def hard_update(target, source):
    for target_param, local_param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(local_param.data)


class ActionSACWrapper(gym.ActionWrapper):

    def __init__(self, env):
        """Changes action space range from [action_space.low, action_space.high] to [-1,1]"""
        self.env = env
        super().__init__(env)
        self.action_space = env.action_space
        self.action_space.low = -np.ones_like(env.action_space.low)
        self.action_space.high = np.ones_like(env.action_space.high)

    def action(self, action):
        action = (action * (self.env.action_space.high - self.env.action_space.low)/2) +\
                 (self.env.action_space.high + self.env.action_space.low)/2
        return action


class DiscreteToBox(gym.ObservationWrapper):

    def __init__(self, env: gym.Env):
        """Converts discrete observation to one-hot box observation"""
        super().__init__(env)
        self.observation_space = gym.spaces.Box(0, 1, (env.observation_space.n, ))
        self._observation_map = np.eye(env.observation_space.n)

    def observation(self, observation):
        obs = tuple(self._observation_map[observation])
        return obs


def create_obs_wrapper(n):
    _obs_map = np.eye(n)

    def _obs_wrapper(obs):
        return _obs_map[obs]

    return _obs_wrapper




