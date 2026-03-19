from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import requests

from .currency_converter import ExchangeRatesError, ExchangeRatesProvider


@dataclass(frozen=True)
class ExchangeRateApiProvider(ExchangeRatesProvider):
    api_url_template: str = "https://api.exchangerate-api.com/v4/latest/{base}"
    timeout_seconds: float = 10.0

    def get_rates(self, base_currency: str) -> Mapping[str, float]:
        base = base_currency.upper()
        url = self.api_url_template.format(base=base)

        try:
            response = requests.get(url, timeout=self.timeout_seconds)
            response.raise_for_status()
            data = response.json()
            rates = data["rates"]
        except (requests.RequestException, ValueError, KeyError) as e:
            raise ExchangeRatesError(f"Failed to fetch exchange rates for {base}") from e

        if not isinstance(rates, dict) or not rates:
            raise ExchangeRatesError(f"Invalid rates payload for {base}")

        return rates

