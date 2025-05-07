# Whale Tracker MCP Server


**A Model Context Protocol (MCP) server for tracking cryptocurrency whale transactions using the Whale Alert API**

[![mit license](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/license/mit/)
[![python versions](https://img.shields.io/pypi/pyversions/mcp)](https://www.python.org/downloads/)
[![smithery badge](https://smithery.ai/badge/@kukapay/whale-tracker-mcp)](https://smithery.ai/server/@kukapay/whale-tracker-mcp)

<!-- omit in toc -->
## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Running in Development Mode](#running-in-development-mode)
  - [Integrating with Claude Desktop](#integrating-with-claude-desktop)
  - [Direct Execution](#direct-execution)
- [Examples](#examples)
- [API Key Configuration](#api-key-configuration)
- [License](#license)
- [Acknowledgements](#acknowledgements)


## Overview

The `whale-tracker-mcp` server is a Python-based implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) that integrates with the [Whale Alert API](https://docs.whale-alert.io/#endpoints). It enables real-time tracking and analysis of large cryptocurrency transactions ("whale" movements) by exposing tools, resources, and prompts to MCP-compatible clients like Claude Desktop.

This server is designed for cryptocurrency enthusiasts, developers, and analysts who want to monitor whale activity directly within their LLM-powered workflows.

## Features

- **Tools**:
  - `get_recent_transactions`: Fetch recent whale transactions with optional filters for blockchain, minimum value, and limit.
  - `get_transaction_details`: Retrieve detailed information about a specific transaction by its ID.
- **Resources**:
  - `whale://transactions/{blockchain}`: Expose recent transactions for a specified blockchain as contextual data.
- **Prompts**:
  - `query_whale_activity`: A reusable template for analyzing whale transaction patterns, optionally filtered by blockchain.
- **Asynchronous API Calls**: Uses `httpx` for efficient, non-blocking requests to the Whale Alert API.
- **Environment Variable Support**: Securely manage your API key via a `.env` file.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **Whale Alert API Key**: Sign up at [whale-alert.io](https://whale-alert.io/) to obtain an API key.
- **MCP Client**: Compatible with MCP clients like Claude Desktop or the MCP Inspector.

## Installation

### Installing via Smithery

To install Whale Tracker for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@kukapay/whale-tracker-mcp):

```bash
npx -y @smithery/cli install @kukapay/whale-tracker-mcp --client claude
```

1. **Clone the repository**:
```bash
git clone https://github.com/kukapay/whale-tracker-mcp.git
cd whale-tracker-mcp
```
2. Install dependencies: We recommend using uv for dependency management:
```bash
uv add "mcp[cli]" httpx python-dotenv
```   
Alternatively, use pip:
```bash
pip install mcp httpx python-dotenv
```
3. Set up your API key: Create a .env file in the project root and add your Whale Alert API key:
```
WHALE_ALERT_API_KEY=your_api_key_here
```

## Usage
### Running in Development Mode

Test the server locally with the MCP Inspector:

```bash
mcp dev whale_tracker.py --with-editable .
```

This opens a web interface where you can explore the server's tools, resources, and prompts.

### Integrating with Claude Desktop

Install the server into Claude Desktop for seamless integration:

```bash
mcp install whale_tracker.py --name "WhaleTracker" -f .env
```

- `--name "WhaleTracker"`: Sets a custom name for the server in Claude Desktop.
- `-f .env`: Loads the API key from the .env file.

Restart Claude Desktop after installation. Look for the hammer icon in the input box to confirm the server is loaded, then try commands like:

- "Show me recent whale transactions on Bitcoin."
- "Get details for transaction ID 123456789."
- "Analyze whale activity on Ethereum."

### Direct Execution

Run the server standalone for custom deployments:

```bash
python whale_tracker.py
```

Or use the MCP CLI:

```bash
mcp run whale_tracker.py
```

## Examples

Here’s how you might interact with the server in Claude Desktop:

### Fetch Recent Transactions:

```text
What are the latest whale transactions on Ethereum with a minimum value of $1,000,000?
```
The server calls `get_recent_transactions` with `blockchain="ethereum"` and `min_value=1000000`.

### Get Transaction Details:

```text
Tell me about transaction ID 123456789.
```

The server uses `get_transaction_details` to fetch and display the transaction data.

### Analyze Whale Activity:

```text
Analyze recent whale transactions on Bitcoin.
```

The `query_whale_activity` prompt triggers an analysis based on the `whale://transactions/bitcoin` resource.

## API Key Configuration

The server requires a Whale Alert API key, which is loaded from the `WHALE_ALERT_API_KEY` environment variable. To configure it:

- Create a .env file:
```text
WHALE_ALERT_API_KEY=your_api_key_here
```
- Ensure `python-dotenv` is installed (included in the dependencies).
- The server will automatically load the key at startup.

Alternatively, pass the key directly when running the server:

```bash
mcp install whale_tracker.py -v WHALE_ALERT_API_KEY=your_api_key_here
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Whale Alert for providing the API to track cryptocurrency whale transactions.
- Model Context Protocol team for the MCP specification and Python SDK.
- httpx for a robust HTTP client library.

Happy whale tracking! 🐳
