"""Bond pricing and risk analytics."""

from typing import Dict


def price_bond(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> Dict[str, float]:
    """Price vanilla fixed-rate bond using DCF."""
    if face_value <= 0 or years_to_maturity <= 0:
        raise ValueError("Face value and maturity must be positive")
    if coupon_rate < 0 or yield_to_maturity < 0:
        raise ValueError("Rates cannot be negative")
    if coupon_frequency not in [1, 2, 4, 12]:
        raise ValueError("Frequency must be 1, 2, 4, or 12")

    n_periods = int(years_to_maturity * coupon_frequency)
    coupon_payment = (face_value * coupon_rate) / coupon_frequency
    periodic_yield = yield_to_maturity / coupon_frequency

    if coupon_rate == 0:
        price = face_value / ((1 + periodic_yield) ** n_periods)
    elif periodic_yield == 0:
        price = coupon_payment * n_periods + face_value
    else:
        pv_coupons = coupon_payment * (1 - (1 + periodic_yield) ** -n_periods) / periodic_yield
        pv_principal = face_value / ((1 + periodic_yield) ** n_periods)
        price = pv_coupons + pv_principal

    return {
        "price": round(price, 2),
        "dirty_price": round(price, 2),
        "discount_premium": round(price - face_value, 2),
        "par_yield_diff": round((coupon_rate - yield_to_maturity) * 10000, 0),
    }


def calculate_duration(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> Dict[str, float]:
    """Calculate Macaulay and Modified duration."""
    bond_price = price_bond(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )["price"]

    n_periods = int(years_to_maturity * coupon_frequency)
    coupon_payment = (face_value * coupon_rate) / coupon_frequency
    periodic_yield = yield_to_maturity / coupon_frequency

    weighted_cf_time = 0.0
    for period in range(1, n_periods + 1):
        time_years = period / coupon_frequency
        cash_flow = coupon_payment + (face_value if period == n_periods else 0)
        pv_cf = cash_flow / ((1 + periodic_yield) ** period)
        weighted_cf_time += (pv_cf / bond_price) * time_years

    macaulay_duration = weighted_cf_time
    modified_duration = macaulay_duration / (1 + yield_to_maturity / coupon_frequency)
    price_change_1bp = -modified_duration * bond_price * 0.0001

    return {
        "macaulay_duration": round(macaulay_duration, 4),
        "modified_duration": round(modified_duration, 4),
        "approx_price_change_1bp": round(price_change_1bp, 4),
    }


def calculate_convexity(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> Dict[str, float]:
    """Calculate convexity for second-order price sensitivity."""
    bond_price = price_bond(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )["price"]

    n_periods = int(years_to_maturity * coupon_frequency)
    coupon_payment = (face_value * coupon_rate) / coupon_frequency
    periodic_yield = yield_to_maturity / coupon_frequency

    convexity_sum = 0.0
    for period in range(1, n_periods + 1):
        cash_flow = coupon_payment + (face_value if period == n_periods else 0)
        pv_cf = cash_flow / ((1 + periodic_yield) ** period)
        convexity_sum += period * (period + 1) * pv_cf

    convexity = convexity_sum / (bond_price * (1 + periodic_yield) ** 2)
    convexity = convexity / (coupon_frequency**2)
    convexity_adjustment_1bp = 0.5 * convexity * (0.0001**2) * bond_price

    return {
        "convexity": round(convexity, 4),
        "convexity_adjustment_1bp": round(convexity_adjustment_1bp, 6),
    }


def calculate_dv01(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> Dict[str, float]:
    """Calculate DV01 using numerical differentiation."""
    price_base = price_bond(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )["price"]
    price_up = price_bond(
        face_value, coupon_rate, yield_to_maturity + 0.0001, years_to_maturity, coupon_frequency
    )["price"]

    dv01 = abs(price_base - price_up)
    dv01_per_100 = (dv01 / face_value) * 100

    return {"dv01": round(dv01, 4), "dv01_per_100": round(dv01_per_100, 4)}


def bond_analytics(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> Dict[str, float]:
    """Comprehensive bond analytics: price, duration, convexity, DV01."""
    price_metrics = price_bond(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )
    duration_metrics = calculate_duration(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )
    convexity_metrics = calculate_convexity(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )
    dv01_metrics = calculate_dv01(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )

    return {**price_metrics, **duration_metrics, **convexity_metrics, **dv01_metrics}


def price_change_estimate(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    yield_change: float,
    coupon_frequency: int = 2,
    include_convexity: bool = True,
) -> Dict[str, float]:
    """Estimate price change using Taylor approximation: ΔP/P ≈ -D×Δy + 0.5×C×(Δy)²."""
    analytics = bond_analytics(
        face_value, coupon_rate, yield_to_maturity, years_to_maturity, coupon_frequency
    )

    current_price = analytics["price"]
    modified_duration = analytics["modified_duration"]
    convexity = analytics["convexity"]

    duration_effect = -modified_duration * current_price * yield_change
    convexity_effect = (
        0.5 * convexity * current_price * (yield_change**2) if include_convexity else 0.0
    )
    estimated_new_price = current_price + duration_effect + convexity_effect

    actual_new_price = price_bond(
        face_value,
        coupon_rate,
        yield_to_maturity + yield_change,
        years_to_maturity,
        coupon_frequency,
    )["price"]

    return {
        "current_price": round(current_price, 2),
        "estimated_new_price": round(estimated_new_price, 2),
        "actual_new_price": round(actual_new_price, 2),
        "estimation_error": round(estimated_new_price - actual_new_price, 4),
        "duration_effect": round(duration_effect, 2),
        "convexity_effect": round(convexity_effect, 4),
    }
