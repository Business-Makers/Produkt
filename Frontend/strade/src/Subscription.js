import React, { useState } from 'react';
import './App.css';
import './Subscription.css';

const Subscription = () => {
  const [activeTab, setActiveTab] = useState('Yearly');

  function handleTabClick(tab) {
    setActiveTab(tab); // Aktiviere den entsprechenden Tab
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
            <li>One Trade</li>
            <li>Access to 1 Portfolio</li>
            <li>Default Usage of $Comms</li>
          </ul>
          <button className="sbmt-button">{buttonText[activeTab].basic}</button>
        </div>
        <div className="subscription silver">
          <h2>Silver Membership</h2>
          <ul>
            <li>Up to 25 Trades</li>
            <li>Access to 4 different Portfolios</li>
            <li>Default Usage of $Comms</li>
          </ul>
          <button className="sbmt-button">{buttonText[activeTab].silver}</button>
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
          <button className="sbmt-button">{buttonText[activeTab].gold}</button>
        </div>
      </div>
    </div>
  );
};

export default Subscription;
