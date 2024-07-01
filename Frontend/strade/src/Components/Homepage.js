import React from 'react';
import '../Styles/Homepage.css';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import SignUp from './SignUp';
import KucoinImage from '../Images/Kucoin.png';
import BinanceImage from '../Images/Binance.png';
import BinanceTRImage from '../Images/BinanceTR.png';
import BITFINEX from '../Images/Bitfinex.png';
import BITGET from '../Images/Bitget.png';
import BITSTAMP from '../Images/Bitstamp.png';
import BYBIT from '../Images/Bybit.png';
import COINBASE from '../Images/coinBase.png';
import GATEIO from '../Images/gateio.png';
import GEMINI from '../Images/gemini.png';
import HTX from '../Images/htx.png';
import KRAKEN from '../Images/kraken.png';
import OKX from '../Images/OKX.png';

const exchanges = [
  { id: 1, name: 'kucoin', imgSrc: KucoinImage, link: 'https://www.kucoin.com'},
  { id: 2, name: 'binance', imgSrc: BinanceImage, link: 'https://www.binance.com/en'},
  { id: 3, name: 'binanceTR', imgSrc: BinanceTRImage, link: 'https://www.trbinance.com/'},
  { id: 4, name: 'bitfinex', imgSrc: BITFINEX, link: 'https://www.bitfinex.com/'},
  { id: 5, name: 'bidget', imgSrc: BITGET, link: 'https://www.bitget.com/de/'},
  { id: 6, name: 'bitstamp', imgSrc: BITSTAMP, link: 'https://www.bitstamp.net/'},
  { id: 7, name: 'bybit', imgSrc: BYBIT, link: 'https://www.bybit.com/en/'},
  { id: 8, name: 'coinBase', imgSrc: COINBASE, link: 'https://www.coinbase.com/de/'},
  { id: 9, name: 'gate.io', imgSrc: GATEIO, link: 'https://www.gate.io/de'},
  { id: 10, name: 'gemini', imgSrc: GEMINI, link: 'https://gemini.google.com/?hl=de'},
  { id: 11, name: 'HTX', imgSrc: HTX, link: 'https://www.htx.com/'},
  { id: 12, name: 'kraken', imgSrc: KRAKEN, link: 'https://www.kraken.com/'},
  { id: 13, name: 'OKX', imgSrc: OKX, link: 'https://www.okx.com/de'},
];

const ExchangeList = () => {
  return (
    <div className="exchanges-container">
      <div className="exchange-header">
        <h2>Available Exchanges</h2>
      </div>
      <div className="exchange-list">
        {exchanges.map(exchange => (
          <div key={exchange.id} className="exchange-item">
            <a href={exchange.link} target="_blank" rel="noopener noreferrer">
              <img src={exchange.imgSrc} alt={exchange.name} className="exchange-image" />
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

function Homepage() {
  return (
    <div className="home">
      <section className="intro">
        <p>Welcome to $Trade - your trusted crypto exchange platform with advanced trading bots</p>
        <p>Experience trading on a new level with our unique features such as bots and much more</p>
        <p><Link to="/signup">Start trading now</Link></p>
      </section>

      <section className='exchanges'>
        <ExchangeList/>
      </section>

      <section className="features">
        <h2>Why choose $Trade?</h2>
        <ul>
        <li>Security first: Our platform uses the latest security technologies to protect your data and transactions. With two-factor authentication and encrypted communication, you can trade with peace of mind.</li>
        <li>Ease of use: Our intuitive user interface is suitable for both beginners and experienced traders. Experience a smooth and efficient trading process with our easy-to-navigate platform.</li>
        <li>Automated trading bots: Our advanced trading bots analyze the market in real time and automatically execute trades based on predefined strategies. These bots are designed to identify opportunities and react at lightning speed to give you a competitive edge.</li>
        </ul>
      </section>

      <section className="reviews">
        <h2>Reviews</h2>
        <small>
        At $Trade we place great value on feedback from our users. Your
        experiences and opinions are invaluable to us as they help us to
        continuously improve our services and customize them to your needs.
        Read the reviews of our satisfied customers and learn first-hand how our
        platform and trading bots have helped them achieve their crypto trading
        goals.
        </small>

        <div className="review-container">
        <div className="review">
          <p>"This app has revolutionized my trading experience!" - Max M.</p>
        </div>
        <div className="review">
          <p>"Safe, fast and reliable. Absolutely recommendable." - Anna K.</p>
        </div>
      </div>

      </section>
      <section className="faq">
        <h2>FAQ</h2>
        <div className="faq-item">
          <h3>What is a crypto exchange?</h3>
          <p>A crypto exchange is a platform that allows users to buy, sell or trade cryptocurrencies such as Bitcoin, Ethereum and other digital assets.
             It acts as a marketplace for cryptocurrencies.</p>
        </div>
        <div className="faq-item">
          <h3>Why should I use your exchange platform?</h3>
          <p>Our exchange platform not only offers a secure and user-friendly environment for trading cryptocurrencies, but also powerful trading bots to help you
             optimize your trading strategies and maximize your profits.</p>
        </div>
        <div className="faq-item">
          <h3>How secure is your platform?</h3>
          <p>We use the latest security technologies, including encrypted communication and two-factor authentication, to ensure the security of
             your data and transactions. Your security is our top priority.</p>
        </div>
        <div className="faq-item">
          <h3>Do you offer support for trading bots?</h3>
          <p>Yes, we offer advanced trading bots that can analyze the market in real time and automatically execute trades based on predefined strategies. These bots help you to trade more
             efficiently and make the most of market opportunities.</p>
        </div>
      </section>
    </div>
  );
}

export default Homepage;