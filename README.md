# Block Kit

This repository provides two main resources for developers looking to build "blocks" – agentic modules for the AI Wallet ecosystem:

1.  **Block Kit SDK (`block_kit_sdk`):** A Python library that developers will install (e.g., via `pip install block-kit-sdk` once published). It provides the foundational tools, base classes (like `AnalystBlock`, `ActionBlock`), Pydantic data models (for `Manifest`, `TransactionProposal`, `ControllerSettings`, `FeeDetail`, etc.), WebSocket utilities, and other helper functions necessary to create custom blocks.
2.  **Scaffold Block Application:** The code in this repository also serves as a template FastAPI application. It demonstrates how to *use* the Block Kit SDK to create a runnable block server. Developers can clone or fork this scaffold as a quick starting point for their own block development.

Blocks are designed to run as independent, external servers. They interface with a user's wallet core (typically a PWA) via APIs and WebSockets. The architectural model is "Wallet-Managed State with External Blocks," meaning the user's wallet application manages user-specific state and provides necessary context to the block servers during interactions.

## What are Blocks?

Blocks are specialized modules that extend the functionality of a user's AI Wallet. There are two primary types:

### Analyst Blocks
*   **Focus:** Dedicated to research, data gathering, market analysis, signal generation, and providing informational summaries.
*   **Output:** Deliver data, charts, textual analysis, or informational alerts directly to the user's wallet.
*   **Interaction:** Analyst Blocks may receive data feeds or specific requests from the wallet, process them, and return insights.
*   **Important Note:** For regulatory reasons, Analyst Blocks strictly provide information and insights; they do **not** offer financial advice, "suggestions," or "highlight opportunities" that could be construed as recommendations for financial transactions.

### Action Blocks
*   **Focus:** Designed to propose and, upon user approval via their wallet, help manage investment strategies.
*   **Output:** Primarily generate `TransactionProposal` objects, which are sent to the wallet core for the user's review and explicit approval before any action is taken.
*   **Interaction:** Receive market data, user preferences, and `ControllerSettings` from the wallet. They use this information, along with their internal logic, to generate transaction proposals.
*   **Controller-Driven:** Action Blocks operate strictly within user-defined `ControllerSettings` which dictate their operational boundaries (e.g., authorized assets, transaction size limits, total cumulative limits).

## Architecture Overview

The Block Kit allows for blocks to be stateless in terms of user management and activity. The user's PWA wallet is responsible for managing all user-specific state and passes the necessary context to block servers for each interaction.

## Core Concepts

Key components and data structures within the Block Kit:

-   **Manifest (`Manifest`):** A Pydantic model (`blocks/models.py`) describing a block's metadata, including its name, version, type ("analyst" or "action"), publisher, description, license, and structured fee information (`FeeDetail` models).
-   **Transaction Proposal (`TransactionProposal`):** (Action Blocks Only) A Pydantic model (`blocks/models.py`) defining the structure for a transaction proposed by an Action Block to the wallet core.
-   **Controller Settings (`ControllerSettings`):** A Pydantic model (`controller/models.py`) specifying the user-defined operational limits for an Action Block (e.g., `authorized_duration_days`, `asset_id`, `max_amount_per_transaction`, `cumulative_max_amount`). These are provided by the wallet to the Action Block.
-   **WebSocket Communication:** The primary method for real-time, bidirectional communication between the user's PWA wallet and an active block server.
-   **Fees (`FeeDetail` models):** A structured system (`blocks/models.py`) allowing blocks to define various types of fees (e.g., one-time, recurring, per-transaction).

## Using the Block Kit SDK (for Block Developers)

To develop a block using the (future) installable SDK:

1.  **Install the SDK:**
    ```bash
    pip install block-kit-sdk # (Once published to PyPI)
    ```
2.  **Import necessary components:**
    ```python
    from block_kit_sdk.blocks import AnalystBlock, ActionBlock, Manifest
    from block_kit_sdk.models import TransactionProposal # (or from block_kit_sdk.blocks.models)
    from block_kit_sdk.controller import ControllerSettings
    # ... and other models/utilities
    ```
3.  **Create your Block Class:** Inherit from `AnalystBlock` or `ActionBlock`.
    ```python
    class MyAnalyst(AnalystBlock):
        async def perform_analysis(self, data: dict) -> dict:
            # Your custom analysis logic
            return {"insight": "Processed data"}

    class MyAction(ActionBlock):
        async def generate_proposal(self, market_data: dict) -> TransactionProposal:
            # Your custom proposal logic, respecting self.controller_settings
            # Ensure self.controller_manager.is_proposal_compliant(...) is checked
            pass
    ```
