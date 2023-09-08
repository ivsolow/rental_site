import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import cookie from 'react-cookies';
import axios from 'axios';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Проверяем, есть ли уже у пользователя токен
    // const equipRentToken = document.cookie.replace(/(?:(?:^|.*;\s*)equip_rent_token\s*=\s*([^;]*).*$)|^.*$/, '$1');
    const authToken = cookie.load('equip_rent_token');
    console.log(authToken)

    // if (!authToken) {
    //   // Если токен отсутствует, устанавливаем сообщение об ошибке
    //   setErrorMessage('Please log in to access this resource');
    //   return;
    // }
    
    if (authToken) {
      navigate('/');
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.5/auth/token/login/', {
        email: email,
        password: password,
      });

      const equip_rent_token = response.data.auth_token;
      console.log('Token:', equip_rent_token);
      document.cookie = `equip_rent_token=${equip_rent_token}; path=/;`;
      
      navigate('/');
    } catch (error) {
      console.error('Error logging in:', error);
      console.log('Authentication failed');
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <br />
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;

// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom'; // Импорт useNavigate из React Router
// import axios from 'axios';

// function Login() {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const navigate = useNavigate(); // Используем useNavigate для перенаправления

//   const handleLogin = async (e) => {
//     e.preventDefault();

//     try {
//       const response = await axios.post('http://127.0.0.5/auth/token/login/', {
//         email: email,
//         password: password,
//       });

//       // Получите токен из ответа и сохраните его в куки
//       const equip_rent_token = response.data.auth_token;
//       console.log('Token:', equip_rent_token); // Вывести токен в консоль
//       document.cookie = `equip_rent_token=${equip_rent_token}; path=/;`;

//       // Перенаправьте пользователя на другую страницу после успешной авторизации
//       // Используйте navigate для перенаправления
//       navigate('/cart'); // Перенаправление в "/cart" после успешной авторизации
//     } catch (error) {
//       console.error('Error logging in:', error);
//       console.log('Authentication failed'); // Вывести сообщение об ошибке в консоль
//     }
//   };

//   return (
//     <div>
//       <h1>Login</h1>
//       <form onSubmit={handleLogin}>
//         <label>
//           Email:
//           <input
//             type="email"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//           />
//         </label>
//         <br />
//         <label>
//           Password:
//           <input
//             type="password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//           />
//         </label>
//         <br />
//         <button type="submit">Login</button>
//       </form>
//     </div>
//   );
// }

// export default Login;
