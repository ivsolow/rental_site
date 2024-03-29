import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import './custom_styles.css';
import serverAddress from './config';

function EquipmentDetail() {
  const { id } = useParams();
  const [equipment, setEquipment] = useState({});

  useEffect(() => {
    fetch(`${serverAddress}/api/v1/equipment/${id}`)
      .then(response => response.json())
      .then(data => {
        setEquipment(data);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, [id]);

  // Проверяем, есть ли данные в объекте equipment
  if (!equipment || !equipment.name) {
    return <div>Loading...</div>; // Отобразить сообщение о загрузке данных
  }

  return (
    <div>
      <h1>Equipment Detail</h1>
      <h2>{equipment.name}</h2>
      <p>Category: {equipment.category}</p>
      <p>Price: {equipment.price}</p>
      <p>Amount: {equipment.amount}</p>

      <h3>Photos</h3>
      {equipment.photos.map((photo, index) => (
        <img
          key={index}
          src={`${serverAddress}${photo.photo}`}
          alt={`Equipment Photo ${index + 1}`}
          width="800"
        />
      ))}
      
      <h3>Reviews</h3>
      <p>Total Reviews: {equipment.feedback.length}</p>
<ul className="reviews-list" >
  {equipment.feedback.map(review => (
    <li key={review.id}>
      <div className="review-item">
        {review.feedback_photos.length > 0 && (
          <img
            src={`${serverAddress}${review.feedback_photos[0].photo}`}
            alt={`Photo by ${review.username}`}
            width="200"
          />
        )}
        <div>
          <Link to={`/reviews/${review.id}`}>
            {review.content.split(' ').slice(0, 5).join(' ')}... by {review.username}
          </Link>
        </div>
      </div>
    </li>
  ))}
</ul>

      <Link to="/">Back to Equipment List</Link>
    </div>
  );
}

export default EquipmentDetail;
