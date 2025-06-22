import pytest
from blocks.base import AnalystBlock
from blocks.models import Manifest

def test_analyst_block_initialization():
    manifest = Manifest(
        name="Test Analyst Block",
        version="1.0.0",
        block_type="analyst",
        publisher=("Test Publisher", "ID string"),
        description="Test description",
    )
    block = AnalystBlock(manifest)
    assert block.manifest == manifest

def test_analyst_block_initialization_invalid():
    manifest = Manifest(
        name="Test Block",
        version="1.0.0",
        block_type="action",
        publisher=("Test Publisher", "ID string"),
        description="Test description"
    )
    with pytest.raises(ValueError):
        AnalystBlock(manifest)