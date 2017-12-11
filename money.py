from decimal import Decimal
from typing import Union

from decorators import validate_other_is_money, validate_same_currencies
from exceptions import MalformattedCurrencyCodeError
from messages import NON_STRING_CURRENCY_MESSAGE, MALFORMATTED_CURRENCY_CODE_MESSAGE

PRECISION = '.0001'
ConvToDecimal = Union[Decimal, int, float, str]


class Money:

    def __init__(
            self,
            amount: ConvToDecimal,
            currency: str
    ) -> None:
        self._amount: Decimal = self._to_decimal(amount)
        self._currency_code: str = self._valudate_currency(currency)

    # public properties
    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency_code

    # to Decimal conversion
    def _to_decimal(self, amount: ConvToDecimal) -> Decimal:
        return self._quantize(Decimal(amount))

    def _quantize(self, amount: Decimal) -> Decimal:
        return amount.quantize(Decimal(PRECISION))

    # currency code validation
    def _valudate_currency(self, currency_code):
        if not isinstance(currency_code, str):
            raise TypeError(NON_STRING_CURRENCY_MESSAGE(
                type(currency_code).__name__))

        is_code_malformed = (
            not currency_code.isalpha()
            or not currency_code.isupper()
            or len(currency_code) != 3
        )
        if is_code_malformed:
            raise MalformattedCurrencyCodeError(
                MALFORMATTED_CURRENCY_CODE_MESSAGE(code=currency_code))

        return currency_code

    # string representation
    def __repr__(self):
        return f"Money(amount='{self._amount}', currency='{self._currency_code}')"

    def __str__(self):
        return f'{self._amount} {self._currency_code}'

    # operators
    def __bool__(self) -> bool:
        return bool(self._amount)

    def __pos__(self) -> 'Money':
        return self

    def __neg__(self) -> 'Money':
        return Money(-self._amount, self._currency_code)

    @validate_other_is_money('add')
    @validate_same_currencies('add')
    def __add__(self, other: 'Money') -> 'Money':
        return Money(self._amount + other._amount, self._currency_code)

    @validate_other_is_money('subtract')
    @validate_same_currencies('subtract')
    def __sub__(self, other: 'Money') -> 'Money':
        return self + (-other)

    @validate_other_is_money('compare')
    @validate_same_currencies('compare')
    def __eq__(self, other: 'Money') -> bool:
        return self._amount == other._amount

    @validate_other_is_money('compare')
    @validate_same_currencies('compare')
    def __ne__(self, other: 'Money') -> bool:
        return self._amount != other._amount

    @validate_other_is_money('compare')
    @validate_same_currencies('compare')
    def __lt__(self, other: 'Money') -> bool:
        return self._amount < other._amount

    @validate_other_is_money('compare')
    @validate_same_currencies('compare')
    def __le__(self, other: 'Money') -> bool:
        return self._amount <= other._amount

    @validate_other_is_money('compare')
    @validate_same_currencies('compare')
    def __gt__(self, other: 'Money') -> bool:
        return self._amount > other._amount

    @validate_other_is_money('compare')
    @validate_same_currencies('compare')
    def __ge__(self, other: 'Money') -> bool:
        return self._amount >= other._amount
