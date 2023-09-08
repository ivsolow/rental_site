// // AddToCartButton.js

// import React, { useState } from 'react';

// function AddToCartButton({ authToken, equipmentItem, onAddToCart }) {
//   const [selectedAmount, setSelectedAmount] = useState(1);

//   const handleAddToCartClick = () => {
//     // if (!authToken) {
//     //   // Если пользователь не авторизован, вы можете выполнить какие-либо действия, например, перенаправить его на страницу входа.
//     //   console.log('User is not authorized. Redirect to login page.');
//     //   return;
//     // }

//     // Проверка на корректность дат
//     // ...

//     onAddToCart({
//       equipment: equipmentItem.id,
//       amount: selectedAmount,
//       date_start: startDate,
//       date_end: endDate,
//     });
//   };

//   return (
//     <div>
//       <button onClick={handleAddToCartClick}>Add to Cart</button>
//       <input
//         type="number"
//         value={selectedAmount}
//         onChange={(e) => setSelectedAmount(e.target.value)}
//         min="1"
//       />
//     </div>
//   );
// }

// export default AddToCartButton;
