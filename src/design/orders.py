from dataclasses import dataclass, field
from typing import List, Protocol


class Discount(Protocol):
    def apply(self, order: "Order") -> float:
        """Возвращает сумму скидки, которую нужно вычесть из заказа"""
        ...


@dataclass
class FixedDiscount:
    amount: float

    def apply(self, order: "Order") -> float:
        return min(self.amount, order.total)


@dataclass
class PercentageDiscount:
    percent: float

    def apply(self, order: "Order") -> float:
        return order.total * (self.percent / 100)


@dataclass
class LoyaltyDiscount:
    loyalty_level: int

    def apply(self, order: "Order") -> float:
        if self.loyalty_level >= 3:
            return order.total * 0.05
        return 0.0


@dataclass
class Order:
    total: float
    customer_name: str
    loyalty_level: int = 1
    discounts: List[Discount] = field(default_factory=list)

    def add_discount(self, discount: Discount):
        self.discounts.append(discount)

    def apply_discounts(self) -> float:
        total_discount = sum(d.apply(self) for d in self.discounts)
        return max(self.total - total_discount, 0)

    def __str__(self):
        final_price = self.apply_discounts()
        return f"Order({self.customer_name}): total={self.total}, final={final_price}"


class DiscountSelector:
    """Определяет, какие скидки применимы к заказу."""

    @staticmethod
    def get_discounts_for_order(order: Order) -> List[Discount]:
        discounts: List[Discount] = []

        # если заказ большой — процентная скидка
        if order.total > 1000:
            discounts.append(PercentageDiscount(10))

        # если клиент постоянный — скидка за лояльность
        if order.loyalty_level >= 3:
            discounts.append(LoyaltyDiscount(order.loyalty_level))

        # всем новым клиентам — фиксированная скидка на первый заказ
        if order.loyalty_level == 1:
            discounts.append(FixedDiscount(50))

        return discounts
