"""
Forwards and Futures Pricing & Hedging Module
Author: Rasheed Cunningham

Implements:
- Cost-of-carry forward pricing
- Forward valuation
- Minimum variance hedge ratio
- Hedge P&L simulator
"""

import math


def forward_price(spot, rate, dividend_yield, time):
    """
    Compute forward price using cost-of-carry model.

    F = S * exp((r - q) * T)
    """
    return spot * math.exp((rate - dividend_yield) * time)


def forward_value(spot_t, delivery_price, rate, dividend_yield, t, T):
    """
    Mark-to-market value of a forward contract at time t.
    """
    tau = T - t
    return (
        spot_t * math.exp(-dividend_yield * tau)
        - delivery_price * math.exp(-rate * tau)
    )


def hedge_ratio(correlation, sigma_spot, sigma_futures):
    """
    Minimum variance hedge ratio.
    """
    return correlation * (sigma_spot / sigma_futures)


def hedge_pnl(
    spot_start,
    spot_end,
    fut_start,
    fut_end,
    units,
    hedge_ratio,
):
    """
    Compute hedged P&L using futures.
    """

    unhedged = units * (spot_end - spot_start)

    contracts = hedge_ratio * units

    futures_pnl = -contracts * (fut_end - fut_start)

    total = unhedged + futures_pnl

    return unhedged, futures_pnl, total


if __name__ == "__main__":

    # Example Parameters
    S0 = 100
    r = 0.05
    q = 0.02
    T = 0.5

    # Forward Price
    F0 = forward_price(S0, r, q, T)
    print("Forward Price:", round(F0, 2))

    # Forward Value After 3 Months
    St = 104
    t = 0.25

    value = forward_value(St, F0, r, q, t, T)
    print("Forward Value:", round(value, 2))

    # Hedge Ratio
    rho = 0.9
    sigma_S = 0.2
    sigma_F = 0.18

    h = hedge_ratio(rho, sigma_S, sigma_F)
    print("Optimal Hedge Ratio:", round(h, 3))

    # Hedge PnL
    pnl = hedge_pnl(
        100,
        105,
        F0,
        F0 + 4,
        1000,
        h,
    )

    print("Unhedged PnL:", round(pnl[0], 2))
    print("Futures PnL:", round(pnl[1], 2))
    print("Total PnL:", round(pnl[2], 2))

