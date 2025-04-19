import locale

def formatMoneyNoDecimal(amount, currency='en_PH.UTF-8') -> str:
    locale.setlocale(locale.LC_ALL, currency)
    return f"₱{amount:,.0f}"

def formatMoney(amount, currency='en_PH.UTF-8') -> str:
    locale.setlocale(locale.LC_ALL, currency)
    return locale.currency(amount, grouping=True)