from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

# Тест №1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result
            содержится слово key'''
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
    print(f'\nдобавлен {result}')


# Тест №2
def test_get_all_pets_with_valid_key(filter=''):
   """Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
   _, api_key = pf.get_api_key(valid_email, valid_password)
   status, result = pf.get_list_of_pets(api_key, filter)
   assert status == 200
   assert len(result['pets']) > 0
   print(f'\nсписок всех питомцев не пустой')

#Тест №3
def test_add_pets_with_valid_data(name='Huge cat', animal_type='cat', age='3', pet_photo='images/Cat.jpg'):
    ''' Проверяем, что можно добавить питомца с корректными данными'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['name'] == name
    print(f'\nдобавлен {result}')

#Тест №4
def test_delete_pet():
    '''Проверяем возможность удаления питомца'''

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять
    # запрашиваем список своих питомцев.
    if len(my_pets['pets']) == 0:

        pf.add_new_pets(auth_key, 'Huge cat', 'cat', '3', 'images/Cat.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pets(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print(f'\nв списке осталось: {num} питомцев')

#Тест №5
def test_update_pet_info(name='V', animal_type='кошечка', age='1'):
    '''Проверяем возможность изменения данных питомца'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print(f'\nданные изменены с новым именем:  {name}')

    else:
# если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#Тест №6
def test_add_pets_with_valid_data_without_photo(name='КошаБезФото', animal_type='кошара', age='1'):
    '''Проверяем возможность добавления нового питомца без фото'''

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['name'] == name
    print(f'\nдобавлен {name}')

#Тест №7
def test_add_photo_at_pet(pet_photo='images/Cat2.jpeg'):
    '''Проверяем возможность добавления новой фотографии питомца'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        print(f'\nфото добавлено')
    else:
        raise Exception("Питомцы отсутствуют")
#Тест №8
def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным email.
            Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print(f'\nСтатус {status} для теста с неправильным email')

#Тест №9
def test_get_api_key_with_correct_mail_and_wrong_passwor(email=valid_email, password=invalid_password):
    """Проверяем запрос с правильным email и c неправильным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print(f'\nСтатус {status} для теста с неправильным паролем')


# Тест №10
def test_get_api_key_with_wrong_email_and_with_wrong__password(email=invalid_email, password=invalid_password):
    """Проверяем запрос с невалидным email и с невалидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print(f'\nСтатус {status} для теста с неверными: email и паролем')

#Тест 11
def test_add_pet_with_valid_data_empty_field():
    """Проверяем добавление питомца с пустыми полями. Тест выводит предупреждение"""
    name = ''
    animal_type = ''
    age = ''
    #  Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['name'] == name
    print(f'\nВнимание!!! Сайт позволяет добавлять питомцев с "пустыми" данными  {result}')

#Тест 12
def test_add_pet_negative_age_number(name='Cat', animal_type='cat', age='-3', pet_photo='images/Cat.jpg'):
    ''' Добавление питомца с отрицательным числом в переменную age (возраст).
    Тест выводит предупреждение'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['age'] == age
    print(f'\nВнимание!!! Сайт позволяет добавлять питомцев с отрицательным возрастом:  {age}')

#Тест 13
def test_add_pet_with_special_characters_in_variable_animal_type(name='Cat', animal_type = 'C%*№"', age='3',
                                                                 pet_photo='images/Cat2.jpeg'):
    ''' Добавление питомца со специальными символами вместо букв
    в переменную animal_type. Тест выводит предупреждение.'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['animal_type'] == animal_type
    print(f'\nВнимание!!! Сайт позволяет добавлять питомцев со специальными символами вместо букв: {animal_type}')

#Тест14
def test_add_pet_with_four_digit_age_number(name='Moty', animal_type = 'cat', age='6788',pet_photo='images/Cat2.jpeg'):
    ''' Добавление питомца с числом превышающим два знака в поле возраст.
    Тест выводит предупреждение.'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert result['age'] == age
    print(f'\nВнимание!!! Сайт позволяет добавлять питомцев с числом превышающим два знака в поле возраст: {age}')


#Тест 15
def test_add_pet_with_a_lot_of_symbol_in_variable_animal_type(name='Korica', age='3', pet_photo='images/Cat2.jpeg'):
    """Добавление питомца с полем "Порода" (animal_type), которое имеет слишком длинное значение.
    Тест выводит предупреждение."""

    animal_type = 'QypёGnMnhFepDelGzbBbuEzxfrPHUvdKsPKlCrApxHSCnchktC'
    #  Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type']#.split()
    symbol_count = len(list_animal_type)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert symbol_count > 25
    print(f'\nВнимание!!! Добавлен питомец с названием более, чем из 25 символов : {symbol_count}')



