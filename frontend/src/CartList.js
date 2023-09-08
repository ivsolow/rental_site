
import React, { useEffect, useState } from 'react';
import cookie from 'react-cookies'; // Импортируем библиотеку для работы с куками
import { Link, useNavigate } from 'react-router-dom';


function Cart() {
  const [cartData, setCartData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    // Получаем токен из куки
    const authToken = cookie.load('equip_rent_token');

    if (!authToken) {
      // Если токен отсутствует, устанавливаем сообщение об ошибке
      setErrorMessage('Please log in to access this resource');
      return;
    }

    // Выполнить GET-запрос к эндпоинту корзины пользователя с использованием токена из куки
    fetch('http://127.0.0.5/api/v1/cart', {
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


// import React, { useEffect, useState } from 'react';
// import cookie from 'react-cookies'; // Импортируем библиотеку для работы с куками

// function Cart() {
//   const [cartData, setCartData] = useState(null);
//   const [errorMessage, setErrorMessage] = useState(null);

//   useEffect(() => {
//     // Получаем токен из куки
//     const authToken = cookie.load('equip_rent_token');

//     if (!authToken) {
//       // Если токен отсутствует, устанавливаем сообщение об ошибке
//       setErrorMessage('Please log in to access this resource');
//       return;
//     }

//     // Выполнить GET-запрос к эндпоинту корзины пользователя с использованием токена из куки
//     fetch('http://127.0.0.5/api/v1/cart', {
//       method: 'GET',
//       headers: {
//         Authorization: `Token ${authToken}`, // Используем токен из куки
//       },
//     })
//       .then(response => {
//         if (response.status === 401) {
//           // Если сервер вернул ошибку 401, устанавливаем сообщение об ошибке
//           setErrorMessage('You are not authorized. Please log in to access this resource. <Link to="/login">Log in</Link>');
//           return;
//         }
//         return response.json();
//       })
//       .then(data => {
//         if (data) {
//           setCartData(data);
//         }
//       })
//       .catch(error => {
//         console.error('Error fetching cart data:', error);
//       });
//   }, []);

//   if (errorMessage) {
//     return <div>{errorMessage}</div>; // Отобразить сообщение об ошибке
//   }

//   if (!cartData) {
//     return <div>Loading...</div>; // Отобразить сообщение о загрузке данных
//   }

//   return (
//     <div>
//       <h1>Cart Contents</h1>
//       {/* Ваш код для отображения корзины */}
//     </div>
//   );
// }

// export default Cart;




// import React, { useEffect, useState } from 'react';
// import cookie from 'react-cookies'; // Импортируем библиотеку для работы с куками
// // import { useNavigate } from 'react-router-dom';

// function Cart() {
//   const [cartData, setCartData] = useState(null);

//   useEffect(() => {
//     // Получаем токен из куки
//     // const navigate = useNavigate();
//     const authToken = cookie.load('equip_rent_token');
  
//     if (!authToken) {
//       // Если токен отсутствует, вы можете предпринять какие-либо действия, например, перенаправить пользователя на страницу входа.
//       // В данном примере просто выведем сообщение об ошибке.
//       console.error('Authorization token not found in cookie.');
//       return;
//     }
  
//     // Выполнить GET-запрос к эндпоинту корзины пользователя с использованием токена из куки
//     fetch('http://127.0.0.5/api/v1/cart', {
//       method: 'GET',
//       headers: {
//         Authorization: `Token ${authToken}`, // Используем токен из куки
//       },
//     })
//       .then(response => {
//         if (response.status === 401) {
//           // Если сервер вернул ошибку 401, перенаправляем пользователя на страницу входа
//         //   navigate('/login');
//           return <div>Пожалуйста, авторизуйтесь</div>;;
//         }
//         return response.json();
//       })
//       .then(data => {
//         if (data) {
//           setCartData(data);
//         }
//       })
//       .catch(error => {
//         console.error('Error fetching cart data:', error);
//       });
//   }, []);

//   if (!cartData) {
//     return <div>Loading...</div>; // Отобразить сообщение о загрузке данных
//   }

//   return (
//  <div>
//   <h1>Cart Contents</h1>
//   {cartData ? (
//     <div>
//       <p>Total Positions: {cartData.total_positions}</p>
//       <p>Total Sum: {cartData.total_summ}</p>

//       <h2>Cart Items</h2>
//       {cartData.cart_item_data && cartData.cart_item_data.length > 0 ? (
//         <ul>
//           {cartData.cart_item_data.map(cartItem => (
//             <li key={cartItem.cart_id}>
//               <h3>{cartItem.equipment.name}</h3>
//               <p>Price: {cartItem.equipment.price}</p>
//               <p>Amount: {cartItem.amount}</p>
//               <p>Sum: {cartItem.summ}</p>
//               <p>Start Date: {cartItem.dates.date_start}</p>
//               <p>End Date: {cartItem.dates.date_end}</p>
//             </li>
//           ))}
//         </ul>
//       ) : (
//         <p>Your cart is empty.</p>
//       )}
//     </div>
//   ) : (
//     <div>Loading...</div>
//   )}
// </div>
//   );
// }

// export default Cart;



// import React, { useEffect, useState } from 'react';

// function Cart() {
//   const [cartData, setCartData] = useState(null);

//   useEffect(() => {
//     // Выполнить GET-запрос к эндпоинту корзины пользователя
//     fetch('http://127.0.0.5/api/v1/cart', {
//       method: 'GET',
//       headers: {
//         Authorization: 'Token acd2b4ff08949dc82e8548e7841b859791211b35', // Замените на ваш токен авторизации
//       },
//     })
//       .then(response => response.json())
//       .then(data => {
//         setCartData(data);
//       })
//       .catch(error => console.error('Error fetching cart data:', error));
//   }, []);

//   if (!cartData) {
//     return <div>Loading...</div>; // Отобразить сообщение о загрузке данных
//   }

//   return (
//     <div>
//       <h1>Cart Contents</h1>
//       <p>Total Positions: {cartData.total_positions}</p>
//       <p>Total Sum: {cartData.total_summ}</p>

//       <h2>Cart Items</h2>
//       <ul>
//         {cartData.cart_item_data.map(cartItem => (
//           <li key={cartItem.cart_id}>
//             <h3>{cartItem.equipment.name}</h3>
//             <p>Price: {cartItem.equipment.price}</p>
//             <p>Amount: {cartItem.amount}</p>
//             <p>Sum: {cartItem.summ}</p>
//             <p>Start Date: {cartItem.dates.date_start}</p>
//             <p>End Date: {cartItem.dates.date_end}</p>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default Cart;
