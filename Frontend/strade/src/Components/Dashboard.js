import React, { useState } from 'react';
import '../Styles/LoggedIn.css';
import '../Styles/Dashboard.css';
import axios from 'axios';
import KucoinImage from '../Images/Kucoin.png';
import BinanceImage from '../Images/Binance.png';
import BinanceTRImage from '../Images/BinanceTR.png';
import { useNavigate } from 'react-router-dom';

async function connectAccount(formData) {
  try {
    await axios.post('http://localhost:8001/connect-exchange/', formData);
  } catch (error) {
    console.error('Error connecting Exchange:', error);
    throw error;
  }
}

export default function Dashboard() {
  const navigate = useNavigate();

  const [isOpen, setIsOpen] = useState(false);
  const [selection, setSelection] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    apiKey: '',
    apiSecret: '',
    passphrase: ''
  });

  const exchanges = [
    { id: 1, name: 'kucoin', imgSrc: KucoinImage, otherData: 'Additional info 1' },
    { id: 2, name: 'binance', imgSrc: BinanceImage, otherData: 'Additional info 2' },
    { id: 3, name: 'binanceTR', imgSrc: BinanceTRImage, otherData: 'Additional info 3' },
    { id: 4, name: 'bitfinex', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 5, name: 'bidget', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 6, name: 'bitstamp', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 7, name: 'bybit', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 8, name: 'coinBase', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 9, name: 'gate.io', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 10, name: 'gemini', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 11, name: 'hTX', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 12, name: 'kraken', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
    { id: 13, name: 'oKX', imgSrc: 'path/to/exchange4.jpg', otherData: 'Additional info 4' },
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
      name: selectedExchange.name
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
      await connectAccount(formData);
      console.log('Account connected successfully');
      navigate('/dashboard');
      window.alert("Exchange Connect successful");
    } catch (error) {
      window.alert("Exchange Connect failed");
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
                      <label htmlFor="name">Name:</label>
                      <input id="name" type="text" value={formData.name} onChange={handleInputChange} />
                    </div>
                    <div>
                      <label htmlFor="apiKey">API Key:</label>
                      <input id="apiKey" type="text" value={formData.apiKey} onChange={handleInputChange} />
                    </div>
                    <div>
                      <label htmlFor="apiSecret">API Secret:</label>
                      <input id="apiSecret" type="text" value={formData.apiSecret} onChange={handleInputChange} />
                    </div>
                    <div>
                      <label htmlFor="passphrase">Passphrase:</label>
                      <input id="passphrase" type="text" value={formData.passphrase} onChange={handleInputChange} />
                    </div>
                    <button type="submit">Connect {exchanges.find(exchange => exchange.id === selectedImage)?.name}</button>
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
                        <p>Wallet Auswahlmöglichkeit 1</p>
                      </div>
                      <div className="image-container" onClick={() => handleImageClick(5)}>
                        <img src="path/to/wallet2.jpg" alt="Wallet Bild 2" />
                        <p>Wallet Auswahlmöglichkeit 2</p>
                      </div>
                      <div className="image-container" onClick={() => handleImageClick(6)}>
                        <img src="path/to/wallet3.jpg" alt="Wallet Bild 3" />
                        <p>Wallet Auswahlmöglichkeit 3</p>
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
