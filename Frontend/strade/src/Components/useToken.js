import { useState } from 'react';

/**Activates the token and puts it into a session storage, meaning that it will remain active until closing of the tab. */
export default function useToken() {
  const getToken = () => {
    const tokenString = sessionStorage.getItem('login_status');
    return tokenString;
  };

  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    sessionStorage.setItem('login_status', userToken); // TODO: Das hier hängt auch mit der schlechten Tokenerstellung aus LogIn zusammen
    setToken(userToken);
  };

  return {
    setToken: saveToken,
    token
  }
}

/*
export default function useToken() {
  const getToken = () => {
    const tokenString = sessionStorage.getItem('token');
    if (!tokenString) {
      return null;
    }
    try {
      const userToken = JSON.parse(tokenString);
      return userToken?.token || null;
    } catch (e) {
      console.error("Error parsing token from localStorage", e);
      return null;
    }
  };

  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    sessionStorage.setItem('token', JSON.stringify(userToken));
    setToken(userToken.token);
  };

  return {
    setToken: saveToken,
    token
  }
}*/