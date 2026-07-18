def cart_total(subtotal: float, discount_percent: float = 0) -> float:
    """Return the cart total after a percentage discount."""
    return subtotal * (1 - discount_percent)
