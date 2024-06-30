import React, { useState } from 'react';
import axios from 'axios';
import '../Styles/LoggedIn.css';
import '../Styles/Subscription.css';
import { useToken } from './useToken'; // Stellen Sie sicher, dass der richtige Pfad zum useToken Hook verwendet wird

const Subscription = () => {
  const { token } = useToken(); // Verwenden Sie den useToken Hook, um den Token abzurufen
  const [activeTab, setActiveTab] = useState('Yearly');

  const buttonText = {
    Yearly: {
      basic: '99$ / Year',
      silver: '199$ / Year',
      gold: '299$ / Year'
    },
    Monthly: {
      basic: '8$ / Month',
      silver: '15$ / Month',
      gold: '20$ / Month'
    }
  };

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  const connectWithServer = async (membership, periodInDays) => {
    const url = 'http://localhost:8001/payment';
    const formData = {
      currency: 'USD',
      product_name: membership,
      product_days: periodInDays
    };

    try {
      const response = await axios.post(url, formData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log('Response from server:', response.data);
      alert(`Successfully purchased ${membership} for ${periodInDays} days!`);
    } catch (error) {
      console.error('Error purchasing membership:', error);
      alert('Error purchasing membership. Please try again later.');
    }
  };

  const handlePriceButtonClick = (membership, periodInDays) => {
    const confirmed = window.confirm(`Do you want to purchase ${membership} for ${periodInDays} days?`);
    if (confirmed) {
      connectWithServer(membership, periodInDays);
    }
  };

  return (
    <div className="subscription-wrapper">
      <div className="tabs">
        <div className={`tab ${activeTab === 'Yearly' ? 'active' : ''}`} onClick={() => handleTabClick('Yearly')}>
          Yearly
        </div>
        <div className={`tab ${activeTab === 'Monthly' ? 'active' : ''}`} onClick={() => handleTabClick('Monthly')}>
          Monthly
        </div>
      </div>
      <div className="subscriptions-container">
        <div className="subscription basic">
          <h2>Basic Membership</h2>
          <ul>
            <li>One Trade</li>
            <li>Access to 1 Portfolio</li>
            <li>Default Usage of $Comms</li>
          </ul>
          <button className="sbmt-button" onClick={() => handlePriceButtonClick('Basic', activeTab === 'Yearly' ? 365 : 30)}>
            {buttonText[activeTab].basic}
          </button>
        </div>
        <div className="subscription silver">
          <h2>Silver Membership</h2>
          <ul>
            <li>Up to 25 Trades</li>
            <li>Access to 4 different Portfolios</li>
            <li>Default Usage of $Comms</li>
          </ul>
          <button className="sbmt-button" onClick={() => handlePriceButtonClick('Silver', activeTab === 'Yearly' ? 365 : 30)}>
            {buttonText[activeTab].silver}
          </button>
        </div>
        <div className="subscription gold">
          <h2>Gold Membership</h2>
          <ul>
            <li>Up to 100 Trades</li>
            <li>Access to 10 different Portfolios</li>
            <li>Premium Usage of $Comms (includes creation of Chatrooms)</li>
            <li>Three Tradingbots</li>
            <li>Up to 30 Alarms</li>
          </ul>
          <button className="sbmt-button" onClick={() => handlePriceButtonClick('Gold', activeTab === 'Yearly' ? 365 : 30)}>
            {buttonText[activeTab].gold}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Subscription;
