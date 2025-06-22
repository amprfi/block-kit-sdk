import pytest
from blocks.models import FeeType, RecurringInterval, FeeCurrency

def test_fee_type_enum():
    assert FeeType.FIXED_ONE_TIME == "fixed_one_time"
    assert FeeType.FIXED_RECURRING == "fixed_recurring"

def test_recurring_interval_enum():
    assert RecurringInterval.MONTHLY == "monthly"
    assert RecurringInterval.QUARTERLY == "quarterly"
    assert RecurringInterval.ANNUALLY == "annually"

def test_fee_currency_enum():
    assert FeeCurrency.DAI == "DAI"
    assert FeeCurrency.USDC == "USDC"
    assert FeeCurrency.USDT == "USDT"
    assert FeeCurrency.AMPR == "AMPR"
    assert FeeCurrency.ETH == "ETH"
    assert FeeCurrency.BTC == "BTC"
    assert FeeCurrency.SOL == "SOL"

def test_number_of_accepted_currencies():
    expected_number_of_currencies = 7
    assert len(FeeCurrency) == expected_number_of_currencies