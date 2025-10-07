class NotComparisonException(Exception):
    """Выбрасывается при попытке операций с разными валютами."""


class NegativeValueException(Exception):
    """Выбрасывается при попытке получить отрицательное значение."""