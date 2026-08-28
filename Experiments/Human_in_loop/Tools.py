
from Helper import get_customer_details, search_orders, issue_refund

tools = [
    {
        "name": "Get Customer Details",
        "description": "Get customer details",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "Search Orders",
        "description": "Search orders of a customer",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "Issue Refund",
        "description": "Issue refund for a customer",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer ID"
                },
                "amount": {
                    "type": "number",
                    "description": "Amount to refund"
                }
            },
            "required": ["customer_id", "amount"]
        }
    }
]