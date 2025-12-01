# ohtuvarasto

[![GHA workflow_badge](https://github.com/TeemuVi/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/TeemuVi/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/TeemuVi/ohtuvarasto/graph/badge.svg?token=UB4E57P6C1)](https://codecov.io/github/TeemuVi/ohtuvarasto)

A warehouse management application with a modern Flask web interface.

## Features

- 📦 **Multiple Warehouse Management**: Create and manage multiple warehouses
- ➕ **Add Items**: Add inventory to warehouses with real-time capacity tracking
- ➖ **Remove Items**: Remove inventory from warehouses
- ✏️ **Edit Warehouses**: Modify warehouse properties (name, capacity)
- 🗑️ **Delete Warehouses**: Remove warehouses permanently
- 📊 **Visual Progress**: See warehouse capacity utilization at a glance
- 🎨 **Modern UI**: Beautiful gradient design with responsive layout

## Installation

```bash
# Install dependencies
poetry install
```

## Usage

### Web Interface

Run the Flask web application:

```bash
cd src
poetry run python app.py
```

Then open your browser and navigate to `http://127.0.0.1:5000`

#### Environment Variables

The following environment variables can be configured:

- `SECRET_KEY`: Secret key for Flask sessions (default: 'dev-secret-key-change-in-production')
- `FLASK_DEBUG`: Enable debug mode ('true' to enable, default: 'false')

**Production Example:**
```bash
export SECRET_KEY="your-secret-key-here"
export FLASK_DEBUG="false"
cd src
poetry run python app.py
```

### Command Line Demo

Run the command-line demo:

```bash
cd src
poetry run python index.py
```

## Testing

Run tests:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run coverage run --branch -m pytest
poetry run coverage report
```
