import React, { Component } from 'react';
import Chart from 'react-apexcharts';

class Donut extends Component {
  constructor(props) {
    super(props);

    this.state = {
      options: {
        chart: {
          background: '#1e1e1e',
        },
        labels: props.data.map(account => account.exchange_name),
        legend: {
          labels: {
            colors: '#FFFFFF' // Farbe der Legendenbeschriftungen
          }
        },
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                total: {
                  show: true,
                  label: 'Total',
                  color: '#FFFFFF'
                }
              }
            }
          }
        }
      },
      series: props.data.map(account => account.currency_count)
    };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.data !== this.props.data) {
      this.setState({
        options: {
          ...this.state.options,
          labels: this.props.data.map(account => account.exchange_name),
        },
        series: this.props.data.map(account => account.currency_count)
      });
    }
  }

  render() {
    return (
      <div className="donut">
        <Chart options={this.state.options} series={this.state.series} type="donut" width="380" />
      </div>
    );
  }
}

export default Donut;