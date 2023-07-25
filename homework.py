from dataclasses import dataclass

message = (
    'Тип тренировки: {0}; '
    'Длительность: {1:.3f} ч.; '
    'Дистанция: {2:.3f} км; '
    'Ср. скорость: {3:.3f} км/ч; '
    'Потрачено ккал: {4:.3f}. '
)


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (message.format(self.training_type,
                               self.duration,
                               self.distance,
                               self.speed,
                               self.calories))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        try:
            pass
        except Exception:
            print('Данную функцию нельзя вызвать.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_SM = 100
    KMH_IN_MS = round(1 / 3.6, 3)
    CALORIES_WEIGHT_MULTIPLIER_ONE = 0.035
    CALORIES_WEIGHT_MULTIPLIER_TWO = 0.029

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return (
            (self.CALORIES_WEIGHT_MULTIPLIER_ONE
             * self.weight + ((self.get_mean_speed() * self.KMH_IN_MS) ** 2
                              / (self.height / self.M_IN_SM))
             * self.CALORIES_WEIGHT_MULTIPLIER_TWO * self.weight)
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT_SWM = 1.1
    CALORIES_WEIGHT_MULTIPLIER_THREE = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self):
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT_SWM)
            * self.CALORIES_WEIGHT_MULTIPLIER_THREE
            * self.weight * self.duration
        )


TRAINING_DICT: dict[str, type] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_class = TRAINING_DICT.get(workout_type)
    if training_class is None:
        raise ValueError("Тип тренировки не определен")
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
     
