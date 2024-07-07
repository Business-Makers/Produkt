import React from 'react';
import { render, screen, cleanup } from '@testing-library/react';
import TradingViewWidget from '../Components/TradingViewWidget';

// Mock für das externe TradingView-Skript
beforeAll(() => {
  window.TradingView = {
    widget: jest.fn(),
  };
});

afterEach(() => {
  cleanup();
  jest.clearAllMocks();
});

describe('TradingViewWidget', () => {
  test('renders TradingView widget container', () => {
    render(<TradingViewWidget symbol="AAPL" />);
  });

  test('loads TradingView script and initializes widget', () => {
    render(<TradingViewWidget symbol="AAPL" />);
    
    // Prüfen, ob das Skript-Tag hinzugefügt wurde
    const script = document.querySelector('script[src="https://s3.tradingview.com/tv.js"]');

    // Simulieren, dass das Skript geladen wurde
    script.onload();

    // Überprüfen, ob das TradingView Widget initialisiert wurde
    expect(window.TradingView.widget).toHaveBeenCalledWith(expect.objectContaining({
      symbol: 'AAPL',
      container_id: 'tradingview_12345',
    }));
  });

  test('cleans up the script when component is unmounted', () => {
    const { unmount } = render(<TradingViewWidget symbol="AAPL" />);
    
    const script = document.querySelector('script[src="https://s3.tradingview.com/tv.js"]');

    // Unmount the component
    unmount();

  });
});
