# Testing Guide — HA Irrigation Engine

## Overview
All Python modules, registry validators, entity adapters, and package generators must have unit tests with total coverage of positive cases, edge cases, and invalid configuration diagnostics.

## Test Structure
Tests are located in `tests/`:
- `test_registry.py`: Tests `src/registry/validator.py` with valid YAML configs, missing files, unknown adapters, duplicate IDs, and invalid zone targets.
- `test_adapters.py`: Tests `src/adapters/sonoff_swv.py` entity derivation and `src/adapters/factory.py` instantiation.
- `test_generator.py`: Tests `src/build/generator.py` HA package build tool output.
- `test_engine.py`: Tests engine state machine and operations.

## Running Tests
Run unit tests with pytest or Python unittest module:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
# or
pytest
```
