import pytest
from blocks.models import BaseFee, FeeType, RecurringInterval, FeeCurrency, OneTimeFixedFee, RecurringFixedFee, Manifest
from pydantic import ValidationError, HttpUrl

def test_base_fee_model():
    fee = BaseFee(fee_currency=FeeCurrency.DAI, description="Test fee")
    assert fee.fee_currency == FeeCurrency.DAI
    assert fee.description == "Test fee"

def test_one_time_fixed_fee_model():
    fee = OneTimeFixedFee(fee_type=FeeType.FIXED_ONE_TIME, amount=100.0, fee_currency=FeeCurrency.USDC)
    assert fee.fee_type == FeeType.FIXED_ONE_TIME
    assert fee.amount == 100.0
    assert fee.fee_currency == FeeCurrency.USDC

def test_recurring_fixed_fee_model():
    fee = RecurringFixedFee(fee_type=FeeType.FIXED_RECURRING, amount=50.0, fee_currency=FeeCurrency.ETH, interval=RecurringInterval.MONTHLY)
    assert fee.fee_type == FeeType.FIXED_RECURRING
    assert fee.amount == 50.0
    assert fee.fee_currency == FeeCurrency.ETH
    assert fee.interval == RecurringInterval.MONTHLY

def test_manifest_model():
    manifest = Manifest(
        name="Test Block",
        version="1.0.0",
        block_type="analyst",
        publisher=("Test Publisher", "ID string"),
        description="A test block",
    )
    assert manifest.name == "Test Block"
    assert manifest.version == "1.0.0"
    assert manifest.block_type == "analyst"
    assert manifest.publisher == ("Test Publisher", "ID string")
    assert manifest.description == "A test block"

def test_manifest_model_with_fee():
    fee = OneTimeFixedFee(fee_type=FeeType.FIXED_ONE_TIME, amount=0.0010, fee_currency=FeeCurrency.BTC)
    manifest = Manifest(
        name="Test Block",
        version="0.2.0",
        block_type="action",
        publisher=("Test Publisher", "ID string"),
        description="A test block",
        fee=fee
    )
    assert manifest.name == "Test Block"
    assert manifest.version == "0.2.0"
    assert manifest.block_type == "action"
    assert manifest.publisher == ("Test Publisher", "ID string")
    assert manifest.description == "A test block"
    assert manifest.fee == fee

def test_manifest_model_with_license():
    manifest = Manifest(
        name="Test Block",
        version="0.2.0",
        block_type="action",
        publisher=("Test Publisher", "ID string"),
        description="A test block",
        license=("MIT", "https://opensource.org/licenses/MIT")
    )
    assert manifest.name == "Test Block"
    assert manifest.version == "0.2.0"
    assert manifest.block_type == "action"
    assert manifest.publisher == ("Test Publisher", "ID string")
    assert manifest.description == "A test block"
    assert manifest.license == ("MIT", HttpUrl("https://opensource.org/licenses/MIT"))


def test_manifest_model_with_multiple_fees_invalid():
    fee1 = OneTimeFixedFee(fee_type=FeeType.FIXED_ONE_TIME, amount=10.0, fee_currency=FeeCurrency.USDC)
    fee2 = RecurringFixedFee(fee_type=FeeType.FIXED_RECURRING, amount=5.0, interval=RecurringInterval.MONTHLY, fee_currency=FeeCurrency.ETH)
    with pytest.raises(ValidationError):
        Manifest(
            name="Test Block",
            version="1.0.0",
            block_type="analyst",
            publisher=("Test Publisher", "ID string"),
            description="Test description",
            fee=[fee1, fee2]
        )

def test_manifest_model_with_agent_block_type_invalid():
    with pytest.raises(ValidationError):
        Manifest(
            name="Test Block",
            version="1.0.0",
            block_type="agent",
            publisher=("Test Publisher", "ID string"),
            description="Test description",
        )
def test_manifest_model_with_XRP_fee_currency_invalid():
    with pytest.raises(ValidationError):
        BaseFee(fee_currency="XRP")

def test_one_time_fixed_fee_negative_invalid():
    with pytest.raises(ValidationError):
        OneTimeFixedFee(fee_type=FeeType.FIXED_ONE_TIME, amount=-10.0, fee_currency=FeeCurrency.ETH)

def test_recurring_fixed_fee_daily_interval_invalid():
    with pytest.raises(ValidationError):
        RecurringFixedFee(fee_type=FeeType.FIXED_RECURRING, amount=5.0, interval="daily", fee_currency=FeeCurrency.ETH)