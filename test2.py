from math import sqrt

message = 'Добро пожаловать в самую лучшую программу для вычисления ' \
          'квадратного корня из заданного числа'
print(message)


def CalculateSquareRoot(Number: float) -> float:
    """Вычисляет квадратный корень."""
    return sqrt(Number)


def calc(your_number: float):
    """Вычисляет из нашей переменной."""
    if your_number <= 0:
        return 0
    else:
        root = CalculateSquareRoot(your_number)
        return print('Мы вычислили квадратный корень из введённого вами числа.'
          'Это будет:', root)


print(message)
calc(25.5)