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
<pre>
SECRET_KEY= # секретный ключ Django <br>
YOOKASSA_ACCOUNT_ID= # Укажите идентификатор аккаунта платежной системы Yookassa <br>
YOOKASSA_SECRET_KEY= # Укажите секретный ключ платежной системы Yookassa <br>
DB_HOST='database' <br>
POSTGRES_DB= # укажите имя базы данных PostgreSQL <br> 
POSTGRES_USER= # укажите имя пользователя базы данных <br>
POSTGRES_PASSWORD= # укажите пароль пользователя базы данных <br>
DJANGO_SETTINGS_MODULE=equipment_rental_site.settings <br><br>
</pre>

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
YOOKASSA_ACCOUNT_ID и YOOKASSA_SECRET_KEY - это данные, которые можно получить после регистраци на сайте Юкассы и выбора тестового магазина. <br> 
5. Соберите контейнеры и запустите приложение командой: `docker-compose up` <br> 
6. Приложение будет доступно по адресу: 'http://localhost:8000'. Для полноценной работы с платежной 
системой(получения ответа от Юкассы) потребуется туннелирование ip-адреса локального хоста
(для этого подойдет сервис ngrok)

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

<br>
===========================================================================================================
<br>

# Equipment rental site

### Backend for a tourist equipment rental website built with Django Rest Framework.

<br>
<br>


#####  **Technologies:**  ############

    ● Python 3.11

    ● Django Rest Framework

    ● PostgreSQL

    ● Redis

    ● Celery

    ● pytest

    ● Docker, docker-compose

##### **Installation:** ############

<br>

1. Install Docker and Docker Compose if you haven't already. <br>
2. Create a directory where the project will be cloned. <br>
3. Navigate to the directory and clone the repository. <br>
4. Create a ".env" file in the root directory and add the following lines: <br><br>
<pre>
SECRET_KEY= # Django secret key <br>
YOOKASSA_ACCOUNT_ID= # Specify the YooKassa payment system account identifier <br>
YOOKASSA_SECRET_KEY= # Specify the YooKassa payment system secret key <br>
DB_HOST='database' <br>
POSTGRES_DB= # Specify the PostgreSQL database name <br> 
POSTGRES_USER= # Specify the database username <br>
POSTGRES_PASSWORD= # Specify the database password <br>
DJANGO_SETTINGS_MODULE=equipment_rental_site.settings <br><br>
</pre>
You can generate the secret key using the following code: <br>

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

YOOKASSA_ACCOUNT_ID and YOOKASSA_SECRET_KEY are the data you can obtain after registering on the YooKassa website and selecting a test shop. <br> 
5. Build the containers and run the application with the command: `docker-compose up` <br> 
6. The application will be available at: 'http://localhost:8000'. For full functionality with the payment system (receiving a response from YooKassa), you will need to tunnel the localhost IP address (you can use a service like ngrok). <br> <br> 

##### **Service Applications:** ##########

● users: registration with email address without using username. 
    Token-based authentication using the Djoser package.

● equipment: list of all equipment available on the site. Fields: Name, description, available quantity,
    category, photos (multiple), user reviews, rating. Filtering and searching by name and category. After
    authentication and selecting rental dates, a list of equipment available only for those dates will be displayed,
    taking into account the equipment already rented.

● cart: adding necessary equipment to the cart, removing items, displaying the cart list.
    Cart output includes cart items: id, equipment (nested fields), quantity, total price, start and end rental dates,
    and at the end - the total price and total number of items.

● payment: first, the content of the cart is checked for date relevance and availability of equipment
    present in the cart (difference between the total available quantity and the rented quantity). If everything is
    fine, the user is redirected to the payment page. The payment system used is YooKassa. A JSON containing the
    payment details is sent, then redirected to the YooKassa payment page, and finally, a webhook receives the payment
    status and its details. If the payment is successful, a new rental is created for the user, the corresponding items
    are removed from the cart, and a celery task is triggered to send an email to the user regarding the successful
    payment with payment details.

● rentals: data about the equipment currently or previously rented. 
    Model fields: equipment, user, quantity, start date, end date, rental started (user picked up the equipment), order closed.

● feedback: if a user has used the rental service (Rentals.is_started=True and Rentals.is_closed=True),
    they can leave a rating and review with photos for each equipment item from that rental. It is also possible to
    edit or delete a review. If a user deletes their profile, their review remains with the username "deleted_user".

        
##### **API Endpoints:** ##########

*Equipment:* <br>

    ● /api/v1/equipment/ [GET] - Get a list of equipment
    ● /api/v1/equipment/<int:pk>/ [GET] - Retrieve equipment item
    ● /api/v1/equipment_dates/ [GET] - Get a list of equipment available on specific dates


*Cart:* <br>

    ● /api/v1/cart/ [GET] - Display the cart contents
    ● /api/v1/remove_from_cart/<int:pk>/<int:amount>/ [DELETE] - Remove a specified quantity of a certain item
    ● /api/v1/add_cart/ [POST] - Add equipment to the cart


*Feedback:* <br>
    
    ● /api/v1/feedback/ [GET], [PUT], [PATCH], [DELETE] - Leave a feedback. +/<int:pk>/ - delete/edit
    ● /api/v1/equipment_for_feedback/ [GET] - Get a list of equipment items that available for feedback


*Payment:* <br>

    ● /api/v1/cart_check/ [GET] - Check the cart for date relevance and equipment availability
    ● /api/v1/payment/ [POST] - Form for submitting a payment (fields: amount, commission)
    ● /api/v1/payment_response/ [POST] - Webhook to receive payment status and details
    ● /api/v1/payment_status/ [POST] - Get payment status data


*Rentals:* <br>

    ● /api/v1/rentals/ [GET] - List of equipment currently or previously rented

*Users:* <br>

    ● /api/v1/auth/ [GET], [PUT], [PATCH], [DELETE] - User authentication
    ● /api/v1/auth/users/activation/ [PUT] - Activate user via email
    ● /api/v1/auth/users/resend_activation/ [PUT] - Resend activation email
    ● /api/v1/auth/users/me/ [GET], [PUT], [PATCH], [DELETE] - Current user
    ● /api/v1/auth/users/reset_password/ [POST] - Reset password
    ● /api/v1/auth/users/set_password/ [POST] - Change password
    ● /auth/token/login [POST] - User authentication using a token
    ● /auth/token/logout [POST] - Log out of the account (delete token)
    ● /api/v1/profile/ [GET], [PUT], [PATCH] - User profile data


