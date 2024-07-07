const mockTrades = [
    {
      account_Holder: 'Alice',
      exchange_name: 'KUCOIN',
      trade_id: '1',
      trade_type: 'buy',
      trade_price: 50000,
      currency_name: 'BTC',
      currency_volume: 0.1,
      trade_status: 'completed',
      date_create: '2023-06-01',
      date_bought: '2023-06-01',
      date_sale: null,
      purchase_rate: 50000,
      selling_rate: null,
      comment: 'Initial investment',
      stop_loss_price: null,
      take_profits: [{ price: 60000 }]
    },
    {
      account_Holder: 'Bob',
      exchange_name: 'BINANCE',
      trade_id: '2',
      trade_type: 'sell',
      trade_price: 60000,
      currency_name: 'ETH',
      currency_volume: 1.5,
      trade_status: 'completed',
      date_create: '2023-07-01',
      date_bought: '2023-06-15',
      date_sale: '2023-07-01',
      purchase_rate: 4000,
      selling_rate: 6000,
      comment: 'Profit sale',
      stop_loss_price: 3500,
      take_profits: []
    },
    {
      account_Holder: 'Charlie',
      exchange_name: 'KRAKEN',
      trade_id: '3',
      trade_type: 'buy',
      trade_price: 150,
      currency_name: 'ADA',
      currency_volume: 200,
      trade_status: 'completed',
      date_create: '2023-08-01',
      date_bought: '2023-08-01',
      date_sale: null,
      purchase_rate: 1.5,
      selling_rate: null,
      comment: 'Diversification',
      stop_loss_price: 1.0,
      take_profits: [{ price: 2.0 }, { price: 2.5 }]
    }
  ];
  
  export default mockTrades;