import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { remove } from 'react-cookies';
import serverAddress from './config';


function Logout() {
  const navigate = useNavigate();
  const [isLoggedOut, setIsLoggedOut] = useState(false);

  useEffect(() => {
    // Получить токен из куки
    const cookies = document.cookie.split('; ');
    let equip_rent_token = null;

    for (const cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name === 'equip_rent_token') {
        equip_rent_token = value;
        break;
      }
    }

    if (!equip_rent_token) {
      // Если токен отсутствует, перенаправить пользователя на страницу авторизации
      navigate('/login');
    }
  }, [navigate]);

  const handleLogoutClick = () => {
    // Получить токен из куки
    const cookies = document.cookie.split('; ');
    let equip_rent_token = null;

    for (const cookie of cookies) {
      const [name, value] = cookie.split('=');
      if (name === 'equip_rent_token') {
        equip_rent_token = value;
        break;
      }
    }

    if (!equip_rent_token) {
      // Если токен отсутствует, перенаправить пользователя на страницу авторизации
      navigate('/login');
      return;
    }

    // Выполнить запрос на разлогинивание
    fetch(`${serverAddress}/auth/token/logout/`, {
      method: 'POST',
      headers: {
        Authorization: `Token ${equip_rent_token}`,
      },
    })
      .then(response => {
        // Удалить токен из куки
        remove('equip_rent_token');
        setIsLoggedOut(true); // Устанавливаем состояние isLoggedOut в true после успешного разлогинивания
      })
      .catch(error => console.error('Error logging out:', error));
  };

  return (
    <div>
      {!isLoggedOut ? (
        <div>
          <p>Вы уверены, что хотите выйти?</p>
          <button onClick={handleLogoutClick}>Выйти</button>
        </div>
      ) : (
        <div>
          <p>Спасибо, что были с нами!</p>
          <p>Авторизуйтесь снова:</p>
          <a href="/login">Авторизоваться снова</a>
        </div>
      )}
    </div>
  );
}

export default Logout;

