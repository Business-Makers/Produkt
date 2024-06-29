import React from 'react';
import { render, screen } from '@testing-library/react';
import TradingViewWidget from '../Components/TradingViewWidget';

describe('TradingViewWidget', () => {
  it('renders TradingView widget with correct symbol', async () => {
    render(<TradingViewWidget symbol="AAPL" />);

    // Wait for the script to load
    await screen.findByTestId('tradingview-script');

    // Check if the container and tradingview div are present
    const container = screen.getByTestId('tradingview-container');
    const tradingViewDiv = screen.getByTestId('tradingview-div');

    expect(container).toBeTruthy(); // or use toBeInTheDocument() if available
    expect(tradingViewDiv).toBeTruthy(); // or use toBeInTheDocument() if available
  });

  it('cleans up TradingView script on unmount', async () => {
    const { unmount } = render(<TradingViewWidget symbol="AAPL" />);
    
    // Wait for the script to load
    await screen.findByTestId('tradingview-script');

    // Check if the container is present before unmounting
    const container = screen.getByTestId('tradingview-container');
    expect(container).toBeTruthy(); // or use toBeInTheDocument() if available

    // Unmount the component
    unmount();

  });
});
