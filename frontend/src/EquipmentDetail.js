import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import './custom_styles.css';

function EquipmentDetail() {
  const { id } = useParams();
  const [equipment, setEquipment] = useState({});

  useEffect(() => {
    fetch(`http://127.0.0.5/api/v1/equipment/${id}`)
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
      
      <h3>Reviews</h3>
      <p>Total Reviews: {equipment.feedback.length}</p>
<ul className="reviews-list" >
  {equipment.feedback.map(review => (
    <li key={review.id}>
      <div className="review-item">
        {review.feedback_photos.length > 0 && (
          <img
            src={`http://127.0.0.5${review.feedback_photos[0].photo}`}
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


// import React, { useEffect, useState } from 'react';
// import { Link, useParams } from 'react-router-dom';

// function EquipmentDetail() {
//   const { id } = useParams();
//   const [equipment, setEquipment] = useState({});

//   useEffect(() => {
//     // Выводим значение id в консоль для проверки
//     console.log('ID:', id);

//     fetch(`http://127.0.0.5/api/v1/equipment/${id}`)
//       .then(response => response.json())
//       .then(data => {
//         // Выводим полученные данные в консоль для отладки
//         console.log('Fetched Data:', data);
//         setEquipment(data);
//       })
//       .catch(error => console.error('Error fetching data:', error));
//   }, [id]);

//   // Выводим текущее состояние equipment в консоль для отладки
//   console.log('Equipment State:', equipment);

//   // Проверяем, есть ли данные в объекте equipment
//   if (!equipment || !equipment.name) {
//     return <div>Loading...</div>; // Отобразить сообщение о загрузке данных
//   }

//   return (
//     <div>
//       <h1>Equipment Detail</h1>
//       <h2>{equipment.name}</h2>
//       <p>Category: {equipment.category}</p>
//       <p>Price: {equipment.price}</p>
//       <p>Amount: {equipment.amount}</p>
//       <Link to="/">Back to Equipment List</Link>
//     </div>
//   );
// }

// export default EquipmentDetail;



//
// import React, { useEffect, useState } from 'react';
// import { Link, useParams } from 'react-router-dom';

// function EquipmentDetail() {
//   // Используем хук useParams для доступа к параметрам маршрута
//   const { id } = useParams();
//   // Создаем состояние для хранения данных о снаряжении
//   const [equipment, setEquipment] = useState({});

//   useEffect(() => {
//     // В этой функции можно выполнить запрос к серверу
//     // для получения данных о снаряжении с указанным id.
//     // Для этого можно использовать fetch или другие методы.
//     // Здесь предполагается, что данные о снаряжении
//     // будут получены и обновят состояние equipment.
//     // Пример запроса:
//     fetch(`http://127.0.0.5/api/v1/equipment/${id}`)
//       .then(response => response.json())
//       .then(data => {
//         setEquipment(data);
//       })
//       .catch(error => console.error('Error fetching data:', error));
//   }, [id]);

//   return (
//     <div>
//       <h1>Equipment Detail</h1>
//       <h2>{equipment.name}</h2>
//       <p>Category: {equipment.category}</p>
//       <p>Price: {equipment.price}</p>
//       <p>Amount: {equipment.amount}</p>
//       <Link to="/">Back to Equipment List</Link>
//     </div>
//   );
// }

// export default EquipmentDetail;

//
// import React, { Component } from 'react';
// import { withRouter } from 'react-router-dom';

// class EquipmentDetail extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       equipment: {}, // Данные о снаряжении
//     };
//   }

//   componentDidMount() {
//     const equipmentId = this.props.match.params.id;

//     // Загрузка данных с API и обновление состояния
//     fetch(`http://127.0.0.5/api/v1/equipment/${equipmentId}`)
//       .then(response => response.json())
//       .then(data => {
//         this.setState({ equipment: data });
//       })
//       .catch(error => console.error('Error fetching data:', error));
//   }

//   render() {
//     const { equipment } = this.state;

//     return (
//       <div>
//         <h1>Equipment Detail</h1>
//         <h2>{equipment.name}</h2>
//         <p>Category: {equipment.category}</p>
//         <p>Price: {equipment.price}</p>
//         <p>Amount: {equipment.amount}</p>
//       </div>
//     );
//   }
// }

// export default withRouter(EquipmentDetail);