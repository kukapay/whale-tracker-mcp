import os
from typing import Optional
import httpx
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("WHALE_ALERT_API_KEY")
BASE_URL = "https://api.whale-alert.io/v1"

if not API_KEY:
    raise ValueError("WHALE_ALERT_API_KEY environment variable is required")

# Initialize the MCP server
mcp = FastMCP("WhaleTracker", dependencies=["httpx"])

# Helper function to make API requests
async def fetch_from_api(endpoint: str, params: dict) -> dict:
    async with httpx.AsyncClient() as client:
        params["api_key"] = API_KEY
        response = await client.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

# Tool: Fetch recent whale transactions
@mcp.tool()
async def get_recent_transactions(
    blockchain: Optional[str] = None,
    min_value: Optional[int] = 500000,
    limit: int = 10
) -> str:
    """Fetch recent whale transactions, optionally filtered by blockchain and minimum value (USD)."""
    params = {
        "min_value": min_value,
        "limit": limit
    }
    if blockchain:
        params["blockchain"] = blockchain.lower()

    data = await fetch_from_api("transactions", params)
    if data["result"] != "success":
        return "Error fetching transactions"

    transactions = data["transactions"]
    return "\n".join(
        f"{tx['timestamp']} - {tx['blockchain']} - {tx['amount_usd']} USD "
        f"(Tx ID: {tx['id']})"
        for tx in transactions
    )

# Tool: Get details of a specific transaction
@mcp.tool()
async def get_transaction_details(transaction_id: str) -> str:
    """Fetch details of a specific whale transaction by its ID."""
    params = {"id": transaction_id}
    data = await fetch_from_api("transaction", params)
    if data["result"] != "success":
        return f"Error fetching transaction {transaction_id}"

    tx = data["transaction"]
    return (
        f"Transaction ID: {tx['id']}\n"
        f"Blockchain: {tx['blockchain']}\n"
        f"Timestamp: {tx['timestamp']}\n"
        f"Amount: {tx['amount']} {tx['symbol']} (${tx['amount_usd']} USD)\n"
        f"From: {tx['from'].get('address', 'Unknown')}\n"
        f"To: {tx['to'].get('address', 'Unknown')}"
    )

# Resource: Dynamic transaction data
@mcp.resource("whale://transactions/{blockchain}")
async def get_transactions_by_blockchain(blockchain: str) -> str:
    """Expose recent whale transactions for a specific blockchain as a resource."""
    params = {
        "blockchain": blockchain.lower(),
        "min_value": 500000,
        "limit": 5
    }
    data = await fetch_from_api("transactions", params)
    if data["result"] != "success":
        return f"No transactions found for {blockchain}"

    transactions = data["transactions"]
    return "\n".join(
        f"{tx['timestamp']} - {tx['amount_usd']} USD (Tx ID: {tx['id']})"
        for tx in transactions
    )

# Prompt: Query whale activity
@mcp.prompt()
def query_whale_activity(blockchain: Optional[str] = None) -> str:
    """Generate a prompt to analyze whale activity on a specific blockchain."""
    if blockchain:
        return f"Analyze recent whale transactions on {blockchain}. What patterns do you notice?"
    return "Analyze recent whale transactions across all blockchains. What patterns do you notice?"

# Run the server directly (optional)
if __name__ == "__main__":
    mcp.run()