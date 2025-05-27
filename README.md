# Block Kit

Block Kit is a library and SDK for developing agentic modules (blocks) that can be connected to a user's wallet. These blocks can perform research, provide analysis (Analyst Blocks), or execute automated investment management strategies (Action Blocks).

## Features

- **WebSocket Communication**: Real-time information exchange between the wallet core and active blocks.
- **Transaction Proposals**: Blocks propose transactions to the wallet core, which can then be executed.
- **Manifest**: An informational card specifying block details such as type, publisher, license, fees, and description.
- **Block Types**: Analyst and Action blocks.
- **Control**: Limitations on block transactions set by the user when installing the block.

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/block-kit.git
   cd block-kit
   ```

2. Install the required packages:
   ```bash
   pip install fastapi uvicorn
   ```

### Running the Application

1. Start the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API at `http://127.0.0.1:8000`.

### Endpoints

- **GET /blocks**: List of blocks
- **POST /blocks**: Create a new block
- **WebSocket /ws**: Real-time communication

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
