"""Ecommerce modeling with pydantic example."""

from datetime import date

from pydantic import BaseModel, Field, confloat


class Product(BaseModel):
    """Product in ecommerce chart."""

    name: str
    category: str
    shipping_weight: confloat(gt=0)
    unit_price: confloat(gt=0)
    tax_percent: confloat(ge=0, le=1)


class Order(BaseModel):
    """Order in ecommerce website."""

    status: str
    creation_date: date = date.today()
    products: list[Product] = Field(default_factory=list)

    def add_item(self, product: Product) -> None:
        """Insert one product into order."""
        self.products.append(product)

    def calculate_sub_total(self) -> float:
        """Total order price without taxes."""
        subtotal = sum((p.unit_price for p in self.products))
        return round(subtotal, 2)

    def calculate_tax(self) -> float:
        """Total paid in taxes."""
        taxes = sum((p.unit_price * p.tax_percent for p in self.products))
        return round(taxes, 2)

    def calculate_total(self) -> float:
        """Total order price considering taxes."""
        total = self.calculate_sub_total() + self.calculate_tax()
        return round(total, 2)

    @property
    def total_weight(self) -> float:
        """Total weight of order."""
        return sum((p.shipping_weight for p in self.products))


def main() -> None:
    banana = Product(
        name="banana",
        category="fruit",
        shipping_weight=0.5,
        unit_price=2.15,
        tax_percent=0.07,
    )

    mango = Product(
        name="mango",
        category="fruit",
        shipping_weight=2,
        unit_price=3.19,
        tax_percent=0.11,
    )

    expensive_mango = Product(
        name="Mango",
        category="Fruit",
        shipping_weight=4.0,
        unit_price=8.0,
        tax_percent=0.20,
    )

    order = Order(creation_date=date.today(), status="openned")

    order.add_item(banana)
    order.add_item(mango)
    order.add_item(expensive_mango)

    print(f"Comparison bewteen mango and expensive mango: {mango == expensive_mango}")

    print(f"Total order price: U$ {order.calculate_total()}")
    print(f"Subtotal order price: U$ {order.calculate_sub_total()}")
    print(f"Value paid in taxes: U$ {order.calculate_tax()}")
    print(f"Total weight order: {order.total_weight}")


if __name__ == "__main__":
    main()
