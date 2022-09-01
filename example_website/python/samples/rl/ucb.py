import logging
from abc import abstractmethod
from typing import Optional

import numpy as np

from samples.rl.bandit import (
    Agent,
    Bandit,
)


logger = logging.getLogger(__name__)


class UCBAgent(Agent):
    def __init__(self):
        super().__init__()
        self.initialised = False

    @abstractmethod
    def initialise(self):
        ...

    @abstractmethod
    def calculate_bandit_index(self, bandit):
        ...

    def _get_current_best_bandit(self) -> Bandit:
        estimates = [self.calculate_bandit_index(bandit) for bandit in self.bandits]
        return self.bandits[np.argmax(estimates)]

    def take_action(self):
        if not self.initialised:
            raise Exception('Initialisation step needs to be executed first.')

        current_bandit = self._get_current_best_bandit()
        reward = current_bandit.pull()
        self.rewards_log.record_action(current_bandit, reward)
        return reward


class UCB1Agent(UCBAgent):
    def initialise(self):
        if self.initialised:
            logger.info('Initialisation step has been executed before.')
            return

        for bandit in self.bandits:
            reward = bandit.pull()
            self.rewards_log.record_action(bandit, reward)
        self.initialised = True

    def calculate_bandit_index(self, bandit):
        '''
        Sample Mean + √(2logN / n)
        '''
        bandit_record = self.rewards_log[bandit]
        sample_mean = bandit_record['reward'] / bandit_record['actions']
        c = np.sqrt(2 * np.log(self.rewards_log.total_actions) / bandit_record['actions'])
        return sample_mean + c

    def __repr__(self):
        return 'UCB1()'


class UCB1TunedAgent(UCBAgent):
    def initialise(self):
        if self.initialised:
            logger.info('Initialisation step has been executed before.')
            return

        for bandit in self.bandits:
            reward = bandit.pull()
            self.rewards_log.record_action(bandit, reward)
        self.initialised = True

    def calculate_bandit_index(self, bandit):
        '''
        C = √( (logN / n) x min(1/4, V(n)) )
        where V(n) is an upper confidence bound on the variance of the bandit, i.e.
        V(n) = Σ(x_i² / n) - (Σ (x_i / n))² + √(2log(N) / n)
        '''
        bandit_record = self.rewards_log[bandit]
        n = bandit_record['actions']
        sample_mean = bandit_record['reward'] / n

        variance_bound = bandit_record['reward_squared'] / n - sample_mean ** 2
        variance_bound += np.sqrt(2 * np.log(self.rewards_log.total_actions) / n)

        c = np.sqrt(np.min([variance_bound, 1 / 4]) * np.log(self.rewards_log.total_actions) / n)
        return sample_mean + c

    def __repr__(self):
        return 'UCB1Tuned()'


class UCB1NormalAgent(UCBAgent):
    def initialise(self):
        if self.initialised:
            logger.info('Initialisation step has been executed before.')
            return

        for bandit in self.bandits:
            for _ in range(2):
                reward = bandit.pull()
                self.rewards_log.record_action(bandit, reward)

        self.initialised = True

    def calculate_bandit_index(self, bandit):
        '''
        Calculates the upper confidence index Sample Mean + C where C = √( 16 SV(n) log(N - 1) / n ) and the sample
        variance is
            SV(n) = ( Σ x_i² - n (Σ x_i / n)² ) / (n - 1)
        '''
        bandit_record = self.rewards_log[bandit]
        n = bandit_record['actions']

        sample_mean = bandit_record['reward'] / n
        sample_variance = (bandit_record['reward_squared'] - n * sample_mean ** 2) / (n - 1)
        c = np.sqrt(16 * sample_variance * np.log(self.rewards_log.total_actions - 1) / n)

        return sample_mean + c

    def _get_bandit_with_insufficient_data(self) -> Optional[Bandit]:
        res = []
        for bandit in self.bandits:
            bandit_record = self.rewards_log[bandit]
            if bandit_record['actions'] < np.max([3, np.ceil(8 * np.log(self.rewards_log.total_actions))]):
                res.append(bandit)

        if res:
            return np.random.choice(res)
        return None

    def _get_current_best_bandit(self) -> Bandit:
        estimates = [self.calculate_bandit_index(bandit) for bandit in self.bandits]
        return self.bandits[np.argmax(estimates)]

    def take_action(self):
        if not self.initialised:
            raise Exception('Initialisation step needs to be executed first.')

        current_bandit = self._get_bandit_with_insufficient_data()
        if not current_bandit:
            current_bandit = self._get_current_best_bandit()
        reward = current_bandit.pull()
        self.rewards_log.record_action(current_bandit, reward)
        return reward

    def __repr__(self):
        return 'UCB1Normal()'
