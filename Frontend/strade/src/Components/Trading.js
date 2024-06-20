import '../Styles/LoggedIn.css';
import '../Styles/Trading.css';

import React, { useState } from 'react';
import TradingViewWidget from './TradingViewWidget';

const CryptoChart = () => {
  const [crypto, setCrypto] = useState('BTC');
  const [exchange, setExchange] = useState('KUCOIN');
  const [orderType, setOrderType] = useState('market');
  const [amount, setAmount] = useState('');
  const [limitUpper, setLimitUpper] = useState('');
  const [limitLower, setLimitLower] = useState('');

  const handleCryptoChange = (event) => {
    setCrypto(event.target.value);
  };

  const handleExchangeChange = (event) => {
    setExchange(event.target.value);
  };

  const handleOrderTypeChange = (event) => {
    setOrderType(event.target.value);
  };

  const handleAmountChange = (event) => {
    setAmount(event.target.value);
  };

  const handleLimitUpperChange = (event) => {
    setLimitUpper(event.target.value);
  };

  const handleLimitLowerChange = (event) => {
    setLimitLower(event.target.value);
  };

  const handleBuy = () => {
    // Hier würde die Kauflogik implementiert werden
    alert(`Buying ${amount} worth of ${crypto} as a ${orderType} order`);
  };

  const getSymbol = () => `${exchange}:${crypto}USDT`;

  return (
    <div className="crypto-chart-container">
      <div className="left-container">
        <div className="crypto-selector">
          <label htmlFor="crypto">Select Cryptocurrency: </label>
          <select id="crypto" value={crypto} onChange={handleCryptoChange}>
            <option value="BTC">Bitcoin (BTC)</option>
            <option value="ETH">Ethereum (ETH)</option>
            <option value="LTC">Litecoin (LTC)</option>
            <option value="XRP">Ripple (XRP)</option>
            <option value="ADA">Cardano (ADA)</option>
          </select>
        </div>
        <div className="exchange-selector">
          <label htmlFor="exchange">Select Exchange: </label>
          <select id="exchange" value={exchange} onChange={handleExchangeChange}>
            <option value="KUCOIN">KuCoin</option>
            <option value="BINANCE">Binance</option>
            <option value="COINBASE">Coinbase</option>
            <option value="KRAKEN">Kraken</option>
            <option value="BITFINEX">Bitfinex</option>
          </select>
        </div>
        <div className="chart-container">
          <h2>{crypto} Price Chart on {exchange}</h2>
          <TradingViewWidget symbol={getSymbol()} />
        </div>
      </div>
      <div className="right-container">
        <div className="order-form">
          <h2>Buy {crypto}</h2>
          <label htmlFor="orderType">Order Type: </label>
          <select id="orderType" value={orderType} onChange={handleOrderTypeChange}>
            <option value="market">Market</option>
            <option value="limit">Limit</option>
          </select>

          {orderType === 'limit' && (
            <>
              <label htmlFor="limitUpper">Upper Limit: </label>
              <input
                type="number"
                id="limitUpper"
                value={limitUpper}
                onChange={handleLimitUpperChange}
              />

              <label htmlFor="limitLower">Lower Limit: </label>
              <input
                type="number"
                id="limitLower"
                value={limitLower}
                onChange={handleLimitLowerChange}
              />
            </>
          )}

          <label htmlFor="amount">Amount (in USD): </label>
          <input
            type="number"
            id="amount"
            value={amount}
            onChange={handleAmountChange}
          />

          <button onClick={handleBuy}>Buy</button>
        </div>
      </div>
    </div>
  );
};

export default CryptoChart;
