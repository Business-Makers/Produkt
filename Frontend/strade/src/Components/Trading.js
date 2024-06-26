import '../Styles/LoggedIn.css';
import '../Styles/Trading.css';

import React, { useState } from 'react';
import TradingViewWidget from './TradingViewWidget';
import useToken from './useToken';
import { useExchanges } from './ExchangeContext';
import axios from 'axios';

const CryptoChart = () => {
  const [selectedCrypto, setSelectedCrypto] = useState('BTC');
  const [selectedExchange, setSelectedExchange] = useState('');
  const [orderType, setOrderType] = useState('market');
  const [amount, setAmount] = useState('');
  const [price, setPrice] = useState('');
  const [stopPrice, setStopPrice] = useState('');
  const [takeProfitPrices, setTakeProfitPrices] = useState([]);
  const [stopLossPrice, setStopLossPrice] = useState('');

  const { exchanges } = useExchanges();
  const token = useToken();

  const handleBuy = async () => {
      let orderData;
      if (orderType.toLowerCase() === 'market') {
          orderData = {
              order_type: orderType.toLowerCase(),
              symbol: selectedCrypto,
              side: selectedExchange,
              amount: parseFloat(amount),
              take_profit_prices: takeProfitPrices.length > 0 ? takeProfitPrices.map(p => parseFloat(p)) : undefined,
              stop_loss_price: stopLossPrice ? parseFloat(stopLossPrice) : undefined
          };
      } else {
      orderData = {
          order_type: orderType.toLowerCase(),
          symbol: selectedCrypto,
          side: selectedExchange,
          amount: parseFloat(amount),
          price: orderType === 'limit' ? parseFloat(price) : undefined,
          stop_price: orderType === 'limit' ? parseFloat(stopPrice) : undefined,
          take_profit_prices: takeProfitPrices.length > 0 ? takeProfitPrices.map(p => parseFloat(p)) : undefined,
          stop_loss_price: stopLossPrice ? parseFloat(stopLossPrice) : undefined
      };
  }

    try {
      const response = await axios.post('http://localhost:8001/trades/create-order/', orderData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log('Order placed successfully', response.data);
    } catch (error) {
          console.log(orderData);
      console.error('Error placing order', error);
    }
  };

  const getSymbol = () => `${selectedExchange}:${selectedCrypto}USDT`;

  return (
    <div className="crypto-chart-container">
      <div className="left-container">
        <div className="crypto-selector">
          <label htmlFor="crypto">Select Cryptocurrency: </label>
          <select id="crypto" value={selectedCrypto} onChange={(e) => setSelectedCrypto(e.target.value)}>
            <option value="BTC">Bitcoin (BTC)</option>
            <option value="ETH">Ethereum (ETH)</option>
            <option value="LTC">Litecoin (LTC)</option>
            <option value="XRP">Ripple (XRP)</option>
            <option value="ADA">Cardano (ADA)</option>
          </select>
        </div>
        <div className="exchange-selector">
          <label htmlFor="exchange">Select Exchange: </label>
          <select id="exchange" value={selectedExchange} onChange={(e) => setSelectedExchange(e.target.value)}>
            {exchanges.length === 0 ? (
              <option value="" disabled>No exchanges connected</option>
            ) : (
              exchanges.map((exchange, index) => (
                <option key={index} value={exchange.exchange_name}>{exchange.exchange_name}</option>
              ))
            )}
          </select>
        </div>
        <div className="chart-container">
          <h2>{selectedCrypto} Price Chart on {selectedExchange}</h2>
          <TradingViewWidget symbol={getSymbol()} />
        </div>
      </div>
      <div className="right-container">
      <div className="order-form">
          <h2>Buy {selectedCrypto}</h2>
          <label htmlFor="order-type">Order Type:</label>
          <select
            id="order-type"
            value={orderType}
            onChange={(e) => setOrderType(e.target.value)}
          >
            <option value="market">Market</option>
            <option value="limit">Limit</option>
          </select>
          <label htmlFor="amount">Amount (USD):</label>
          <input
            type="number"
            id="amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
          {orderType === 'limit' && (
            <>
              <label htmlFor="price">Price:</label>
              <input
                type="number"
                id="price"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
              />
              <label htmlFor="stopPrice">Stop Price:</label>
              <input
                type="number"
                id="stopPrice"
                value={stopPrice}
                onChange={(e) => setStopPrice(e.target.value)}
              />
            </>
          )}
          <label htmlFor="takeProfitPrices">Take Profit Prices (comma separated) (optional):</label>
          <input
            type="text"
            id="takeProfitPrices"
            value={takeProfitPrices}
            onChange={(e) => setTakeProfitPrices(e.target.value.split(','))}
          />
          <label htmlFor="stopLossPrice">Stop Loss Price (optional):</label>
          <input
            type="number"
            id="stopLossPrice"
            value={stopLossPrice}
            onChange={(e) => setStopLossPrice(e.target.value)}
          />
          <button type="button" onClick={handleBuy}>Buy</button>
        </div>
      </div>
    </div>
  );
};

export default CryptoChart;
