"""
Binomial Options Pricing Model
Author: Rasheed Cunningham

Supports:
- European Calls & Puts
- American Calls & Puts
- Delta & Gamma (basic)
"""

import math


def binomial_option_price(
    S0,
    K,
    r,
    sigma,
    T,
    N,
    option_type="call",
    american=False
):
    """
    Cox-Ross-Rubinstein binomial model
    """

    dt = T / N

    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u

    p = (math.exp(r * dt) - d) / (u - d)

    discount = math.exp(-r * dt)

    # Terminal prices
    prices = [
        S0 * (u ** j) * (d ** (N - j))
        for j in range(N + 1)
    ]

    # Payoffs
    if option_type == "call":
        values = [max(S - K, 0) for S in prices]
    else:
        values = [max(K - S, 0) for S in prices]

    # Backward induction
    for i in range(N - 1, -1, -1):

        new_values = []

        for j in range(i + 1):

            hold = discount * (
                p * values[j + 1]
                + (1 - p) * values[j]
            )

            if american:

                S = S0 * (u ** j) * (d ** (i - j))

                if option_type == "call":
                    exercise = max(S - K, 0)
                else:
                    exercise = max(K - S, 0)

                new_values.append(max(hold, exercise))

            else:
                new_values.append(hold)

        values = new_values

    return values[0]


def delta_gamma(
    S0, K, r, sigma, T, N, option_type="call"
):
    """
    Approximate Delta & Gamma
    """

    h = 0.01 * S0

    V = binomial_option_price(
        S0, K, r, sigma, T, N, option_type
    )

    V_up = binomial_option_price(
        S0 + h, K, r, sigma, T, N, option_type
    )

    V_down = binomial_option_price(
        S0 - h, K, r, sigma, T, N, option_type
    )

    delta = (V_up - V_down) / (2 * h)

    gamma = (V_up - 2 * V + V_down) / (h ** 2)

    return delta, gamma


if __name__ == "__main__":

    S0 = 100
    K = 100
    r = 0.05
    sigma = 0.2
    T = 1
    N = 100

    euro_call = binomial_option_price(
        S0, K, r, sigma, T, N,
        option_type="call",
        american=False
    )

    amer_put = binomial_option_price(
        S0, K, r, sigma, T, N,
        option_type="put",
        american=True
    )

    delta, gamma = delta_gamma(
        S0, K, r, sigma, T, N
    )

    print("European Call:", round(euro_call, 4))
    print("American Put:", round(amer_put, 4))
    print("Delta:", round(delta, 4))
    print("Gamma:", round(gamma, 4))
