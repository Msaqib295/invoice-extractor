def check_totals(inv, tolerance=1.0):
    if inv.subtotal is None or inv.total is None:
        return {"status": "cannot_check",
                "message": "Subtotal or total not found, so the numbers could not be checked."}
    expected = inv.subtotal - (inv.discount or 0) + (inv.tax or 0) + (inv.delivery or 0)
    diff = round(inv.total - expected, 2)
    if abs(diff) <= tolerance:
        return {"status": "ok", "expected": expected, "difference": diff,
                "message": "Numbers add up."}
    return {"status": "mismatch", "expected": expected, "difference": diff,
            "message": f"The numbers do not add up (expected {expected:,.0f}, "
                       f"invoice total {inv.total:,.0f}). Please check."}