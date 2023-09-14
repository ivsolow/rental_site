import React, { useEffect, useState } from 'react';
import cookie from 'react-cookies';

function AuthChecker({ children, onAuthorized, onUnAuthorized }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const authToken = cookie.load('equip_rent_token');

    if (authToken) {
      setIsAuthenticated(true);
      onAuthorized(); // Вызываем колбэк при успешной авторизации
    } else {
      setIsAuthenticated(false);
      onUnAuthorized(); // Вызываем колбэк, если пользователь не авторизован
    }
  }, []);

  return isAuthenticated ? children : null;
}

export default AuthChecker;
