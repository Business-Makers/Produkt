import React, { useState } from 'react';
import '../Styles/LoggedIn.css';
import '../Styles/Dashboard.css';
import useToken from './useToken';
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

export default function Dashboard() {
  const navigate = useNavigate();
  const { token} = useToken();

  const [isOpen, setIsOpen] = useState(false);
  const [selection, setSelection] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [formData, setFormData] = useState({
    api_name: '',
    exchange_id: 'kucoin',
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
     exchange_id: selectedExchange.name
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
    } catch (error) {
      window.alert("Exchange connection failed");
      console.error('Error connecting account:', error);
    }
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <button className="connect-button" onClick={toggleContainer}>Connect a new account</button>
      {isOpen && (
        <div>
          {!selection ? (
            <div>
              <button className="selection-button" onClick={() => handleSelectionClick('Exchange')}>Exchange</button>
            </div>
          ) : (
            <div>
              {selectedImage ? (
                <div className="editing-container">
                  <form onSubmit={handleSubmit}>
                    <div>
                      <label htmlFor='api_name'>Name:</label>
                      <input id="api_name" type="text" value={formData.api_name} onChange={handleInputChange} />
                    </div>
                    <div>
                      <label htmlFor="key">API Key:</label>
                      <input id="key" type="text" value={formData.key} onChange={handleInputChange} />
                    </div>
                    <div>
                      <label htmlFor="secret_key">API Secret:</label>
                      <input id="secret_key" type="text" value={formData.secret_key} onChange={handleInputChange} />
                    </div>
                    <div>
                      <label htmlFor="passphrase">Passphrase:</label>
                      <input id="passphrase" type="text" value={formData.passphrase} onChange={handleInputChange} />
                    </div>
                    <button type="submit">Connect to {exchanges.find(exchange => exchange.id === selectedImage)?.name}</button>
                  </form>
                </div>
              ) : (
                <div>
                  {selection === 'Exchange' ? (
                    <div>
                      {exchanges.map(exchange => (
                        <div key={exchange.id} className="image-container" onClick={() => handleImageClick(exchange.id)}>
                          <img src={exchange.imgSrc} alt={exchange.name} />
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div>
                      {/*
                      <div className="image-container" onClick={() => handleImageClick(4)}>
                        <img src="path/to/wallet1.jpg" alt="Wallet Bild 1" />
                        <p>Wallet selection option 1</p>
                      </div>
                      <div className="image-container" onClick={() => handleImageClick(5)}>
                        <img src="path/to/wallet2.jpg" alt="Wallet Bild 2" />
                        <p>Wallet selection option 2</p>
                      </div>
                      <div className="image-container" onClick={() => handleImageClick(6)}>
                        <img src="path/to/wallet3.jpg" alt="Wallet Bild 3" />
                        <p>Wallet selection option 3</p>
                      </div>
                      */}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
