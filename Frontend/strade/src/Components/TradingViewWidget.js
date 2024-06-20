import React, { useEffect } from 'react';

const TradingViewWidget = ({ symbol }) => {
  useEffect(() => {
    // Dynamisch das Script-Tag hinzufügen
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;

    script.onload = () => {
      if (window.TradingView) {
        new window.TradingView.widget({
          width: 980,
          height: 610,
          symbol: symbol,
          interval: "D",
          timezone: "Etc/UTC",
          theme: "dark", // Setze das Theme auf "dark"
          style: "1",
          locale: "en",
          toolbar_bg: "#1e1e1e",
          enable_publishing: false,
          allow_symbol_change: true,
          container_id: "tradingview_12345"
        });
      }
    };

    document.getElementById('tradingview-widget-container').appendChild(script);

    return () => {
      // Clean up the script if the component is unmounted
      document.getElementById('tradingview-widget-container').removeChild(script);
    };
  }, [symbol]);

  return (
    <div className="tradingview-widget-container" id="tradingview-widget-container">
      <div id="tradingview_12345"></div>
    </div>
  );
};

export default TradingViewWidget;
