import locale

def formatMoneyNoDecimal(amount=0, currency='en_PH.UTF-8') -> str:
    if isinstance(amount, str):
        amount = float(amount)
        
    locale.setlocale(locale.LC_ALL, currency)
    return f"₱{amount:,.0f}"

def formatMoney(amount=0, currency='en_PH.UTF-8') -> str:
    if amount is None:
        amount = 0
    
    if isinstance(amount, str):
        amount = float(amount)
        
    locale.setlocale(locale.LC_ALL, currency)
    return locale.currency(amount, grouping=True)