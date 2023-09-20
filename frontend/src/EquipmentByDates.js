import React, { useState } from 'react';
import cookie from 'react-cookies';

// Компонент для формы выбора дат
function DateSelectionForm({ startDate, endDate, setStartDate, setEndDate, handleSubmit }) {
  return (
    <form onSubmit={handleSubmit}>
      <label>
        Start Date:
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </label>
      <br />
      <label>
        End Date:
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </label>
      <br />
      <button type="submit">Search</button>
    </form>
  );
}

function QuantitySelector({ onQuantityChange }) {
  const [quantity, setQuantity] = useState(1);

  const handleIncrease = () => {
    setQuantity(quantity + 1);
    onQuantityChange(quantity + 1);
  };

  const handleDecrease = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1);
      onQuantityChange(quantity - 1);
    }
  };

  return (
    <div>
      <button onClick={handleDecrease}>-</button>
      <span>{quantity}</span>
      <button onClick={handleIncrease}> + </button>
    </div>
  );
}

function EquipmentByDates() {
  const authToken = cookie.load('equip_rent_token');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [equipmentData, setEquipmentData] = useState(null);
  const [error, setError] = useState(null);
  const [selectedQuantity, setSelectedQuantity] = useState(1);
  const [notification, setNotification] = useState(null);
  const ipAddress = process.env.BACKEND_SERVER_IP || '0.0.0.0';
  const port = process.env.BACKEND_SERVER_PORT || '1337';
  const serverAddress = `http://${ipAddress}:${port}`;

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Проверка на корректность дат
    if (!startDate || !endDate || startDate >= endDate) {
      setError('Check your dates. They are either in the past or the start date is greater than the end date.');
      return;
    }

  try {
    const response = await fetch(`${serverAddress}/api/v1/equipment_dates/?date_end=${endDate}&date_start=${startDate}`);
    if (response.ok) {
      const data = await response.json();
      setEquipmentData(data);
      setError(null);
    } else {
      if (response.status === 400) {
        const errorMessage = await response.text();
        setError(`Bad Request: ${errorMessage}`);
      } else {
        setError('An error occurred while fetching equipment data.');
      }
    }
  } catch (error) {
    console.error('Error fetching equipment data:', error);
    setError('An error occurred while fetching equipment data.');
  }

};
  

  // Функция для обработки клика по кнопке "Add to Cart"
  const handleAddToCartClick = (equipmentItem, selectedQuantity) => {
    if (!authToken) {
      setError('User is not authorized.');
      return;
    }

      const requestData = {
        equipment: equipmentItem.id,
        amount: selectedQuantity,
        date_start: startDate,
        date_end: endDate,
      };

      // Отправка данных на сервер
      fetch(`${serverAddress}/api/v1/add_cart/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${authToken}`,
        },
        body: JSON.stringify(requestData),
      })
        .then((response) => {
          if (response.ok) {
            setNotification('Equipment added to cart successfully.');
            setTimeout(() => {
              setNotification(null);
            }, 3000); // Очистка уведомления через 3 секунды
          } else {
            // Обработка ошибки добавления в корзину
            setError('An error occurred while adding to cart.');
          }
        })
        .catch((error) => {
          console.error('Error adding to cart:', error);
          setError('An error occurred while adding to cart.');
        });
    // }
  };

  return (
    <div>
      <h1>Equipment by Dates</h1>
      <DateSelectionForm
        startDate={startDate}
        endDate={endDate}
        setStartDate={setStartDate}
        setEndDate={setEndDate}
        handleSubmit={handleSubmit}
      />

      {equipmentData && (
        <div>
          <h2>Equipment Results</h2>
          {equipmentData.map((equipmentItem) => (
            <div key={equipmentItem.id}>
              <h3>
                <a href={`/equipment/${equipmentItem.id}`}>{equipmentItem.name}</a>
              </h3>
              <p>Category: {equipmentItem.category}</p>
              <p>Rating: {equipmentItem.rating}</p>
              <p>Description: {equipmentItem.description}</p>
              <p>Price: {equipmentItem.price}</p>
              <p>Amount: {equipmentItem.amount}</p>
              {equipmentItem.photos && equipmentItem.photos.length > 0 && (
                <div>
                  <p>Photos:</p>
                  {equipmentItem.photos.map((photo, index) => (
                    <img
                      key={index}
                      src={`${serverAddress}${photo.photo}`}
                      alt={`Equipment ${equipmentItem.name}`}
                      style={{ maxWidth: '200px', maxHeight: '200px' }}
                    />
                  ))}
                </div>
              )}
              {authToken ? (
                <>
                <QuantitySelector onQuantityChange={setSelectedQuantity} />
                <button onClick={() => handleAddToCartClick(equipmentItem, selectedQuantity)}>
                  Add to Cart
                </button>
                {error && <p>{error}</p>}
                {notification && <p>{notification}</p>}
              </>
              ) : (
                <div>
                  You can add to cart after logging in. <a href="/login">Log in</a>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default EquipmentByDates;
