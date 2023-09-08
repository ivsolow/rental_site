import React from 'react';
import { Link, NavLink } from 'react-router-dom';

function Home() {
  return (
    <div>
      <h1>Welcome to Our Website</h1>
      <nav>
        <ul>
          <li>
            <NavLink to="/" exact activeClassName="active">
              Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/cart" activeClassName="active">
              Cart
            </NavLink>
          </li>
          <li>
            <NavLink to="/equipment" activeClassName="active">
              all equipment
            </NavLink>
          </li>
          <li>
            <NavLink to="/equipment-dates" activeClassName="active">
              Equipment, available in some dates
            </NavLink>
          </li>
          <li>
            <NavLink to="/login" activeClassName="active">
              Login
            </NavLink>
          </li>
          <li>
            <NavLink to="/logout" activeClassName="active">
              Logout
            </NavLink>
          </li>
        </ul>
      </nav>
      <hr />

      {/* Дополнительный контент главной страницы */} 
      <p>
        Добро пожаловать на наш веб-сайт. Здесь вы можете найти различное снаряжение для аренды.
        Пожалуйста, используйте навигацию выше, чтобы перейти на нужные страницы.
      </p>
    </div>
  );
}

export default Home;
