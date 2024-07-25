from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel
import os
from api_requests import request_crypto_prices, request_gold_price


class CalculateCryptoPortfolio(BaseModel):
    pass


class CalculateGoldPortfolio(BaseModel):
    pass


@tool(args_schema=CalculateCryptoPortfolio, return_direct=False)
def get_crypto_portfolio_value():
    """Calculates the user's current crypto portfolio value in US dollars"""
    amount_cardano = float(os.getenv("AMOUNT_CARDANO"))
    amount_ethereum = float(os.getenv("AMOUNT_ETHEREUM"))
    amount_ripple = float(os.getenv("AMOUNT_RIPPLE"))
    amount_vechain = float(os.getenv("AMOUNT_VECHAIN"))

    value_cardano, value_ethereum, value_ripple, value_vechain = request_crypto_prices()
    value = amount_cardano * value_cardano + amount_ethereum * value_ethereum + amount_ripple * value_ripple + amount_vechain * value_vechain

    print(f"Crypto portfolio value calculated: {value}")
    return value


@tool(args_schema=CalculateGoldPortfolio, return_direct=False)
def get_gold_portfolio_value():
    """Calculates the user's current gold portfolio value in US dollars"""
    amount_gold = float(os.getenv("AMOUNT_GOLD"))
    value = request_gold_price() * amount_gold

    print(f"Gold portfolio value calculated: {value}")
    return value
