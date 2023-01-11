from dataclasses import dataclass
from typing import Dict, Type, ClassVar


@dataclass
class InfoMessage:
    """
    Информационное сообщение о тренировке.
    """
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        info_message = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return info_message


@dataclass
class Training:
    # Каждый класс, описывающий определённый вид тренировки, будет
    # дополнять и расширять этот базовый класс.
    """
    Базовый класс тренировки.
    Содержит все основные свойства и методы для тренировок.
    Входные переменные:
    - action - количество совершённых действий
    - duration - длительность тренировки
    - weight - вес спортсмена
    """

    # расстояние, которое спортсмен преодолевает
    LEN_STEP: ClassVar[float] = 0.65
    # константа для перевода значений из метров в километры.
    M_IN_KM: ClassVar[float] = 1000
    # константа для перевода времени.
    TIME_CONST: ClassVar[float] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """
        Возвращает дистанцию (в километрах), которую преодолел спортсмен
        за время тренировки.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    # возвращает значение средней скорости движения во время тренировки в км/ч
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # формула из задания
        # преодоленная_дистанция_за_тренировку / время_тренировки
        return self.get_distance() / self.duration

    # метод определяется в дочерних классах, расчет калорий отличается
    # в зависимости от тренировки
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Требуется определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """
        Возвращает объект класса - информационное сообщение
        о выполненной тренировке.
        """
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:

        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.TIME_CONST)


@dataclass
class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    Дополнительный параметр height — рост спортсмена
    """

    calorie_1: ClassVar[float] = 0.035
    calorie_2: ClassVar[float] = 0.029
    calorie_3: ClassVar[float] = 2

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.calorie_1
                * self.weight
                + (self.get_mean_speed() ** self.calorie_3
                    // self.height)
                * self.calorie_2 * self.weight)
                * self.TIME_CONST * self.duration)


@dataclass
class Swimming(Training):
    """
    Тренировка: плавание.
    Дополнительные входные переменные:
    - length_pool — длина бассейна в метрах;
    - count_pool — сколько раз пользователь переплыл бассейн.
    Переопределённые переменные:
    - LEN_STEP - теперь один гребок
    Переопределёны методы:
    - get_spent_calories() - расчета калорий
    - get_mean_speed() - рассчитывает среднюю скорость
    """

    # расстояние, которое спортсмен преодолевает за гребок 1.38 метра
    LEN_STEP: ClassVar[float] = 1.38
    calorie_1: ClassVar[float] = 1.1
    calorie_2: ClassVar[float] = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.calorie_1)
                * self.calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """
    Заранее подготовленные тестовые данные.
    """
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in workout:
        raise ValueError(f"Такой тренировки - {workout_type}, не найдено")
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
