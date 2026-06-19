# Tests for the Mergington High School FastAPI app

- Location: tests/
- Test runner: pytest
- Pattern: AAA (Arrange / Act / Assert)
- Deterministic: tests use an autouse fixture to backup and restore `src.app.activities` for each test.

## Setup

Create and activate a virtual environment, then install test dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest requests
```

## Run tests

```bash
pytest -q
```

## Notes

- The tests load `src/app.py` directly so they operate on the same module instance the app exposes.
- An autouse fixture in `tests/conftest.py` makes a deep copy of `activities` before each test and restores it after, ensuring tests are isolated and deterministic.
- Tests use the synchronous `TestClient` from `fastapi.testclient`.
