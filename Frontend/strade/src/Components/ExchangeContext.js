import React, { createContext, useContext, useState } from 'react';

const ExchangeContext = createContext();

export const useExchanges = () => {
  return useContext(ExchangeContext);
};

export const ExchangeProvider = ({ children }) => {
  const [exchanges, setExchanges] = useState([]);

  return (
    <ExchangeContext.Provider value={{ exchanges, setExchanges }}>
      {children}
    </ExchangeContext.Provider>
  );
};