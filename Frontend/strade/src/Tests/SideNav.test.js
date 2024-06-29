// SideNav.test.js
import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import SideNav from '../Components/SideNav';
import '@testing-library/jest-dom/extend-expect'; // für zusätzliche Matcher wie "toBeInTheDocument"

describe('SideNav', () => {
  test('renders the logo', () => {
    const { getByAltText } = render(
      <Router>
        <SideNav />
      </Router>
    );
    const logo = getByAltText('logo');
    expect(logo).toBeInTheDocument();
  });

  test('renders the navigation links', () => {
    const { getByText } = render(
      <Router>
        <SideNav />
      </Router>
    );

    const dashboardLink = getByText('Dashboard');
    const portfolioLink = getByText('My Portfolio');
    const terminalLink = getByText('Terminal');
    const subscriptionLink = getByText('Subscription');
    const commsLink = getByText('$Comms');

    expect(dashboardLink).toBeInTheDocument();
    expect(portfolioLink).toBeInTheDocument();
    expect(terminalLink).toBeInTheDocument();
    expect(subscriptionLink).toBeInTheDocument();
    expect(commsLink).toBeInTheDocument();
  });

  test('links have correct paths', () => {
    const { getByText } = render(
      <Router>
        <SideNav />
      </Router>
    );

    const dashboardLink = getByText('Dashboard').closest('a');
    const portfolioLink = getByText('My Portfolio').closest('a');
    const terminalLink = getByText('Terminal').closest('a');
    const subscriptionLink = getByText('Subscription').closest('a');
    const commsLink = getByText('$Comms').closest('a');

    expect(dashboardLink).toHaveAttribute('href', '/');
    expect(portfolioLink).toHaveAttribute('href', '/portfolio');
    expect(terminalLink).toHaveAttribute('href', '/trading');
    expect(subscriptionLink).toHaveAttribute('href', '/subscription');
    expect(commsLink).toHaveAttribute('href', '/comms');
  });
});