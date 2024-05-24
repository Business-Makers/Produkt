import React, { useState } from 'react';
import './App.css';
import './Subscription.css';

  const Subscription = () => {
  const [activeTab, setActiveTab] = useState('Yearly');
  const [buttonText, setButtonText] = useState('150$ / Year'); 

  function handleTabClick(tab) {
    setActiveTab(tab); // Aktiviere den entsprechenden Tab
    if (tab === 'Yearly') {
        setButtonText('150$ / Year'); // Setze den Button-Text basierend auf dem Tab
    } else if (tab === 'Monthly') {
        setButtonText('12$ / Month'); // Setze den Button-Text basierend auf dem Tab
    }
}
  
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
              <li>Up to 25 Trades</li>
              <li>Access to 4 different Portfolios</li>
              <li>Default Usage of $Comms</li>
            </ul>
            <button className="sbmt-button">{buttonText}</button>
          </div>
          <div className="subscription silver">
            <h2>Silver Membership</h2>
            <ul>
              <li>Up to 25 Trades</li>
              <li>Access to 4 different Portfolios</li>
              <li>Default Usage of $Comms</li>
            </ul>
            <button className="sbmt-button">{buttonText}</button>
          </div>
          <div className="subscription gold">
            <h2>Gold Membership</h2>
            <ul>
              <li>Up to 100 Trades</li>
              <li>Access to 10 different Portfolios</li>
              <li>Premium Usage of $Comms <p>  </p>(includes creation of Chatrooms)</li>
            </ul>
            <button className="sbmt-button">{buttonText}</button>
          </div>
        </div>
      </div>
    );
  };
  
  export default Subscription;
