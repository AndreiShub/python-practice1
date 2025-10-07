from dataclasses import dataclass, field
from .exceptions import NegativeValueException, NotComparisonException


from dataclasses import dataclass, field

@dataclass(frozen=True)
class Money:
    value: float
    currency: str

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Сумма не может быть отрицательной")

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise ValueError("Можно складывать только объекты Money")
        if self.currency != other.currency:
            raise NotComparisonException("Нельзя складывать разные валюты")
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise ValueError("Можно вычитать только объекты Money")
        if self.currency != other.currency:
            raise NotComparisonException("Нельзя вычитать разные валюты")
        result = self.value - other.value
        if result < 0:
            raise NegativeValueException("Результат не может быть отрицательным")
        return Money(result, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and self.value == other.value

    def __repr__(self):
        return f"{self.value:.2f} {self.currency.upper()}"


@dataclass
class Wallet:
    initial_money: Money
    _balances: dict[str, Money] = field(init=False, default_factory=dict)

    def __post_init__(self):
        # При инициализации создаём баланс с одной валютой
        self._balances[self.initial_money.currency] = self.initial_money

    @property
    def currencies(self):
        return set(self._balances.keys())

    def __getitem__(self, currency: str) -> Money:
        # Возвращаем Money даже если валюты нет (значение 0)
        return self._balances.get(currency, Money(0, currency))

    def __delitem__(self, currency: str):
        # Если валюты нет — ничего не делаем
        self._balances.pop(currency, None)

    def __contains__(self, currency: str) -> bool:
        return currency in self._balances

    def __len__(self) -> int:
        return len(self._balances)

    def add(self, money: Money) -> "Wallet":
        current = self._balances.get(money.currency, Money(0, money.currency))
        self._balances[money.currency] = current + money
        return self  # чтобы можно было чейнить

    def sub(self, money: Money) -> "Wallet":
        current = self._balances.get(money.currency, Money(0, money.currency))
        self._balances[money.currency] = current - money  # может бросить NegativeValueException
        # Если баланс стал 0, можно удалить валюту
        if self._balances[money.currency].value == 0:
            del self._balances[money.currency]
        return self

    def __repr__(self):
        items = ", ".join(f"{cur}: {money}" for cur, money in self._balances.items())
        return f"Wallet({items})"