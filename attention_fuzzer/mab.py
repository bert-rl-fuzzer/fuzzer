import logging
from abc import (
    ABC,
)
from collections import defaultdict
from typing import List
from uuid import uuid4

import numpy as np

logger = logging.getLogger(__name__)


class BernoulliBandit:
    def __init__(self, encoded_sent: List[int]):
        """
        Simulates bandit.
        Args:
            encoded_sent: Encoded sentence
        """
        self.encoded_sent = list(encoded_sent)
        self.encoded_sent_str = ",".join([str(i) for i in encoded_sent])
        self.id = uuid4()


class BanditRewardsLog:
    def __init__(self):
        self.total_actions = 0
        self.total_rewards = 0
        self.all_rewards = []  # not necessary, can be omitted
        self.record = defaultdict(lambda: dict(actions=0, reward=0, reward_squared=0))

    def record_action(self, bandit, reward):
        self.total_actions += 1
        self.total_rewards += reward
        self.all_rewards.append(reward)
        self.record[bandit.id]['actions'] += 1
        self.record[bandit.id]['reward'] += reward
        self.record[bandit.id]['reward_squared'] += reward ** 2

    def __getitem__(self, bandit):
        return self.record[bandit.id]


class Agent(ABC):

    def __init__(self):
        self.rewards_log = BanditRewardsLog()
        self._bandits = None

    @property
    def bandits(self):
        if not self._bandits:
            raise ValueError("No bandit!")
        return self._bandits

    @bandits.setter
    def bandits(self, val):
        self._bandits = val


class BayesianAgent(Agent):
    def __init__(self, reward_distr='bernoulli'):
        if reward_distr not in ('bernoulli'):
            raise ValueError('reward_distr must be "bernoulli".')

        self.reward_distr = reward_distr
        super().__init__()

    def _sample_bandit_mean(self, bandit):
        bandit_record = self.rewards_log[bandit]
        # print(f"bandit_record for {bandit.encoded_sent_str}: {bandit_record}")

        if self.reward_distr == 'bernoulli':
            # + 1 for a Beta(1, 1) prior
            successes = bandit_record['reward'] + 1
            failures = bandit_record['actions'] - bandit_record['reward'] + 1
            return np.random.beta(a=successes, b=failures, size=1)[0]
        else:
            raise NotImplementedError()

    def __repr__(self):
        return 'BayesianAgent(reward_distr="{}")'.format(self.reward_distr)

# Reference: https://towardsdatascience.com/multi-armed-bandits-thompson-sampling-algorithm-fea205cf31df