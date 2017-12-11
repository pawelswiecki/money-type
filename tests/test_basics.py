from decimal import Decimal

import pytest

from exceptions import MalformattedCurrencyCodeError
from money import Money


@pytest.mark.parametrize('amount, currency, expected_amount', [
    (Decimal('11.0001'), 'XYZ', Decimal('11.0001')),
    (10, 'EUR', Decimal('10.0000')),
    (35.1, 'USD', Decimal('35.1000')),
    ('99.1234', 'XYZ', Decimal('99.1234')),
])
def test_money_properties(amount, currency, expected_amount):
    money = Money(amount, currency)
    assert money.amount == expected_amount
    assert money.currency == currency


@pytest.mark.parametrize('amount, expected_amount', [
    ('1', Decimal('1.0000')),
    ('1.11111', Decimal('1.1111')),
    ('1.55555', Decimal('1.5556')),
    ('1.99999', Decimal('2.0000')),
])
def test_money_amount_round(amount, expected_amount):
    money = Money(amount, 'GBP')
    assert money.amount == expected_amount


@pytest.mark.parametrize('amount, currency, expected', [
    ('100.1', 'EUR', "Money(amount='100.1000', currency='EUR')"),
    ('99.1234', 'ABC', "Money(amount='99.1234', currency='ABC')"),
])
def test_money_repr(amount, currency, expected):
    assert repr(Money(amount, currency)) == expected


@pytest.mark.parametrize('amount, currency, expected', [
    ('100.1', 'EUR', '100.1000 EUR'),
    ('99.1234', 'ABC', '99.1234 ABC'),
])
def test_money_str(amount, currency, expected):
    assert str(Money(amount, currency)) == expected


@pytest.mark.parametrize('non_string_object', [
    10, 10.0, Decimal('10'), [10], {}, object(), None, False,
])
def test_currency_code_validation_should_raise_error_on_non_string(non_string_object):  # noqa: E501
    with pytest.raises(TypeError):
        Money(amount=1, currency=non_string_object)


@pytest.mark.parametrize('bad_code', [
    '', '   ', '1', '123', 'qwerty', 'usd', 'USD2',
    'Bob', 'PLn', 'USDUSD', 'CH ', 'USD ', 'EU2',
])
def test_currency_code_validation_should_raise_error_on_malformatted_code(bad_code):  # noqa: E501
    with pytest.raises(MalformattedCurrencyCodeError):
        Money(amount=1, currency=bad_code)
