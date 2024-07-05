
import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { BrowserRouter as Router } from 'react-router-dom';
import Homepage from '../Components/Homepage';

describe('Homepage Component', () => {
  test('renders without crashing', () => {
    const { getByText } = render(
      <Router>
        <Homepage />
      </Router>
    );
    expect(getByText('Welcome to $Trade - your trusted crypto exchange platform with advanced trading bots')).toBeInTheDocument();
  });

  test('renders exchange list', () => {
    const { getByAltText } = render(
      <Router>
        <Homepage />
      </Router>
    );

    // Check if one of the exchange images is rendered
    expect(getByAltText('kucoin')).toBeInTheDocument();
    expect(getByAltText('binance')).toBeInTheDocument();
    expect(getByAltText('binanceTR')).toBeInTheDocument();
  });

  test('renders features section', () => {
    const { getByText } = render(
      <Router>
        <Homepage />
      </Router>
    );
    expect(getByText('Why choose $Trade?')).toBeInTheDocument();
    expect(getByText('Security first: Our platform uses the latest security technologies to protect your data and transactions. With two-factor authentication and encrypted communication, you can trade with peace of mind.')).toBeInTheDocument();
  });

  test('renders reviews section', () => {
    const { getByText } = render(
      <Router>
        <Homepage />
      </Router>
    );
    expect(getByText('Reviews')).toBeInTheDocument();
  });

  test('renders FAQ section', () => {
    const { getByText } = render(
      <Router>
        <Homepage />
      </Router>
    );
    expect(getByText('FAQ')).toBeInTheDocument();
    expect(getByText('What is a crypto exchange?')).toBeInTheDocument();
  });

  test('renders SignUp link', () => {
    const { getByText } = render(
      <Router>
        <Homepage />
      </Router>
    );
    expect(getByText('Start trading now')).toBeInTheDocument();
  });
});