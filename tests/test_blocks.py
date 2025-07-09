import pytest
from blocks.base import AnalystBlock
from blocks.models import Manifest

class ConcreteAnalystBlock(AnalystBlock):
    async def initialize(self):
        pass

    async def analyze(self, request: dict) -> str:
        return "Analysis result"

def test_analyst_block_initialization():
    manifest = Manifest(
        name="Test Analyst Block",
        version="1.0.0",
        block_type="analyst",
        publisher=("Test Publisher", "ID string"),
        description="Test description",
    )
    block = ConcreteAnalystBlock(manifest)
    assert block.manifest.name == "Test Analyst Block"

def test_analyst_block_initialization_invalid():
    manifest = Manifest(
        name="Test Block",
        version="1.0.0",
        block_type="action",
        publisher=("Test Publisher", "ID string"),
        description="Test description"
    )
    with pytest.raises(ValueError):
        ConcreteAnalystBlock(manifest)
