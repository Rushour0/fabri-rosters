from store import cart_total


def test_cart_total_keeps_ninety_percent_after_ten_percent_discount() -> None:
    assert cart_total(100, 10) == 90
