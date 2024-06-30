import React, { useState } from 'react';
import axios from 'axios';

import '../Styles/LoggedIn.css';
import '../Styles/Subscription.css';

const Subscription = () => {
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

  const connectWithServer = async (formData) => {
    const url = 'http://localhost:8001/payment';
    try {
      const response = await axios.post(url, formData);
      return response.data; // Rückgabe der Antwortdaten
    } catch (error) {
      console.error('Fehler beim Senden der Anfrage:', error);
      throw error; // Fehler weiterwerfen für die Fehlerbehandlung
    }
  };

  const handlePriceButtonClick = async (membership) => {
    const periodInDays = activeTab === 'Yearly' ? 365 : 30; 
    const membershipName = membership; 

  
    const confirmed = window.confirm(`Möchtest du den Kauf von ${membershipName} für ${periodInDays} Tage wirklich abschließen?`);

    if (confirmed) {
      const formData = {
        currency: 'USD',
        product_name: membershipName,
        product_days: periodInDays
      };

      try {
        const serverResponse = await connectWithServer(formData);
        console.log('Erfolgreich gesendet:', serverResponse);

        alert(`Erfolgreich ${membershipName} für ${periodInDays} Tage gekauft!`);
      } catch (error) {
        console.error('Fehler beim Senden der Anfrage:', error);
        alert('Fehler beim Senden der Anfrage. Bitte versuche es später erneut.'); // Fehlermeldung anzeigen
      }
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
          <p className="active-status">(Currently active)</p>
          <ul>
            <li>One Trade</li>
            <li>Access to 1 Portfolio</li>
            <li>Default Usage of $Comms</li>
          </ul>
          <button className="sbmt-button" onClick={() => handlePriceButtonClick('basic')}>{buttonText[activeTab].basic}</button>
        </div>
        <div className="subscription silver">
          <h2>Silver Membership</h2>
          <ul>
            <li>Up to 25 Trades</li>
            <li>Access to 4 different Portfolios</li>
            <li>Default Usage of $Comms</li>
          </ul>
          <button className="sbmt-button" onClick={() => handlePriceButtonClick('silver')}>{buttonText[activeTab].silver}</button>
        </div>
        <div className="subscription gold">
          <h2>Gold Membership</h2>
          <ul>
            <li>Up to 100 Trades</li>
            <li>Access to 10 different Portfolios</li>
            <li>Premium Usage of $Comms <p>  </p>(includes creation of Chatrooms)</li>
            <li>Three Tradingbots</li>
            <li>Up to 30 Alarms</li>
          </ul>
          <button className="sbmt-button" onClick={() => handlePriceButtonClick('gold')}>{buttonText[activeTab].gold}</button>
        </div>
      </div>
    </div>
  );
};

export default Subscription;
