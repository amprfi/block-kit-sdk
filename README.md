# Ampr Block Kit SDK

The Ampr Block SDK provides a unified, well-documented interface for developing and testing blocks for the Ampr wallet.

Blocks are designed to run as independent, external services. They interface with a user's wallet core via the [XMTP messaging protocol](https://xmtp.org/). Blocks are stateless and receive all necessary context from the wallet core for each interaction. The user's PWA wallet is responsible for managing all user-specific state and passes the necessary context to block servers for each interaction.

## Types of Blocks?

Blocks are specialized modules that extend the functionality of a user's AI Wallet. There are two primary types:

### Analyst Blocks
*   **Focus:** Dedicated to research, data gathering, market analysis, signal generation, and providing informational summaries.
*   **Output:** Deliver data, charts, textual analysis, or informational alerts directly to the user's wallet.
*   **Interaction:** Analyst Blocks may receive data feeds or specific requests from the wallet, process them, and return insights.
*   *Disclaimer:* For regulatory reasons, Analyst Blocks strictly provide information and insights; they do **not** offer financial advice, "suggestions," or "highlight opportunities" that could be construed as recommendations for financial transactions unless a block developer has obtained and can demostrate to Ampersand Labs its license to do so.

### Action Blocks *(Coming Soon)*
*   **Focus:** Designed to propose and, upon user approval via their wallet, help manage investment strategies.
*   **Output:** Primarily generate `TransactionProposal` objects, which are sent to the wallet core for the user's review and explicit approval before any action is taken.
*   **Interaction:** Receive market data, user preferences, and `ControllerSettings` from the wallet. They use this information, along with their internal logic, to generate transaction proposals.
*   **Controller-Driven:** Action Blocks operate strictly within user-defined `ControllerSettings` which dictate their operational boundaries (e.g., authorized assets, transaction size limits, total cumulative limits).
*   *Disclaimer:* Ampersand Labs retains the right to review any block submitted to the Ampr Block Store for compliance with regulatory requirements. Activities carried out by blocks may be subject to local licensing requirements for which Ampersand Labs may require evidence of compliance.


## Core Concepts

Key components and data structures within the Block Kit:

-   **Manifest (`Manifest`):** A Pydantic model (`blocks/models.py`) describing a block's metadata, including its name, version, type ("analyst" or "action"), publisher, description, license, and structured fee information (`FeeDetail` models).
-   **Transaction Proposal (`TransactionProposal`):** (Action Blocks Only) A Pydantic model (`blocks/models.py`) defining the structure for a transaction proposed by an Action Block to the wallet core.
-   **Controller Settings (`ControllerSettings`):** A Pydantic model (`controller/models.py`) specifying the user-defined operational limits for an Action Block (e.g., `authorized_duration_days`, `asset_id`, `max_amount_per_transaction`, `cumulative_max_amount`). These are provided by the wallet to the Action Block.
-   **Fees (`FeeDetail` models):** A structured system (`blocks/models.py`) allowing blocks to define various types of fees (e.g., one-time, recurring, per-transaction).

## Installation

To install the Ampr Block SDK, you'll need Python 3.8 or later and Poetry for dependency management. Follow these steps:

1. **Install Poetry**:
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone the Repository**:
   ```sh
   git clone https://github.com/ampr-wallet/block-sdk.git
   cd block-sdk
   ```

3. **Install Dependencies**:
   ```sh
   poetry install
   ```

4. **Activate the Virtual Environment**:
   ```sh
   poetry shell
   ```
   
## Progress Checklist

- [x] Base block classes (`BaseBlock`, `AnalystBlock`)
- [x] Manifest model for block metadata
- [x] Fee structure models (`BaseFee`, `OneTimeFixedFee`, `RecurringFixedFee`)
- [x] Basic block initialization and management
- [ ] Implement communication via XMTP
- [ ] Add more block types (e.g., `ActionBlock`, `CustodialBlock`)
- [ ] Expand fee structure with more fee types
- [ ] Improve documentation with more examples
- [ ] Add end to end testing

## Contributions and License

Contributions to the Block Kit SDK are welcome! Please open an issue or submit a pull request. If you're interested in getting involved, you can check out our Discourse (link coming soon).

All code in this repository is licensed under the Apache License, Version 2.0. See the LICENSE file for details.

Copyright 2025 Ampersand Labs B.V.