4.  **Define your Block's Manifest:** Create an instance of the `Manifest` model.
5.  **Integrate with a Server:** While the SDK provides core logic, you'll need a web server (like FastAPI, Flask, etc.) to expose it. The scaffold application in this repository provides a ready-to-use FastAPI setup.

## The Scaffold Block Application

This repository also serves as a scaffold or template for building a runnable block server using FastAPI and the Block Kit SDK.

### Prerequisites

-   Python 3.10+
-   Pip for package management
-   A virtual environment (e.g., `venv`) is highly recommended.

### Setting up the Scaffold

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amprfi/block-kit.git
    cd block-kit
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` includes FastAPI, Uvicorn. In the future, it would ideally list `block-kit-sdk` if it were a separate published package, or reference a local SDK module if developed as part of a monorepo structure).*

### Project Structure of the Scaffold

-   `main.py`: Main FastAPI application entry point.
-   `requirements.txt`: Python package dependencies for the scaffold.
-   `ws_handlers/`: Contains WebSocket connection handlers (e.g., `websocket_endpoint`).
-   `routes/`: Defines example HTTP API endpoint routers.
-   `blocks/`: Contains base classes (`base.py`) and Pydantic models (`models.py`) *provided by the SDK*. (In a true SDK setup, these would be imported from the installed `block_kit_sdk` package).
-   `controller/`: Contains logic for managing block controllers (`manager.py`) and Pydantic models for controller settings (`models.py`) *provided by the SDK*.
-   `utils/`: Utility functions (currently a placeholder, could be part of the SDK).

### Running the Scaffold Application

1.  Ensure your virtual environment is activated and dependencies are installed.
2.  Start the FastAPI application using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
3.  The application will typically be available at `http://127.0.0.1:8000`.

### API Endpoints (Scaffold Examples)

The scaffold block server exposes example HTTP API endpoints, prefixed with `/api/v1`:

-   **`GET /api/v1/manifest`**: Retrieves the block's `Manifest`.
    *   *Note: In a real block, this manifest would be dynamically loaded or defined by the block developer, not hardcoded as in the scaffold's `routes/__init__.py`.*
-   **`POST /api/v1/propose_transaction`**: (Action Blocks) An example endpoint.
    *   *Note: While available, the primary mechanism for Action Blocks to send proposals to the PWA wallet is expected to be via the WebSocket connection.* This HTTP endpoint might be used for other purposes, like internal testing or integration with a block's own backend services.
-   **`GET /api/v1/controller_settings`**: (Action Blocks) An example endpoint.
    *   *Note: `ControllerSettings` are primarily communicated from the PWA wallet to the Action Block via WebSocket during session initialization. This HTTP endpoint is less likely to be used by the PWA but could be useful for debugging or internal block logic.*

### WebSocket Endpoint (Scaffold Example)

-   **`/ws`**: An example WebSocket endpoint for real-time communication. The PWA wallet would connect here. The scaffold provides a basic echo server; a real block would implement its full WebSocket communication logic using handlers from the SDK or custom code.

### Configuration (Scaffold Example)

The scaffold (`routes/__init__.py`) demonstrates hardcoded `BLOCK_TYPE`, `DEFAULT_MANIFEST`, and `DEFAULT_CONTROLLER_SETTINGS`. A production block would:
-   Define its `Manifest` programmatically or load it from a configuration file.
-   Receive its `ControllerSettings` (if an Action Block) from the PWA wallet via the WebSocket connection when a user session starts.

## Developing Your Own Block

1.  **Choose Block Type:** Decide if you're building an Analyst or Action Block.
2.  **Set Up Project:**
    *   **Option A (Recommended for FastAPI):** Clone this scaffold repository and customize it.
    *   **Option B (Advanced):** Start a new Python project, `pip install block-kit-sdk` (when available), and integrate the SDK components with your chosen web framework.
3.  **Implement Core Logic:** Write the unique analysis or strategy logic for your block, subclassing from `AnalystBlock` or `ActionBlock`.
4.  **Define Manifest:** Create and populate the `Manifest` for your block.
5.  **Implement Communication:** Set up WebSocket handlers for interaction with the PWA wallet, using SDK utilities where appropriate.
6.  **Test Thoroughly:** Unit test and integration test your block's logic and communication.
7.  **Deploy:** Host your block server on your preferred infrastructure.
8.  **Register (Future Step):** Expect a process to register your block with Ampersand Labs to make it discoverable by AI Wallet users.

## Contributions and License

Contributions to the Block Kit SDK are welcome! Please open an issue or submit a pull request. If you're interested in getting involved, you can check out our [Discourse](https://www.discourse.org/).

All code in this repository is licensed under the Apache License, Version 2.0. See the LICENSE file for details.

Copyright 2025 Ampersand Labs B.V.
