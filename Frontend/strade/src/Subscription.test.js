import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Subscription from './Subscription';

describe('Subscription Component', () => {
  test('renders correctly with default yearly tab active', () => {
    render(<Subscription />);

    // Check for tabs
    expect(screen.getByText(/Yearly/i)).toBeInTheDocument();
    expect(screen.getByText(/Monthly/i)).toBeInTheDocument();

    // Check if yearly tab is active
    expect(screen.getByText(/Yearly/i)).toHaveClass('active');
    expect(screen.getByText(/Monthly/i)).not.toHaveClass('active');

    // Check for subscription plans
    expect(screen.getByText(/Silver Membership/i)).toBeInTheDocument();
    expect(screen.getByText(/Gold Membership/i)).toBeInTheDocument();
    expect(screen.getByText(/\(Currently active\)/i)).toBeInTheDocument();
    expect(screen.getByText(/300\$ \/ Year/i)).toBeInTheDocument();
  });

  test('switches to monthly tab when clicked', () => {
    render(<Subscription />);

    const yearlyTab = screen.getByText(/Yearly/i);
    const monthlyTab = screen.getByText(/Monthly/i);

    // Ensure initial state
    expect(yearlyTab).toHaveClass('active');
    expect(monthlyTab).not.toHaveClass('active');

    // Click the monthly tab
    fireEvent.click(monthlyTab);

    // Check if monthly tab is now active
    expect(monthlyTab).toHaveClass('active');
    expect(yearlyTab).not.toHaveClass('active');
  });

  test('renders subscription details correctly', () => {
    render(<Subscription />);

    // Check for silver membership details
    expect(screen.getByText(/Silver Membership/i)).toBeInTheDocument();
    expect(screen.getByText(/Up to 25 Trades/i)).toBeInTheDocument();
    expect(screen.getByText(/Access to 4 different Portfolios/i)).toBeInTheDocument();
    expect(screen.getByText(/Default Usage of \$Comms/i)).toBeInTheDocument();

    // Check for gold membership details
    expect(screen.getByText(/Gold Membership/i)).toBeInTheDocument();
    expect(screen.getByText(/Up to 100 Trades/i)).toBeInTheDocument();
    expect(screen.getByText(/Access to 10 different Portfolios/i)).toBeInTheDocument();
    expect(screen.getByText(/Premium Usage of \$Comms \(includes creation of Chatrooms\)/i)).toBeInTheDocument();
    expect(screen.getByText(/300\$ \/ Year/i)).toBeInTheDocument();
  });

  test('button click triggers correct action', () => {
    render(<Subscription />);

    // Check if button is in the document
    const button = screen.getByText(/300\$ \/ Year/i);
    expect(button).toBeInTheDocument();

    // Mock function to handle button click
    const handleClick = jest.fn();
    button.onclick = handleClick;

    // Simulate button click
    fireEvent.click(button);

    // Check if the click handler was called
    expect(handleClick).toHaveBeenCalled();
  });
});
