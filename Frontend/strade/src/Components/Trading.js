import '../Styles/LoggedIn.css';
import '../Styles/Trading.css';

import React, { useState, useEffect } from 'react';
import TradingViewWidget from './TradingViewWidget';
import useToken from './useToken';
import { useExchanges } from './ExchangeContext';
import axios from 'axios';
import mockTrades from './mockTrades';

const getTradeHistory = async (token) => {
  try {
    const response = await axios.get('http://localhost:8001/trades/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.trades_data;
  } catch (error) {
    console.error('Error fetching trade history:', error);
  }
}

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
  const { token } = useToken();

  const [ trades, setTrades ] = useState([]);

  useEffect(() => {
  if (token) {
    const fetchData = async () => {
      try {
        const tradeData = await getTradeHistory(token);
        setTrades(tradeData);
        console.log(trades);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }
}, [token]);

useEffect(() => {
    console.log("Exchanges", exchanges);
  if (exchanges && exchanges.length > 0 && !selectedExchange) {
    setSelectedExchange(exchanges[0].exchange_name);
  }
}, [exchanges]);

  const handleBuy = async () => {
      let orderData;
      if (orderType.toLowerCase() === 'market') {
          orderData = {
              order_type: orderType.toLowerCase(),
              trade_price: 0.0,
              symbol: selectedCrypto,
              side: selectedExchange,
              amount: parseFloat(amount),
              take_profit_prices: takeProfitPrices.length > 0 ? takeProfitPrices.map(p => parseFloat(p)) : 0,
              stop_loss_price: stopLossPrice ? parseFloat(stopLossPrice) : 0
          };
      } else {
      orderData = {
          order_type: orderType.toLowerCase(),
          trade_price: 0.0,
          symbol: selectedCrypto,
          side: selectedExchange,
          amount: parseFloat(amount),
          price: orderType === 'limit' ? parseFloat(price) : 0,
          stop_price: orderType === 'limit' ? parseFloat(stopPrice) : 0,
          take_profit_prices: takeProfitPrices.length > 0 ? takeProfitPrices.map(p => parseFloat(p)) : 0,
          stop_loss_price: stopLossPrice ? parseFloat(stopLossPrice) : 0
      };
  }

    try {
          console.log(orderData);
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
    <div>
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
    <div className="trade-history-container">
      <h2>Trade History</h2>
      {trades && trades.length > 0 ? (
          <div className="trade-history">
              {trades.map((trade, index) => (
                  <div key={index} className="trade-item">
                      <div className="trade-left">
                          <p><strong>Currency:</strong> {trade.currency_name}</p>
                          <p><strong>Account Holder:</strong> {trade.account_Holder}</p>
                      </div>
                      <div className="trade-middle">
                          <p><strong>Trade Date:</strong> {trade.date_create}</p>
                          <p><strong>Trade ID:</strong> {trade.trade_id}</p>
                      </div>
                      <div className="trade-right">
                          <p><strong>Volume:</strong> {trade.currency_volume}</p>
                          <p><strong>Purchase Price:</strong> {trade.purchase_rate}</p>
                      </div>
                      <div className="trade-chart">
                      </div>
                  </div>
              ))}
        </div>
      ) : (
          <p>No trades available.</p>
      )}
    </div>
    </div>
  );
};

export default CryptoChart;