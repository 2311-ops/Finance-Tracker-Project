from datetime import datetime
cat ={'I':'income' , 'E':'expence'}
datef =   '%d-%m-%Y'
def get_date(prompt, allow_def = False):
    date_str = input(prompt)
    if allow_def and not date_str:
        return datetime.today().strftime(datef)
    try:
        valid_date = datetime.strptime(date_str ,datef)
        return valid_date.strftime(datef)    
    except ValueError:
        print('invalid date.')
        return get_date(prompt , allow_def)
def get_amount():
    try:
        amount = float(input('enter the amount: '))
        if amount <= 0:
            raise ValueError('amount must be above zero.')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input('enter the category I = income , E = expense: ').upper()
    if category in cat:
        return cat[category]
    print('invalid category , enter either i , or e: ')
    return get_category()

def get_desc():
    return input('enter the description: ')