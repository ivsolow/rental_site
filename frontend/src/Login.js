import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import cookie from 'react-cookies';
import axios from 'axios';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const authToken = cookie.load('equip_rent_token');
    console.log(authToken)
    
    if (authToken) {
      navigate('/');
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://0.0.0.0:1337/auth/token/login/', {
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
