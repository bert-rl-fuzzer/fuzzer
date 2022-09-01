import numpy as np


class PiEstimator:
    def __init__(self):
        self.total_samples = 0
        self.total_in_circle = 0
        self.x_centre = 0.5
        self.y_centre = 0.5
        self.radius = 0.5
        self.box_area = 1

    def reset(self):
        self.total_samples = 0
        self.total_in_circle = 0

    def is_point_in_circle(self, x, y):
        return (x - self.x_centre) ** 2 + (y - self.y_centre) ** 2 < self.radius ** 2

    def current_pi_estimate(self):
        """
        Since (Circle Area) = pi * R^2 that means pi = (Circle Area) / R ** 2
        :return: pi estimate
        """
        circle_area_estimate = (self.total_in_circle / self.total_samples) * self.box_area
        return circle_area_estimate / self.radius ** 2

    def sample_point(self):
        x, y = np.random.uniform(0, 1, 2)
        self.total_samples += 1

        if self.is_point_in_circle(x, y):
            self.total_in_circle += 1

        return x, y

    def sample_points(self, n=100):
        """Faster than just sampling one point at a time."""
        points = np.random.uniform(0, 1, (n, 2))
        points_classifications = np.apply_along_axis(
            lambda xy: self.is_point_in_circle(xy[0], xy[1]),
            axis=1,
            arr=points,
        )

        self.total_samples += n
        self.total_in_circle += np.sum(points_classifications)
