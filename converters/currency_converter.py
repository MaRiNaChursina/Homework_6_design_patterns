from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class ExchangeRatesError(RuntimeError):
    pass

class ExchangeRatesProvider:
    def get_rates(self, base_currency: str) -> Mapping[str, float]:
        raise NotImplementedError


@dataclass(frozen=True)
class CurrencyConverter:
    provider: ExchangeRatesProvider
    base_currency: str = "USD"

    def convert(self, amount: float, target_currency: str) -> float:
        if amount < 0:
            raise ValueError("amount must be non-negative")

        base = self.base_currency.upper()
        target = target_currency.upper()

        if base == target:
            return float(amount)

        rates = self.provider.get_rates(base)
        try:
            rate = float(rates[target])
        except KeyError as e:
            raise ExchangeRatesError(f"Rate not found for {base}->{target}") from e

        return float(amount) * rate