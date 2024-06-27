import React from 'react';
import { Link } from 'react-router-dom';
import { FaChartLine, FaWallet, FaToolbox, FaDollarSign, FaComments } from 'react-icons/fa';
import '../Styles/SideNav.css';

function SideNav() {
  return (
    <nav className="side-nav">
      <div className="logo">
        <Link to="/">
          <img src="/strade.png" alt="logo"/>
        </Link>
      </div>
      <ul>
        <li>
          <Link to="/">
            <FaChartLine /> Dashboard
          </Link>
        </li>
        <li>
          <Link to="/portfolio">
            <FaWallet /> My Portfolio
          </Link>
        </li>
        <li>
          <Link to="/trading">
            <FaToolbox /> Terminal
          </Link>
        </li>
        <li>
          <Link to="/subscription">
            <FaDollarSign /> Subscription
          </Link>
        </li>
        <li>
          <Link to="/comms">
            <FaComments /> $Comms
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default SideNav;