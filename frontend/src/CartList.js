
import React, { useEffect, useState } from 'react';
import cookie from 'react-cookies'; // Импортируем библиотеку для работы с куками
import { Link, useNavigate } from 'react-router-dom';


function Cart() {
  const [cartData, setCartData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    // Получаем токен из куки
    const authToken = cookie.load('equip_rent_token');
      const ipAddress = process.env.BACKEND_SERVER_IP || '0.0.0.0';
      const port = process.env.BACKEND_SERVER_PORT || '1337';
      const serverAddress = `http://${ipAddress}:${port}`;

    if (!authToken) {
      // Если токен отсутствует, устанавливаем сообщение об ошибке
      setErrorMessage('Please log in to access this resource');
      return;
    }

    // Выполнить GET-запрос к эндпоинту корзины пользователя с использованием токена из куки
    fetch(`${serverAddress}/api/v1/cart`, {
      method: 'GET',
      headers: {
        Authorization: `Token ${authToken}`, // Используем токен из куки
      },
    })
      .then(response => {
        if (response.status === 401) {
          // Если сервер вернул ошибку 401, устанавливаем сообщение о неавторизации
          setErrorMessage('You are not authorized. Please log in to access this resource.');
          return;
        }
        return response.json();
      })
      .then(data => {
        if (data) {
          setCartData(data);
        }
      })
      .catch(error => {
        console.error('Error fetching cart data:', error);
      });
  }, []);

  if (errorMessage) {
    return <div>{errorMessage} <Link to="/login">Log in</Link></div>; // Отобразить сообщение об ошибке
  }

  if (!cartData) {
    return <div>Loading...</div>; // Отобразить сообщение о загрузке данных
  }

  return (
    <div>
      <h1>Cart Contents</h1>
      <p>Total Positions: {cartData.total_positions}</p>
      <p>Total Sum: {cartData.total_summ}</p>

      <h2>Cart Items</h2>
      {cartData.cart_item_data && cartData.cart_item_data.length > 0 ? (
        <ul>
          {cartData.cart_item_data.map(cartItem => (
            <li key={cartItem.cart_id}>
              <h3>{cartItem.equipment.name}</h3>
              <p>Price: {cartItem.equipment.price}</p>
              <p>Amount: {cartItem.amount}</p>
              <p>Sum: {cartItem.summ}</p>
              <p>Start Date: {cartItem.dates.date_start}</p>
              <p>End Date: {cartItem.dates.date_end}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>Your cart is empty.</p>
      )}
    </div>
  );
}

export default Cart;
