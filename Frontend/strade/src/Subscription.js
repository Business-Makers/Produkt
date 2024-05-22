import React, { useState } from 'react';
import './App.css';
import './Subscription.css';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const Subscription = () => {
    const [activeTab, setActiveTab] = useState('Yearly');
  
    return (
      <div className="subscription-wrapper">
        <div className="tabs">
          <div className={`tab ${activeTab === 'Yearly' ? 'active' : ''}`} onClick={() => setActiveTab('Yearly')}>
            Yearly
          </div>
          <div className={`tab ${activeTab === 'Monthly' ? 'active' : ''}`} onClick={() => setActiveTab('Monthly')}>
            Monthly
          </div>
        </div>
        <div className="subscriptions-container">
          <div className="subscription silver">
            <h2>Silver Membership</h2>
            <p className="active-status">(Currently active)</p>
            <ul>
              <li>Up to 25 Trades</li>
              <li>Access to 4 different Portfolios</li>
              <li>Default Usage of $Comms</li>
            </ul>
          </div>
          <div className="subscription gold">
            <h2>Gold Membership</h2>
            <ul>
              <li>Up to 100 Trades</li>
              <li>Access to 10 different Portfolios</li>
              <li>Premium Usage of $Comms <p>  </p>(includes creation of Chatrooms)</li>
            </ul>
            <button>300$ / Year</button>
          </div>
        </div>
      </div>
    );
  };
  
  export default Subscription;
