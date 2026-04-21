# Test Suite Overview

## Coverage
- API endpoints: `/api/inventory/add`, `/api/inventory/reduce`, `/health`, 
    `/` (root)
- Inventory logic: add, reduce, get, list, and error conditions
- Product logic: creation, property access, string representations
- TODO: Add unit tests for Order logic (creation, validation, 
    and business rules)
- Health and root endpoint: status and content-type

## Structure
- All tests are located in the `tests/` directory.
- All test modules are unit tests:
  - `test_api.py`: Unit tests for API endpoints (inventory add/reduce, 
      error handling; uses in-memory fakes)
  - `test_health.py`: Unit test for /health endpoint (status and response)
  - `test_inventory.py`: Unit tests for Inventory class (mocked, no persistence)
  - `test_product.py`: Unit tests for Product class (creation, properties,
      string output)
  - `test_repository.py`: Unit tests for repository classes (save, load, update;
      no real I/O)
  - `test_root.py`: Unit tests for root endpoint (status and content-type)

## Isolation
- All API tests use FastAPI's `TestClient`.
- Google Sheets access is patched using a `FakeRepo` and pytest's `monkeypatch` 
    to avoid real network calls.
- No test depends on external services or persistent state.
- Model tests use `MagicMock` or direct instantiation.

## Running Tests
- Run all tests: `pytest`
- Show slowest tests: `pytest --durations=10`
- Show print/debug output: `pytest -s`

## Notes
- All tests are independent and can be run in any order.
- Fixtures are used for setup and teardown.
- The suite is designed for speed and reliability.
