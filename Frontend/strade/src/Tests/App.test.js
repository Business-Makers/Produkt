// test.js

import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import App from '../Components/App';

describe('App Component', () => {
  test('renders login links when not authenticated', () => {
    render(
      <Router>
        <App />
      </Router>
    );

    // Check for login and signup links
    const loginLink = screen.getByRole('link', { name: /login/i });
    const signupLink = screen.getByRole('link', { name: /sign up/i });

    expect(loginLink).toBeInTheDocument();
    expect(signupLink).toBeInTheDocument();
  });

  test('renders navigation sidebar when authenticated', () => {
    // Mock useToken hook to simulate authenticated state
    jest.mock('./useToken', () => ({
      __esModule: true,
      default: () => ({
        token: 'mockedToken',
        setToken: jest.fn(),
      }),
    }));

    render(
      <Router>
        <App />
      </Router>
    );

    // Check for sidebar navigation links
    const subscriptionLink = screen.getByRole('link', { name: /subscription/i });
    const tradingLink = screen.getByRole('link', { name: /trading/i });
    const portfolioLink = screen.getByRole('link', { name: /portfolio/i });
    const marketLink = screen.getByRole('link', { name: /market/i });
    const commsLink = screen.getByRole('link', { name: /comms/i });

    expect(subscriptionLink).toBeInTheDocument();
    expect(tradingLink).toBeInTheDocument();
    expect(portfolioLink).toBeInTheDocument();
    expect(marketLink).toBeInTheDocument();
    expect(commsLink).toBeInTheDocument();
  });
});