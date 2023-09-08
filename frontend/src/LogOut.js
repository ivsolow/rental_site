import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { remove } from 'react-cookies';

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
    fetch('http://127.0.0.5/auth/token/logout/', {
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




// import React, { useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { remove } from 'react-cookies';

// function Logout() {
//   const navigate = useNavigate();

//   useEffect(() => {
//     // Получить токен из куки
//     const cookies = document.cookie.split('; ');
//     let equip_rent_token = null;

//     for (const cookie of cookies) {
//       const [name, value] = cookie.split('=');
//       if (name === 'equip_rent_token') {
//         equip_rent_token = value;
//         break;
//       }
//     }

//     if (!equip_rent_token) {
//       // Если токен отсутствует, сразу перенаправить пользователя на страницу авторизации
//       navigate('/login');
//       return;
//     }

//     // Выполнить запрос на разлогинивание
//     fetch('http://127.0.0.5/auth/token/logout/', {
//       method: 'POST',
//       headers: {
//         Authorization: `Token ${equip_rent_token}`,
//       },
//     })
//       .then(response => {
//         // Удалить токен из куки
//         remove('equip_rent_token');
//         // Опционально: перенаправить пользователя на другую страницу
//         navigate('/logout-success'); // Замените на путь, куда вы хотите перенаправить после разлогинивания
//       })
//       .catch(error => console.error('Error logging out:', error));
//   }, [navigate]);

//   return null; // Не отображаем ничего, так как мы перенаправляем пользователя автоматически
// }

// export default Logout;



// import React from 'react';
// import { useNavigate, Route } from 'react-router-dom';
// import { remove } from 'react-cookies';

// function Logout() {
//   const navigate = useNavigate();

//   const handleLogoutClick = () => {
//     // Получить токен из куки
//     const cookies = document.cookie.split('; ');
//     let equip_rent_token = null;

//     for (const cookie of cookies) {
//       const [name, value] = cookie.split('=');
//       if (name === 'equip_rent_token') {
//         equip_rent_token = value;
//         break;
//       }
//     }

//     if (!equip_rent_token) {
//       // Если токен отсутствует, сразу перенаправить пользователя на страницу авторизации
//       navigate('/login');
//       return;
//     }

//     // Выполнить запрос на разлогинивание
//     fetch('http://127.0.0.5/auth/token/logout/', {
//       method: 'POST',
//       headers: {
//         Authorization: `Token ${equip_rent_token}`,
//       },
//     })
//       .then(response => {
//         // Удалить токен из куки
//         remove('equip_rent_token');
//         // Опционально: перенаправить пользователя на другую страницу
//         navigate('/logout-success'); // Замените на путь, куда вы хотите перенаправить после разлогинивания
//       })
//       .catch(error => console.error('Error logging out:', error));
//   };

//   return (
//     <div>
//       <p>Вы уверены, что хотите выйти?</p>
//       <button onClick={handleLogoutClick}>Выйти</button>
//     </div>
//   );
// }

// export default Logout;

// // В вашем компоненте для маршрутизации
// <Route path="/logout" element={<Logout />} />



// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { remove } from 'react-cookies';

// function Logout() {
//   const navigate = useNavigate();
//   const [isLoggedOut, setIsLoggedOut] = useState(false);

//   const handleLogoutClick = () => {
//     // Получить токен из куки
//     const cookies = document.cookie.split('; ');
//     let equip_rent_token = null;

//     for (const cookie of cookies) {
//       const [name, value] = cookie.split('=');
//       if (name === 'equip_rent_token') {
//         equip_rent_token = value;
//         break;
//       }
//     }

//     console.log(equip_rent_token);

//     if (!equip_rent_token) {
//       // Если токен отсутствует, перенаправить пользователя на страницу авторизации
//       navigate('/login');
//       return;
//     }

//     // Выполнить запрос на разлогинивание
//     fetch('http://127.0.0.5/auth/token/logout/', {
//       method: 'POST',
//       headers: {
//         Authorization: `Token ${equip_rent_token}`,
//       },
//     })
//       .then(response => {
//         // Удалить токен из куки
//         remove('equip_rent_token');
//         setIsLoggedOut(true); // Устанавливаем состояние isLoggedOut в true после успешного разлогинивания
//       })
//       .catch(error => console.error('Error logging out:', error));
//   };

//   return (
//     <div>
//       {!isLoggedOut ? (
//         <div>
//           <p>Вы уверены, что хотите выйти?</p>
//           <button onClick={handleLogoutClick}>Выйти</button>
//         </div>
//       ) : (
//         <div>
//           <p>Спасибо, что были с нами!</p>
//           <p>Авторизуйтесь снова:</p>
//           <a href="/login">Авторизоваться снова</a>
//         </div>
//       )}
//     </div>
//   );
// }

// export default Logout;


// import React from 'react';
// import { useNavigate } from 'react-router-dom';
// import { remove } from 'react-cookies';

// function Logout() {
//   const navigate = useNavigate();

//   const handleLogoutClick = () => {
//     // Получить токен из куки
//     const cookies = document.cookie.split('; ');
//     let equip_rent_token = null;

//     for (const cookie of cookies) {
//       const [name, value] = cookie.split('=');
//       if (name === 'equip_rent_token') {
//         equip_rent_token = value;
//         break;
//       }
//     }

//     console.log(equip_rent_token);

//     if (!equip_rent_token) {
//       // Если токен отсутствует, перенаправить пользователя на страницу авторизации
//       navigate('/login');
//       return;
//     }

//     // Выполнить запрос на разлогинивание
//     fetch('http://127.0.0.5/auth/token/logout/', {
//       method: 'POST',
//       headers: {
//         Authorization: `Token ${equip_rent_token}`,
//       },
//     })
//       .then(response => {
//         // Удалить токен из куки
//         remove('auth_token');
//         // Перенаправить пользователя на страницу авторизации или куда угодно
//         navigate('/login'); // Замените на путь, куда вы хотите перенаправить после разлогинивания
//       })
//       .catch(error => console.error('Error logging out:', error));
//   };

//   return (
//     <div>
//       <p>Вы уверены, что хотите выйти?</p>
//       <button onClick={handleLogoutClick}>Выйти</button>
//     </div>
//   );
// }

// export default Logout;


// import React, { useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { remove } from 'react-cookies';


//   function Logout() {
//     const navigate = useNavigate();
  
//     useEffect(() => {
//       // Получить токен из куки
//       const authToken = document.cookie
//         .split('; ')
//         .find(row => row.startsWith('auth_token='))
//         .split('=')[1];
  
//       if (!authToken) {
//         // Если токен отсутствует, перенаправить пользователя на страницу авторизации
//         navigate('/login');
//         return;
//       }
  
//       // Выполнить запрос на разлогинивание
//       fetch('http://127.0.0.5/auth/token/logout/', {
//         method: 'POST',
//         headers: {
//           Authorization: `Token ${authToken}`,
//         },
//       })
//         .then(response => {
//           // Удалить токен из куки
//           remove('auth_token');
//           // Перенаправить пользователя на страницу авторизации или куда угодно
//           navigate('/login'); // Замените на путь, куда вы хотите перенаправить после разлогинивания
//         })
//         .catch(error => console.error('Error logging out:', error));
//     }, [navigate]);
  
//     return <div>Logging out...</div>;
//   }

// export default Logout;



// import React, { useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { remove } from 'react-cookies';

// function Logout() {
//   const navigate = useNavigate();

//   useEffect(() => {
//     // Получить токен из куки
//     const cookies = document.cookie.split('; ');
//     let equip_rent_token = null;
    
//     for (const cookie of cookies) {
//       const [name, value] = cookie.split('=');
//       if (name === 'equip_rent_token') {
//         equip_rent_token = value;
//         break;
//       }
//     }

//     console.log(equip_rent_token)
//     if (!equip_rent_token) {
//       // Если токен отсутствует, перенаправить пользователя на страницу авторизации
//       navigate('/login');
//       return;
//     }

//     // Выполнить запрос на разлогинивание
//     fetch('http://127.0.0.5/auth/token/logout/', {
//       method: 'POST',
//       headers: {
//         Authorization: `Token ${equip_rent_token}`,
//       },
//     })
//       .then(response => {
//         // Удалить токен из куки
//         remove('auth_token');
//         // Перенаправить пользователя на страницу авторизации или куда угодно
//         navigate('/login'); // Замените на путь, куда вы хотите перенаправить после разлогинивания
//       })
//       .catch(error => console.error('Error logging out:', error));
//   }, [navigate]);

//   return <div>Logging out...</div>;
// }

// export default Logout;
