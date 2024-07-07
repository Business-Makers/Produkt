import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from "axios";
import useToken from "./useToken";

const ExchangeContext = createContext();


export const ExchangeProvider = ({ children }) => {
  const [exchanges, setExchanges] = useState([]);
  const { token } = useToken();

  useEffect(() => {
    const fetchExchanges = async () => {
      try {
        const response = await axios.get('http://localhost:8001/dashboard/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setExchanges(response.data.dashboard);
      } catch (error) {
        console.error('Error fetching exchanges:', error);
      }
    };

    fetchExchanges();
  }, [token]);

  return (
    <ExchangeContext.Provider value={{ exchanges }}>
      {children}
    </ExchangeContext.Provider>
  );
};

export const useExchanges = () => {
  return useContext(ExchangeContext);
};