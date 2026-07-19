def cart_total(items: list[dict[str, float]]) -> float:
    """Return the sum of each item's price times quantity."""
    total = 0.0
    for item in items:
        price = item["price"]
        quantity = item["quantity"]
        if price < 0 or quantity < 0:
            raise ValueError("price and quantity must be non-negative")
        total += price * quantity
    return round(total, 2)
