def get_balance_and_currency_count(exchange):
    """
    Fetches the USDT balance and the count of non-zero currency balances.

    Parameters:
    exchange (object): An exchange object with a `fetchBalance` method.

    Returns:
    tuple: (usdt_balance, number_of_currencies) if both are > 0, else (None, 0).

    Example:
    usdt_balance, currency_count = get_balance_and_currency_count(exchange)
    """
    try:
        balance = exchange.fetchBalance()

        usdt_balance = balance['total'].get('USDT', -1)
        if usdt_balance != -1:
            print(f"Your USDT balance on KuCoin: {usdt_balance}")

        total_balances = balance['total']
        non_zero_currencies = {currency: amount for currency, amount in total_balances.items() if amount > 0}
        number_of_currencies = len(non_zero_currencies)

        if usdt_balance > 0 and number_of_currencies > 0:
            return usdt_balance, number_of_currencies

        return None, 0

    except Exception as e:
        print(f"Error fetching balance: {e}")
        return None, 0

