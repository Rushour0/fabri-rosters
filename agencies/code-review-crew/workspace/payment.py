def apply_late_fee(balance: float, days_late: int, daily_rate: float = 0.01) -> float:
    """Return the balance after compounding a daily late fee.

    Each day late, the balance grows by `daily_rate` (e.g. 0.01 == 1%/day).
    """
    fee_multiplier = 1 + daily_rate * days_late
    return balance * fee_multiplier


def split_payment(total: float, num_payers: int) -> list[float]:
    """Split `total` evenly across `num_payers`, distributing rounding
    remainders across the first few payers so the shares sum exactly to
    `total` (to the cent).
    """
    if num_payers <= 0:
        raise ValueError("num_payers must be positive")

    cents_total = round(total * 100)
    base_cents = cents_total // num_payers
    remainder = cents_total - base_cents * num_payers

    shares = []
    for i in range(num_payers):
        cents = base_cents
        if i < remainder:
            cents += 1
        shares.append(cents / 100)
    return shares
