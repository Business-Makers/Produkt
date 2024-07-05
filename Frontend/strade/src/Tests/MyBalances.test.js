import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import MyBalances from '../Components/MyBalances';

const mockExchanges = [
  {
    exchange_name: 'binance',
    account_holder: 'John Doe',
    balance: 12345.67,
    currency_count: 5,
  },
  {
    exchange_name: 'kraken',
    account_holder: 'Jane Doe',
    balance: 23456.78,
    currency_count: 3,
  },
  {
    exchange_name: 'coinbase',
    account_holder: 'Alice',
    balance: 34567.89,
    currency_count: 8,
  },
];

describe('MyBalances Component', () => {
  test('renders without crashing', () => {
    const { getByText } = render(<MyBalances exchanges={mockExchanges} />);
    expect(getByText('Total Balance')).toBeInTheDocument();
  });

  test('displays the correct total balance', () => {
    const { getByText } = render(<MyBalances exchanges={mockExchanges} />);
    const totalBalance = mockExchanges.reduce((sum, exchange) => sum + exchange.balance, 0).toFixed(2);
    expect(getByText(`Total Balance`)).toBeInTheDocument();
    expect(getByText(`${totalBalance} $`)).toBeInTheDocument();
  });

  test('displays all exchange balances correctly', () => {
    const { getByText } = render(<MyBalances exchanges={mockExchanges} />);
    mockExchanges.forEach(exchange => {
      expect(getByText(exchange.exchange_name)).toBeInTheDocument();
      expect(getByText(exchange.account_holder)).toBeInTheDocument();
    });
  });

  test('renders "No exchange connected." when no exchanges are passed', () => {
    const { getByText } = render(<MyBalances exchanges={[]} />);
  });
});