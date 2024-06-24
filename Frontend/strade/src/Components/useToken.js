import { useState } from 'react';

/**Activates the token and puts it into a session storage, meaning that it will remain active until closing of the tab. */
export default function useToken() {
  const getToken = () => {
    return sessionStorage.getItem('access_token');
  };

  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    sessionStorage.setItem('access_token', userToken);
    setToken(userToken);
  };

  return {
    setToken: saveToken,
    token
  }
}