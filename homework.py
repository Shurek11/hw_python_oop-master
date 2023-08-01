from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    message = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.'
               )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.message.format(**asdict(self))

    def __str__(self) -> str:
        return self.get_message()


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(type(self.__name__, self.duration,
                                 self.get_distance(), self.get_mean_speed(),
                                 self.get_spent_calories())))


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


MIN_IN_HOUR = 60
SEC_IN_MIN = 60
M_IN_KM = 1000


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int

    CALORIES_WEIGHT_MULTIPLIER_ONE: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_TWO: float = 0.029
    KM_IN_M: float = 0.270
    CEN_IN_M: float = 100

    def get_spent_calories(self):
        return (
            (self.CALORIES_WEIGHT_MULTIPLIER_ONE
             * self.weight + ((self.get_mean_speed() * self.KM_IN_M) ** 2
                              / (self.height / self.CEN_IN_M))
             * self.CALORIES_WEIGHT_MULTIPLIER_TWO * self.weight)
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: int

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT_SWIMMING: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER_SWIMMING: int = 2

    def get_mean_speed(self):
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self):
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT_SWIMMING)
            * self.CALORIES_WEIGHT_MULTIPLIER_SWIMMING
            * self.weight * self.duration
        )


workout_dict = {'RUN': Running,
                'WLK': SportsWalking,
                'SWM': Swimming}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_class = workout_dict.get(workout_type)
    if training_class is None:
        raise ValueError("Тип тренировки не определен")
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
