from common.types import DjangoChoices

PRICE_FREE: int = 0
PRICE_INEXPENSIVE: int = 1
PRICE_MODERATE: int = 2
PRICE_EXPENSIVE: int = 3
PRICE_VERY_EXPENSIVE: int = 4
PRICE_LEVEL_CHOICES: DjangoChoices = DjangoChoices([
    (PRICE_FREE, PRICE_FREE),
    (PRICE_INEXPENSIVE, PRICE_INEXPENSIVE),
    (PRICE_MODERATE, PRICE_MODERATE),
    (PRICE_EXPENSIVE, PRICE_EXPENSIVE),
    (PRICE_VERY_EXPENSIVE, PRICE_VERY_EXPENSIVE)
])
