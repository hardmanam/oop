import json


class RegisterMixin:
    def __max_id(self,data):
        if data:
            ids = [i['id'] for i in data]
            return max(ids) + 1
        return 1
    def register(self, name, password):
        if name in [user['name'] for user in data_names]:
            raise Exception('Такой юзер уже существует!')
        data_names.append({
            'id': self.__max_id(data_names),
            'name': name,
            'password': validate_password(password)
            })
        json.dump(data_names, open('user.json', 'w'), sort_keys=True, indent=4)
        return 'Регистрация прошла успешно'

class LoginMixin:
    def login(self, name, password):
        if name in [user['name'] for user in data_names]:
            user = [i for i in data_names if name == i['name']] 
            if password == user[0]['password']:
                return 'Вы успешно залогинились!'
            raise Exception('Неверный пароль!')
        return 'Нет такого юзера в БД' 


class ChangePasswordMixin:
    def change_password(self, name, password, new_password):        
        validate_password(new_password)
        user = [i for i in data_names if name == i['name']]
        if password == user[0]['password']:
            index = data_names.index(user[0])
            data_names[index]['password'] = new_password
            json.dump(data_names, open('user.json', 'w'), sort_keys=True, indent=4)
            return 'Успешно поменяли пароль'
        raise Exception('Старый пароль не совпадает')

class ChangeUserNameMixin:
    def __correct_name(self,name):
        names = [user['name'] for user in data_names]
        while name in names:
            print('Пользователь с наким именем существует')
            name = input('Введите новое имя: ')
        return name
    def change_name(self, name, new_name):
        names = [user['name'] for user in data_names]
        if name in names:
            user = [user for user in data_names if name == user['name']]
            index = data_names.index(user[0])
            data_names[index]['name'] = self.__correct_name(new_name)
            json.dump(data_names, open('user.json', 'w'), sort_keys=True, indent=4)
            return 'Успешно сменили имя'
        raise Exception('Нет такого юзера в БД')

class CheckOwnerMixin:
    def check(self, owner):
        if owner in [user['name'] for user in data_names]:
            return 'Пост успешно создан'
        raise Exception('Нет такого пользователя')


class User(RegisterMixin, LoginMixin, ChangePasswordMixin, ChangeUserNameMixin):
    pass

class Post(CheckOwnerMixin):
    def __init__(self, title, description, price, quantity, owner):
        self.title = title
        self.description = description
        self.price = price
        self.quantity = quantity
        self.owner = self.check(owner)
    def post(self):
        post = {'title': self.title, 'description': self.description, 'price': self.price, 'quantity': self.quantity}
        print('Пост создан')

def validate_password(pass1):
    if len(pass1) <= 8:
        raise Exception('Пароль слишком короткий')
    elif pass1.isdigit() or pass1.isalpha():
        raise Exception('Пароль должен состоять из букв и цифр!')
    return pass1


data_names = json.load(open('user.json'))
obj1 = User()
print(obj1.register('John111', '12345667ad'))
print(obj1.login('John111', '12345667ad'))
print(obj1.change_password('John111', '12345667ad', '123456789a'))
print(obj1.login('John111', '123456789a'))
print(obj1.change_name('John111' , 'john321'))
# John111 = Post('pen', 'green', 10, 1, 'john321')
# John111.post()

