from __future__ import annotations

from converters import CurrencyConverter, ExchangeRateApiProvider, ExchangeRatesError


def _read_amount_usd() -> float:
    raw = input("Введите значение в USD:\n").strip().replace(",", ".")
    try:
        amount = float(raw)
    except ValueError as e:
        raise ValueError("Некорректное число") from e
    if amount < 0:
        raise ValueError("Сумма должна быть неотрицательной")
    return amount


def main() -> None:
    amount = _read_amount_usd()

    converter = CurrencyConverter(provider=ExchangeRateApiProvider(), base_currency="USD")
    targets = ["RUB", "EUR", "GBP", "CNY"]

    for target in targets:
        try:
            converted = converter.convert(amount, target)
        except ExchangeRatesError as e:
            print(f"Ошибка получения курса для {target}: {e}")
            continue
        print(f"{amount:g} USD to {target}: {converted:g}")

if __name__ == "__main__":
    main()