# Equipment rental site

### Бэкенд для сайта проката туристического снаряжения на Django Rest Framework.

<br>
<br>


#####  **Технологии:**  ############

    ● Python 3.11

    ● Django Rest Framework

    ● PostgreSQL

    ● Redis

    ● Celery

    ● pytest

    ● Docker, docker-compose

##### **Установка:** ############

<br>
1. Установите Docker и Docker Compose, если они еще не установлены. <br>
2. Создайте папку, куда будет склонирован проект. <br>
3. Перейдите в папку, склонируйте репозиторий. <br>
4. В корне каталога создайте файл ".env" и добавьте туда следующие строки: <br><br>
SECRET_KEY=   # секретный ключ Django <br>
YOOKASSA_ACCOUNT_ID=   # Укажите идентификатор аккаунта платежной системы Yookassa <br>
YOOKASSA_SECRET_KEY=   # Укажите секретный ключ платежной системы Yookassa <br>
DB_HOST=   'database' <br>
POSTGRES_DB=   # укажите имя базы данных PostgreSQL <br> 
POSTGRES_USER=   # укажите имя пользователя базы данных <br>
POSTGRES_PASSWORD=   # укажите пароль пользователя базы данных <br>
DJANGO_SETTINGS_MODULE=   equipment_rental_site.settings <br><br>

Секретный ключ можно сгенерировать с помощью следующего кода: <br>
```python
import random
import string

def generate_secret_key(length=50):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(characters) for _ in range(length))
    return secret_key

print(generate_secret_key())
```
<br> 
YOOKASSA_ACCOUNT_ID и YOOKASSA_SECRET_KEY - это данные, которые можно получить после регистрации
на сайте Юкассы и выбора тестового магазина. <br> 
4. Соберете контейнеры и запустите приложение командой: `docker-compose up` <br> 
5. Приложение будет доступно по адресу: 'http://localhost:8000'

##### **Приложения сайта:** ##########

    ● Пользователи(users): регистрация по адресу почты, без использования username. 
        Авторизация по токенам с помощью пакета Djoser.

    ● Снаряжение(equipment): список всего снаряжения, которое есть на сайте. Поля: Название, описание, доступное 
        количество, категория, фото(несколько), отзывы пользователей, рейтинг. Фильтрация и поиск по названию и 
        категории. После авторизации и выбора дат проката, появляется список снаряжения, которое доступно только на
        эти даты, с учетом уже имеющегося снаряжения в прокате. 

    ● Корзина(cart): Добавление нужного снаряжения в корзину, удаление, отображение списка корзины.
        Вывод корзины - перечесление позиций корзины: id, снаряжение(вложенные поля), количество, сумма, даты начала
        и конца проката, и в конце - общая сумма и общее количество позиций.

    ● Платежи(payment): сначала происходит проверка содержимого корзины на актуальность дат, и доступность снаряжения,
        которое есть в корзине(разность между общим доступным количеством и занятым), если все ок - идет перенаправление
        на формирования платежа. Платежная система - Yookassa. Отправляем json содержимого платежа, переходим на
        страницу оплаты Юкассы, затем на вебхук сайта поступает ответ статуса платежа и его детализация. 
        Если платеж успешен - у пользователя cоздается новая аренда, соответсвующие объекты удаляются из корзины, 
        также с помощью celery task отправляется письмо на почту об успешной оплате с деталями платежа.

    ● Прокат(rentals): данные о снаряжении, которое находится(или находилось) в прокате. 
        Поля модели: снаряжение, пользователь, количество, дата начала, дата окончания, прокат
        начался(пользователь забрал снаряжение), заказ закрыт.

    ● Отзывы(feedback): если пользователь воспользовался прокатом(поля Rentals.is_started=True и
        Rentals.is_closed=True), то он может поставить оценку, а также оставить отзыв с фото на каждую позицию
        снаряжения из данного проката. Также можно редактировать или удалить отзыв. Если пользователь удалит свой
        профиль, его отзыв останется со значением пользователя "deleted_user" 

        
##### **API эндпойны:** ##########

*Equipment:* <br>

    ● /api/v1/equipment/ [GET] - Получение списка снаряжения
    ● /api/v1/equipment/<int:pk>/ [GET] - Просмотр конкретной еденицы снаряжения
    ● /api/v1/equipment_dates/ [GET] - Получение списка снаряжения, доступного в определенные даты

*Cart:* <br>

    ● /api/v1/cart/ [GET] - Отображение содержимого корзины
    ● /api/v1/remove_from_cart/<int:pk>/<int:amount>/ [DELETE] - Удаление выбранного количества определенной позиции
    ● /api/v1/add_cart/ [POST] - Добавление снаряжения в корзину

*Feedback:* <br>
    
    ● /api/v1/feedback/ [GET], [PUT], [PATCH], [DELETE] - Оставить отзыв. +/<int:pk>/ -удалить/отредактировать
    ● /api/v1/equipment_for_feedback/ [GET] - получение списка снаряжения, на которое можно оставить отзыв

*Payment:* <br>

    ● /api/v1/cart_check/ [GET] - проверка корзины на актуальность дат и наличие снаряжения
    ● /api/v1/payment/ [POST] - форма для отправки платежа(поля: сумма, комиссия)
    ● /api/v1/payment_response/ [POST] - вебхук для получения статуса и деталей платежа
    ● /api/v1/payment_status/ [POST] - получение данных статуса об оплате

*Rentals:* <br>

    ● /api/v1/rentals/ [GET] - список снаряжения, которое есть(было) в аренде

*Users:* <br>

    ● /api/v1/auth/ [GET], [PUT], [PATCH], [DELETE] - авторизация пользователя
    ● /api/v1/auth/users/activation/ [PUT] - активация пользователя по почте
    ● /api/v1/auth/users/resend_activation/ [PUT] - повторная отправка письма активации
    ● /api/v1/auth/users/me/ [GET], [PUT], [PATCH], [DELETE] - текущий пользователь
    ● /api/v1/auth/users/reset_password/ [POST] - сбросить пароль
    ● /api/v1/auth/users/set_password/ [POST] - поменять пароль
    ● /auth/token/login [POST] - аутентификация пользователя по токену
    ● /auth/token/logout [POST] - выход из аккаунта(удаление токена)
    ● /api/v1/profile/ [GET], [PUT], [PATCH] - данные профиля пользователя

