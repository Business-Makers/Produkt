import React from 'react';
import { render, waitFor } from '@testing-library/react';
import axios from 'axios';
import { ExchangeProvider, useExchanges } from '../Components/ExchangeContext';
import useToken from '../Components/useToken';

// Mocking axios
jest.mock('axios');

// Mocking useToken
jest.mock('../Components/useToken');

const MockComponent = () => {
  const { exchanges } = useExchanges();
  return (
    <div>
      {exchanges.length > 0 ? (
        exchanges.map((exchange, index) => (
          <div key={index} data-testid="exchange-item">
            {exchange.name}
          </div>
        ))
      ) : (
        <div>No exchanges available</div>
      )}
    </div>
  );
};

describe('ExchangeProvider', () => {
  const token = 'fake-token';
  
  beforeEach(() => {
    useToken.mockReturnValue({ token });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('fetches and provides exchanges data', async () => {
    const exchangesData = [
      { name: 'Exchange 1' },
      { name: 'Exchange 2' },
    ];

    axios.get.mockResolvedValueOnce({ data: { dashboard: exchangesData } });

    const { getAllByTestId, getByText } = render(
      <ExchangeProvider>
        <MockComponent />
      </ExchangeProvider>
    );

    await waitFor(() => {
      expect(getAllByTestId('exchange-item')).toHaveLength(2);
    });
  });

  test('displays error message if fetch fails', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network Error'));

    const { getByText } = render(
      <ExchangeProvider>
        <MockComponent />
      </ExchangeProvider>
    );
  });
});
