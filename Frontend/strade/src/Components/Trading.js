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
    const response = await axios.get('http://51.20.249.18:8001/trades/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    //console.log(response.data); // Falls nicht klappt, noch .trades_data anhaengen
    return response.data.trades;
  } catch (error) {
    console.error('Error fetching trade history:', error);
  }
}

const handleSell = async (trade_id, token) => {
  try {
    const response = await axios.post('http://51.20.249.18:8001/complete_trade/', { trade_id }, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 200) {
      alert('Trade completed successfully');
      window.location.reload();
    } else {
      alert('Failed to complete trade');
    }
  } catch (error) {
    console.error('There was an error completing the trade:', error);
    alert('Error completing trade');
  }
};

const fetchCurrentPrice = async (symbol) => {
  try {
    const response = await axios.get(`https://api.coingecko.com/api/v3/simple/price?ids=${symbol}&vs_currencies=usd`);
    return response.data[symbol].usd;
  } catch (error) {
    console.error('Error fetching current price:', error);
    return 0.0;
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
  const [currentPrice, setCurrentPrice] = useState(0.0);

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

useEffect(() => {
    const fetchPrice = async () => {
      const price = await fetchCurrentPrice(selectedCrypto);
      setCurrentPrice(price);
    };
    fetchPrice();
  }, [selectedCrypto]);

  const handleBuy = async () => {
      let orderData;
      if (orderType.toLowerCase() === 'market') {
          orderData = {
              trade_price: currentPrice,
              side: 'buy',
              symbol: selectedCrypto + "/USDT",
              exchangeName: selectedExchange,
              amount: parseFloat(amount),
              price: 0,
              stop_price: 0,
              order_type: orderType.toLowerCase(),
              take_profit_prices: takeProfitPrices.length > 0 ? takeProfitPrices.map(p => parseFloat(p)) : [],
              stop_loss_price: stopLossPrice ? parseFloat(stopLossPrice) : undefined,
              comment: ''
          };
      } else {
      orderData = {
          trade_price: currentPrice,
          side: 'buy',
          symbol: selectedCrypto + "/USDT",
          exchangeName: selectedExchange,
          amount: parseFloat(amount),
          price: orderType === 'limit' ? parseFloat(price) : undefined,
          stop_price: orderType === 'limit' ? parseFloat(stopPrice) : undefined,
          order_type: orderType.toLowerCase(),
          take_profit_prices: takeProfitPrices.length > 0 ? takeProfitPrices.map(p => parseFloat(p)) : [],
          stop_loss_price: stopLossPrice ? parseFloat(stopLossPrice) : undefined,
          comment: ''
      };
  }

    try {
          console.log(orderData);
      const response = await axios.post('http://51.20.249.18:8001/trades/create-order/', orderData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.status === 200) {
          console.log('Order placed successfully', response.data);
          alert("Trade created successfully");
          window.location.reload();
      }
      else {
          alert("Something went wrong creating your trade");
      }
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
              value={takeProfitPrices.join(',')} // Zusammenführen des Arrays zu einem String für die Anzeige
              onChange={(e) => setTakeProfitPrices(e.target.value.split(',').map(p => parseFloat(p)))}
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
                                <p><strong>Account Holder:</strong> {trade.account_holder}</p>
                            </div>
                            <div className="trade-middle">
                                <p><strong>Trade Date:</strong> {trade.date_create}</p>
                                <p><strong>Trade ID:</strong> {trade.trade_id}</p>
                            </div>
                            <div className="trade-right">
                                <p><strong>Volume:</strong> {trade.currency_volume}</p>
                                <p><strong>Purchase Rate:</strong> {trade.purchase_rate}</p>
                                {(trade.trade_type === 'market' && !trade.date_sale) ? (
                                    <button onClick={() => handleSell(trade.trade_id, token)}>Sell</button>
                                ) : (
                                    <p><strong>Selling Rate:</strong> {trade.selling_rate}</p>
                                )}
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