from dataclasses import dataclass
from typing import Type, List, Dict


@dataclass
class InfoMessage:
    """Informational message about the training"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Training type: {self.training_type}; '
                f'Duration:: {self.duration:.3f} hrs; '
                f'Distance: {self.distance:.3f} km; '
                f'Avgerage speed: {self.speed:.3f} km/h; '
                f'Calories burned: {self.calories:.3f}.')


@dataclass
class Training:
    """The main training class"""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Get the distance in km"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average speed in km/h"""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of burned calories"""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed training."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Training: running."""
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        callories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                     * self.weight / self.M_IN_KM
                     * self.duration * 60)
        return callories


class SportsWalking(Training):
    """Training: sports walking."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        callories = ((self.CALORIES_WEIGHT_MULTIPLIER
                     * self.weight
                     + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                      / (self.height / self.CM_IN_M))
                     * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                     * self.weight)
                     * self.duration * 60)
        return callories


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2
    const = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        callories = ((self.get_mean_speed() + self.const)
                     * self.CALORIES_WEIGHT_MULTIPLIER
                     * self.weight * self.duration)
        return callories


def read_package(workout_type: str, data: List[float]) -> Training:
    """Read the data recieved from the sensors"""
    type_of_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    return type_of_training[workout_type](*data)


def main(training: Training) -> None:
    """The main function."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
