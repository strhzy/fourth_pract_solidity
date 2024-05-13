from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import *
import pexpect

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=address_contract, abi=abi)

def check_pass(password):
    if len(password) < 12:
        print("Пароль должен быть больше 12 символов")
        return False

    if not any(item.islower() for item in password):
        print("Пароль должен содержать прописные буквы")
        return False
    
    if not any(item.isupper() for item in password):
        print("Пароль должен содержать строчные буквы")
        return False
    
    if not any(item.isdigit() for item in password):
        print("Пароль должен содержать числа")
        return False
    
    if not any(item in string.punctuation for item in password):
        print("Пароль должен содержать спец символы")
        return False

    return True

def new_acc():
    password = input("Введите пароль для нового аккаунта: ")
    if check_pass(password):
        account = w3.geth.personal.new_account(password)
        return account
    else:
        return 0

def auth():
    public_key = input("Введите ваш публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        check_sum = w3.to_checksum_address(public_key)
        w3.geth.personal.unlock_account(check_sum, password)
        print("\nАвторизация прошла успешно!\n")
        return check_sum
    except Exception as e:
        print(f"\nОшибка авторизации: {e}\n")
        return ''


def create_estate(account):
    size = int(input("Введите размер недвижимости: "))
    estate_address = input("Введите адрес недвижимости: ")
    es_type = int(input("Введите тип недвижимости: "))
    try:
        contract.functions.createEstate(size, estate_address, es_type).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")

def create_ad(account):
    price = int(input("Введите цену объявления: "))
    id_estate = int(input("Введите ID недвижимости: "))
    ad_status = int(input("Введите статус объявления: "))
    try:
        contract.functions.createAd(price, id_estate, ad_status).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")

def change_status_estate(account):
    id_estate = int(input("Введите ID недвижимости: "))
    try:
        contract.functions.changeStatusEstate(id_estate).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")

def change_status_ad(account):
    id_ad = int(input("Введите ID объявления: "))
    id_estate = int(input("Введите ID недвижимости: "))
    try:
        contract.functions.changeStatusAd(id_ad, id_estate).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")

def buy_estate(account):
    id_ad = int(input("Введите ID объявления: "))
    try:
        contract.functions.buyEstate(id_ad).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")
    
def withdraw(account):
    value = int(input("Введите сумму для вывода: "))
    try:
        contract.functions.withDraw(value).transact({'from': account})
    except Exception as e:
        print(f"Ошибка: {e}")
    
def get_balance_own(account):
    balance = w3.eth.get_balance(account)
    return balance

def get_balance_contr(address_account):
    balance = w3.eth.get_balance(address_account)
    return balance

def get_estates(account):
    try:
        estates = contract.functions.getEstates().call({'from': account})
        return estates
    except Exception as e:
        print(f"Ошибка: {e}")

def get_ads(account):
    try:
        ads = contract.functions.getAds().call({'from': account})
        return ads
    except Exception as e:
        print(f"Ошибка: {e}")

def pay(account):
    value = int(input("Введите сумму для контракта: "))
    try:
        contract.functions.pay().transact({'from': account, 'value': value})
    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    account = ""
    while True:
        if account=='':  
            choice = str(input('''
Выберите действие:
1. Регистрация
2. Авторизация
3. Выход из программы
'''))
            match choice:
                case "1":
                    print(new_acc())
                case "2":
                    account = auth()
                    print(account)
                case "3":
                    exit()
                case _:
                    print("Введите корректное значение")
        else:
            choice = str(input('''
Выберите действие:
1. Создать недвижимость
2. Создать объявление
3. Изменить статус недвижимости
4. Изменить статус объявления
5. Купить недвижимость
6. Вывести средства с контракта
7. Вывести мою недвижимость
8. Вывести доступные объявления
9. Вывести мой баланс
10. Вывести баланс смарт-контракта
11. Положить деньги на контракт
12. Выход из программы
'''))
            match choice:
                case "1":
                    create_estate(account)
                case "2":
                    create_ad(account)
                case "3":
                    change_status_estate(account)
                case "4":
                    change_status_ad(account)
                case "5":
                    buy_estate(account)
                case "6":
                    withdraw(account)
                case "7":
                    print(get_estates(account))
                case "8":
                    print(get_ads(account))
                case "9":
                    print(get_balance_own(account))
                case "10":
                    print(get_balance_contr(address_contract))
                case "11":
                    pay(account)
                case "12":
                    exit()
                case _:
                    print("Введите корректное значение")
main()