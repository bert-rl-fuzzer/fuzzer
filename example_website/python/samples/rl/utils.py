import logging
from typing import List

import numpy as np
import matplotlib.pyplot as plt

from samples.rl.bandit import Agent, Bandit
from samples.rl import ucb


logger = logging.getLogger(__name__)


def compare_agents(
    agents: List[Agent],
    bandits: List[Bandit],
    iterations: int,
    show_plot=True,
):
    for agent in agents:
        logger.info("Running for agent = %s", agent)
        agent.bandits = bandits
        if isinstance(agent, ucb.UCBAgent):
            agent.initialise()

        N = iterations - agent.rewards_log.total_actions
        agent.take_actions(N)
        if show_plot:
            cumulative_rewards = np.cumsum(
                agent.rewards_log.all_rewards,
            )
            plt.plot(cumulative_rewards, label=str(agent))

    if show_plot:
        plt.xlabel("iteration")
        plt.ylabel("total rewards")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
