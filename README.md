# Block Kit

Block Kit provides a library and a template FastAPI server designed to be used by **individual agentic modules (blocks)**. Each block runs its own instance of this server, allowing it to interface with a user's wallet core (via APIs and WebSockets) and its own backend services. Blocks can perform research, provide analysis (Analyst Blocks), or propose automated investment management strategies (Action Blocks).

This `block-kit` repository serves as the foundational library that a block developer would use and customize. The server defined here is part of the block itself, not a central management system for multiple blocks.

## Features

- **WebSocket Communication**: Real-time information exchange between the wallet core and active blocks.
- **Transaction Proposals**: Blocks propose transactions to the wallet core, which can then be executed.
- **Manifest**: An informational card specifying block details such as type, publisher, license, fees, and description.
- **Block Types**: Analyst and Action blocks.
- **Control**: Limitations on block transactions set by the user when installing the block.

## Getting Started

### Prerequisites

- Python 3.10+
- Pip for package management
- A virtual environment, such as `venv` is recommended

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/amprfi/block-kit.git
    cd block-kit
    ```
2.  Create and activate a virtual environment (example using `venv`):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Project Structure

The project is organized into the following main directories:
-   `main.py`: The main FastAPI application entry point.
-   `requirements.txt`: Python package dependencies.
-   `ws_handlers/`: Contains WebSocket connection handlers.
-   `routes/`: Defines HTTP API endpoint routers.
-   `blocks/`: Contains base classes for blocks (`base.py`) and Pydantic models for block-related data structures (`models.py`).
-   `control/`: Contains logic for managing block controls/governors (`manager.py`) and Pydantic models for control settings (`models.py`).
-   `utils/`: Utility functions (currently a placeholder).

## Core Data Models

The system uses Pydantic models for data validation and serialization:

-   **`Manifest`** (`blocks/models.py`): Describes a block's metadata.
    -   Fields: `name`, `version`, `block_type` ("analyst" or "action"), `publisher`, `description`, `license` (optional), `fees` (Optional[List[FeeDetail]]; a list of structured fee objects, see `FeeDetail` and specific fee types like `OneTimeFixedFee`, `RecurringFixedFee`, etc., in `blocks/models.py`).
-   **`TransactionProposal`** (`blocks/models.py`): Structure for a transaction proposed by a block.
    -   Fields: `block_id`, `action_type` (e.g., "buy", "sell"), `asset_id`, `amount`, `currency`, `justification` (optional).
-   **`ControlSettings`** (`control/models.py`): Defines the operational limits for an Action Block.
    -   Fields: `authorized_duration_days`, `asset_id`, `max_amount_per_transaction`, `cumulative_max_amount`.

## Running the Application

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    Alternatively, you can run the `main.py` script directly (if it includes `uvicorn.run`):
    ```bash
    python main.py
    ```
3.  The application will typically be available at `http://127.0.0.1:8000`.

## API Endpoints

The block's server instance exposes the following HTTP API endpoints, prefixed with `/api/v1` (as configured in `main.py`):

-   **`GET /api/v1/manifest`**: Retrieves the manifest of this block instance.
    -   **Response**: The `Manifest` object for this block.

-   **`POST /api/v1/propose_transaction`**: Endpoint for the block to submit a transaction proposal. This would typically be called by the block's internal logic to send a proposal to the wallet core (if the wallet core polls this endpoint or if this block is part of a system where it pushes proposals).
    -   **Request Body**: A `TransactionProposal` object. The `block_id` field within the proposal should identify this block (e.g., using a unique ID from its manifest).
    -   **Response**: Status of the proposal (e.g., "proposed", "rejected_by_library_core") and details.

-   **`GET /api/v1/control_settings`** (For Action Blocks only): Retrieves the current control settings applied to this Action Block instance.
    -   **Response**: The `ControlSettings` object for this block. Returns 404 if not an Action Block or if settings are not configured.

### WebSocket Endpoint

-   **`/ws`**: A WebSocket endpoint for real-time communication between this block instance and the wallet core (currently a simple echo server for testing). The wallet core would connect to this endpoint on the block's server.

## Configuration

The specific details of the block (its `Manifest` and, for Action Blocks, its initial `ControlSettings`) are currently hardcoded in `routes/__init__.py` for demonstration (see `BLOCK_TYPE`, `DEFAULT_MANIFEST`, `DEFAULT_CONTROL_SETTINGS`). In a production block, these would be loaded from a configuration file (e.g., `config.yaml` or `.env`) or set via environment variables when the block's server instance is started. The `ControlSettings` for an Action Block are ultimately defined by the end-user via their wallet application and would be supplied to the block instance upon activation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
