import '../Styles/LoggedIn.css';
import '../Styles/Trading.css';

import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  TimeScale
} from 'chart.js';
import 'chartjs-adapter-date-fns';

// Registriere die notwendigen Komponenten
ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  TimeScale
);

const CryptoChart = () => {
  const [chartData, setChartData] = useState({
    datasets: [
      {
        label: 'Cryptocurrency Price',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        segment: {
          borderColor: ctx => ctx.p0.parsed.y < ctx.p1.parsed.y ? 'green' : 'red',
        },
        pointRadius: 0,
      },
    ],
  });

  const [crypto, setCrypto] = useState('bitcoin');
  const [purchaseAmount, setPurchaseAmount] = useState('');
  const [purchaseStatus, setPurchaseStatus] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await axios.get(`https://api.coingecko.com/api/v3/coins/${crypto}/market_chart`, {
          params: {
            vs_currency: 'usd',
            days: '30',
          },
        });

        if (result.data && result.data.prices) {
          const prices = result.data.prices.map(price => ({
            x: new Date(price[0]),
            y: price[1],
            formattedY: `$${price[1].toFixed(2)}`,
          }));

          setChartData({
            datasets: [
              {
                label: `${crypto.charAt(0).toUpperCase() + crypto.slice(1)} Price`,
                data: prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                segment: {
                  borderColor: ctx => ctx.p0.parsed.y < ctx.p1.parsed.y ? 'green' : 'red',
                },
                pointRadius: 0,
              },
            ],
          });
        } else {
          console.error("Unexpected response format", result.data);
        }
      } catch (error) {
        console.error("Error fetching data", error);
      }
    };

    fetchData();
  }, [crypto]);

  const handleCryptoChange = (event) => {
    setCrypto(event.target.value);
  };

  const handlePurchase = async () => {
    try {
      const response = await axios.post('http://example.com/api/purchase', { //TODO: Hier muss die richtige Adresse vom Server hin
        crypto,
        amount: parseFloat(purchaseAmount),
      });

      console.log('Purchase response:', response.data);
      setPurchaseStatus('Purchase successful!');
    } catch (error) {
      console.error('Error purchasing:', error);
      setPurchaseStatus('Error purchasing, please try again.');
    }
  };

  const handleAmountChange = (event) => {
    setPurchaseAmount(event.target.value);
  };

  console.log('chartData:', chartData);

  return (
    <div className="crypto-chart-container">
      <div className="chart-content">
        <div className="crypto-selector">
          <label htmlFor="crypto">Select Cryptocurrency: </label>
          <select id="crypto" value={crypto} onChange={handleCryptoChange}>
            <option value="bitcoin">Bitcoin</option>
            <option value="ethereum">Ethereum</option>
            <option value="litecoin">Litecoin</option>
            <option value="ripple">Ripple</option>
            <option value="cardano">Cardano</option>
          </select>
        </div>
        <div className="chart-container">
          <h2>{crypto.charAt(0).toUpperCase() + crypto.slice(1)} Price Chart</h2>
          <Line
            data={chartData}
            options={{
              scales: {
                x: {
                  type: 'time',
                  time: {
                    unit: 'day',
                  },
                },
              },
            }}
          />
        </div>
        <div className="purchase-container">
          <div className="purchase-form">
            <input
              type="number"
              value={purchaseAmount}
              onChange={handleAmountChange}
              placeholder="Enter amount to purchase"
            />
            <button onClick={handlePurchase}>Purchase</button>
            {purchaseStatus && <p>{purchaseStatus}</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CryptoChart;
