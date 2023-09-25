import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import serverAddress from './config';

class EquipmentList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      equipmentList: [], // Список снаряжения
    };
  }

  componentDidMount() {
    fetch(`${serverAddress}/api/v1/equipment/`)
      .then(response => response.json())
      .then(data => {
        this.setState({ equipmentList: data });
      })
      .catch(error => console.error('Error fetching data:', error));
  }

  render() {
    const { equipmentList } = this.state;

    return (
      <div>
        <h1>Equipment List</h1>
        <ul>
          {equipmentList.map(item => (
            <li key={item.id}>
              <h2>{item.name}</h2>
              <p>Price: {item.price}</p>
              <p>Rating: {item.rating || '-'}</p>
              {item.photos.map((photo, index) => (
                <Link key={index} to={`/equipment/${item.id}`}>
                  <img src={`${serverAddress}${photo.photo}`} alt={`Equipment ${item.id} - ${index}`} width='500' />
                </Link>
              ))}
            </li>
          ))}
        </ul>
      </div>
    );
  }
}

export default EquipmentList;
