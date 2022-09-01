import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class BetaBinomialTest:
    def __init__(self, group_a_name, group_b_name, a_prior=1, b_prior=1):
        self.a_prior = a_prior
        self.b_prior = b_prior

        self.group_data = {
            group_a_name: {'successes': 0, 'trials': 0, 'sample_ratio': 0},
            group_b_name: {'successes': 0, 'trials': 0, 'sample_ratio': 0},
        }

    def update_group_data(self, group_name, successes, trials):
        self.group_data[group_name]['successes'] = successes
        self.group_data[group_name]['failures'] = trials - successes
        self.group_data[group_name]['trials'] = trials
        self.group_data[group_name]['sample_ratio'] = successes / trials

    def compare(self, group_a_name, group_b_name, n=10000, margin=0, show_plot=True):
        samples_a = np.random.beta(
            a=self.a_prior + self.group_data[group_a_name]['successes'],
            b=self.b_prior + self.group_data[group_a_name]['failures'],
            size=n,
        )
        samples_b = np.random.beta(
            a=self.a_prior + self.group_data[group_b_name]['successes'],
            b=self.b_prior + self.group_data[group_b_name]['failures'],
            size=n,
        )

        differences = samples_a - samples_b
        prob_a_better_than_b = np.mean(differences > margin)

        if show_plot:
            fig, ax = plt.subplots(1, 2)
            sns.histplot(differences, ax=ax[0], stat='probability')
            ax[0].title.set_text(
                'P({}-{}>{})={:.3f}'.format(group_a_name, group_b_name, margin, prob_a_better_than_b),
            )
            ax[0].axvline(x=margin, ymin=0, ymax=1, color='k')

            sns.histplot(
                samples_a,
                ax=ax[1],
                label='{} (sample ratio={:.2f})'.format(group_a_name, self.group_data[group_a_name]['sample_ratio']),
                color='b',
                stat='probability',
            )
            sns.histplot(
                samples_b,
                ax=ax[1],
                label='{} (sample ratio={:.2f})'.format(group_b_name, self.group_data[group_b_name]['sample_ratio']),
                color='r',
                stat='probability'
            )
            ax[1].axvline(x=self.group_data[group_a_name]['sample_ratio'], ymin=0, ymax=1, color='k')
            ax[1].axvline(x=self.group_data[group_b_name]['sample_ratio'], ymin=0, ymax=1, color='k')
            ax[1].title.set_text('Posterior Histograms')
            ax[1].legend(bbox_to_anchor=(1.1, 1.05))
            plt.show()

        return prob_a_better_than_b, differences
