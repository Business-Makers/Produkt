import React from 'react';
import '../Styles/Balance.css';

const ExchangeBalance = ({ exchange }) => {
  return (
    <div className="exchange-balance">
      <h3>{exchange.exchange_name}</h3>
      <p><strong>Account Holder:</strong> {exchange.account_holder}</p>
      <p><strong>Balance:</strong> {`${exchange.balance.toFixed(2)} $`}</p>
      <p><strong>Currency Count:</strong> {exchange.currency_count}</p>
    </div>
  );
};

const TotalBalance = ({ total }) => {
  return (
    <div className="total-balance">
      <h3>Total Balance</h3>
      <p>{total}</p>
    </div>
  );
};

/** Displays the Balance of each given exchange the User is connected to and calculates the total of all balances
 * 
 * @param exchanges The array of connected exchanges given by the dashboard-call to the backend
 * 
 * @returns HTML containing the balance values
*/
const MyBalances = ({ exchanges }) => {
  const totalBalance = exchanges.reduce((sum, exchange) => sum + exchange.balance, 0);
  const formattedBalance = `${totalBalance.toFixed(2)} $`;

  return (
    <div className="balances-container">
      {exchanges.map((exchange, index) => (
        <ExchangeBalance key={index} exchange={exchange} />
      ))}
      <TotalBalance total={formattedBalance} />
    </div>
  );
};

export default MyBalances;