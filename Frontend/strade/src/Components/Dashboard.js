import React, { useState } from 'react';
import '../Styles/LoggedIn.css';
import '../Styles/Dashboard.css';
import useToken from './useToken';
import Chart from './Chart';
import Donut from './DonutChart';
import axios from 'axios';
import KucoinImage from '../Images/Kucoin.png';
import BinanceImage from '../Images/Binance.png';
import BinanceTRImage from '../Images/BinanceTR.png';
import BITFINEX from '../Images/Bitfinex.png';
import BITGET from '../Images/Bitget.png';
import BITSTAMP from '../Images/Bitstamp.png';
import BYBIT from '../Images/Bybit.png';
import COINBASE from '../Images/coinBase.png';
import GATEIO from '../Images/gate.iopng.png';
import GEMINI from '../Images/gemini.png';
import HTX from '../Images/htx.png';
import KRAKEN from '../Images/kraken.png';
import OKX from '../Images/OKX.png';

import { useNavigate } from 'react-router-dom';


async function connectAccount(formData, token) {
  try {
    const response = await axios.post('http://localhost:8001/connect-exchange/', formData, {
      headers: {
        Authorization: `Bearer ${token}` // Token als Header senden
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error connecting to the exchange:', error);
    throw error;
  }
}

async function retrieveData(token){
  try{
    const response = await axios.get('http://localhost:8001/dashboard/',{
      headers: {
        Authorization: `Bearer ${token}` // Token als Header senden
      }
    });

    return response.data;
  }
  catch (error){
    console.error('Error response Data');

    throw error;
  }
}


export default function Dashboard() {
  const navigate = useNavigate();
  const { token } = useToken();

  const [isOpen, setIsOpen] = useState(false);
  const [selection, setSelection] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [formData, setFormData] = useState({
    account_holder: '',
    exchange_name: '',
    key: '',
    secret_key: '',
    passphrase: ''
  });

  const exchanges = [
    { id: 1, name: 'kucoin', imgSrc: KucoinImage},
    { id: 2, name: 'binance', imgSrc: BinanceImage},
    { id: 3, name: 'binanceTR', imgSrc: BinanceTRImage},
    { id: 4, name: 'bitfinex', imgSrc: BITFINEX},
    { id: 5, name: 'bidget', imgSrc: BITGET},
    { id: 6, name: 'bitstamp', imgSrc: BITSTAMP},
    { id: 7, name: 'bybit', imgSrc: BYBIT},
    { id: 8, name: 'coinBase', imgSrc: COINBASE},
    { id: 9, name: 'gate.io', imgSrc: GATEIO},
    { id: 10, name: 'gemini', imgSrc: GEMINI},
    { id: 11, name: 'HTX', imgSrc: HTX},
    { id: 12, name: 'kraken', imgSrc: KRAKEN},
    { id: 13, name: 'OKX', imgSrc: OKX},
  ];

  const toggleContainer = () => {
    setIsOpen(!isOpen);
    setSelection(null);
    setSelectedImage(null);
  };

  const handleSelectionClick = (selection) => {
    setSelection(selection);
  };

  const handleImageClick = (imageId) => {
    const selectedExchange = exchanges.find(exchange => exchange.id === imageId);
    setSelectedImage(imageId);
    setFormData(prevFormData => ({
      ...prevFormData,
     exchange_name: selectedExchange.name
    }));
  };

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData(prevFormData => ({
      ...prevFormData,
      [id]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await connectAccount(formData, token);
      console.log('Account successfully connected');
      navigate('/dashboard');
      window.alert("Exchange connected successfully");
      const account_data = await retrieveData(token);
      console.log("Test", account_data);
      window.alert("retrieve Data successfull");

    } catch (error) {
      window.alert("Exchange connection failed");
      console.error('Error connecting account:', error);
    }
  };

  const chartData = {
    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    series: [30, 40, 35, 50, 49, 60]
  };

  return (
      <div>
        <h2>Dashboard</h2>

        <button className="connect-button" onClick={toggleContainer}>Connect a new account</button>
        {isOpen && (
            <div>
              {!selection ? (
                  <div>
                    <button className="selection-button" onClick={() => handleSelectionClick('Exchange')}>Exchange
                    </button>
                  </div>
              ) : (
                  <div>
                    {selectedImage ? (
                        <div className="editing-container">
                          <form onSubmit={handleSubmit}>
                            <div>
                              <label htmlFor='account_holder'>Name:</label>
                              <input id="account_holder" type="text" value={formData.account_holder}
                                     onChange={handleInputChange}/>
                            </div>
                            <div>
                              <label htmlFor="key">API Key:</label>
                              <input id="key" type="text" value={formData.key} onChange={handleInputChange}/>
                            </div>
                            <div>
                              <label htmlFor="secret_key">API Secret:</label>
                              <input id="secret_key" type="text" value={formData.secret_key}
                                     onChange={handleInputChange}/>
                            </div>
                            <div>
                              <label htmlFor="passphrase">Passphrase:</label>
                              <input id="passphrase" type="text" value={formData.passphrase}
                                     onChange={handleInputChange}/>
                            </div>
                            <button type="submit">Connect
                              to {exchanges.find(exchange => exchange.id === selectedImage)?.name}</button>
                          </form>
                        </div>
                    ) : (
                        <div>
                          {selection === 'Exchange' ? (
                              <div>
                                {exchanges.map(exchange => (
                                    <div key={exchange.id} className="image-container"
                                         onClick={() => handleImageClick(exchange.id)}>
                                      <img src={exchange.imgSrc} alt={exchange.name}/>
                                    </div>
                                ))}
                              </div>
                          ) : (
                              <div></div>
                          )}
                        </div>
                    )}
                  </div>
              )}
            </div>
        )}
        <div className="Account-Data">
          <Donut></Donut>
          <div className="Balance">
            <h4 style={{color: 'black'}}>Current Balance:</h4>
            <h3 className="Money"> {chartData.series[chartData.series.length - 1]}</h3>
          </div>
          <Chart data={chartData}></Chart>
        </div>

        <div className='Specifics'>
          
        </div>

      </div>

  );
}
