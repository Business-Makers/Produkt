import React from 'react';
import { render, waitFor } from '@testing-library/react';
import { ExchangeProvider, useExchanges } from '../Components/ExchangeContext';
import axios from 'axios';

// Mock axios for testing purposes
jest.mock('axios');

describe('ExchangeProvider', () => {
  beforeEach(() => {
    axios.get.mockClear(); // Clear any prior mock setup for axios.get
  });

  it('provides exchanges through context', async () => {
    // Mock data to be returned by axios
    const mockExchanges = [
      { id: 1, name: 'Exchange 1' },
      { id: 2, name: 'Exchange 2' },
    ];

    // Mock axios.get to return mockExchanges
    axios.get.mockResolvedValueOnce({ data: { dashboard: mockExchanges } });

    // Render the component tree with ExchangeProvider
    const { getByText } = render(
      <ExchangeProvider>
        <TestComponent />
      </ExchangeProvider>
    );

  });
});

// Test component using useExchanges hook
const TestComponent = () => {
  const { exchanges } = useExchanges();

  return (
    <div>
      <h1>Exchanges:</h1>
      <ul>
        {exchanges.map((exchange) => (
          <li key={exchange.id}>{exchange.name}</li>
        ))}
      </ul>
    </div>
  );
};

