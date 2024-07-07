import React from 'react';
import { render } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import '@testing-library/jest-dom/extend-expect';
import SideNav from '../Components/SideNav';

describe('SideNav Component', () => {
  test('renders without crashing', () => {
    const { getByAltText } = render(
      <Router>
        <SideNav />
      </Router>
    );
    expect(getByAltText('logo')).toBeInTheDocument();
  });

  test('renders dashboard link', () => {
    const { getByText } = render(
      <Router>
        <SideNav />
      </Router>
    );
    expect(getByText('Dashboard')).toBeInTheDocument();
  });

  test('renders terminal link', () => {
    const { getByText } = render(
      <Router>
        <SideNav />
      </Router>
    );
    expect(getByText('Terminal')).toBeInTheDocument();
  });

  test('renders subscription link', () => {
    const { getByText } = render(
      <Router>
        <SideNav />
      </Router>
    );
    expect(getByText('Subscription')).toBeInTheDocument();
  });

  test('contains correct icons', () => {
    const { container } = render(
      <Router>
        <SideNav />
      </Router>
    );
  });
});
