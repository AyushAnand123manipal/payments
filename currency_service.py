"""
Currency conversion service for PayPal Clone.
"""
import requests
import json
import os
from datetime import datetime, timedelta
from flask import current_app, session
from decimal import Decimal, ROUND_HALF_UP

# Hardcoded rates for demonstration purposes
# In a real app, these would be fetched from an API
EXCHANGE_RATES = {
    "USD": Decimal('1.0'),
    "EUR": Decimal('0.91'),
    "GBP": Decimal('0.77'),
    "JPY": Decimal('153.72'),
    "CAD": Decimal('1.35'),
    "AUD": Decimal('1.48'),
    "INR": Decimal('83.77'),
    "CNY": Decimal('7.23')
}

# List of supported currencies with symbols
SUPPORTED_CURRENCIES = {
    "USD": {"name": "US Dollar", "symbol": "$"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "GBP": {"name": "British Pound", "symbol": "£"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$"},
    "INR": {"name": "Indian Rupee", "symbol": "₹"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥"}
}

def get_currency_symbol(currency_code):
    """Get the currency symbol for a given currency code"""
    symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CAD': 'C$',
        'AUD': 'A$',
        'INR': '₹',
        'CNY': '¥'
    }
    return symbols.get(currency_code, currency_code)

def get_supported_currencies():
    """Return the list of supported currencies."""
    return SUPPORTED_CURRENCIES

def convert_amount(amount, from_currency, to_currency):
    """
    Convert an amount from one currency to another.
    
    Args:
        amount (float): The amount to convert
        from_currency (str): 3-letter currency code to convert from
        to_currency (str): 3-letter currency code to convert to
        
    Returns:
        float: The converted amount
    """
    if not amount or not from_currency or not to_currency:
        return 0.0
        
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency == to_currency:
        return float(amount)
    
    try:
        # Convert to Decimal for precise calculations
        amount = Decimal(str(amount))
        
        # Convert to USD first (as base currency)
        from_rate = EXCHANGE_RATES.get(from_currency, Decimal('1.0'))
        amount_in_usd = amount / from_rate
        
        # Convert from USD to target currency
        to_rate = EXCHANGE_RATES.get(to_currency, Decimal('1.0'))
        converted_amount = amount_in_usd * to_rate
        
        # Round to 2 decimal places
        return float(converted_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    except Exception as e:
        current_app.logger.error(f"Currency conversion error: {e}")
        return float(amount)  # Return original amount on error

def format_currency(amount, currency_code):
    """Format the amount with the appropriate currency symbol"""
    symbol = get_currency_symbol(currency_code)
    if currency_code == 'INR':
        return f'₹{amount:,.2f}'
    elif currency_code in ['USD', 'EUR', 'GBP', 'CAD', 'AUD']:
        return f'{symbol}{amount:,.2f}'
    elif currency_code in ['JPY', 'CNY']:
        return f'{symbol}{amount:,.0f}'
    else:
        return f'{amount:,.2f} {currency_code}'

def update_exchange_rates():
    """
    Update exchange rates from an external API.
    This function is a placeholder - in a real app, you would use an API like Open Exchange Rates,
    Fixer.io, or similar services.
    """
    try:
        # This would be a real API call in production
        # Example with Open Exchange Rates:
        # app_id = os.environ.get("OPEN_EXCHANGE_RATES_APP_ID")
        # response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={app_id}")
        # data = response.json()
        # return data["rates"]
        
        # For now, just return our static rates
        return EXCHANGE_RATES
    except Exception as e:
        current_app.logger.error(f"Failed to update exchange rates: {e}")
        return EXCHANGE_RATES