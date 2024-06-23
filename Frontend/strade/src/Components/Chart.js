import React from 'react';
import Chart from 'react-apexcharts';
import '../Styles/Chart.css';

const MyChart = ({ data }) => {
  const chartOptions = {
    chart: {
      id: 'basic-line',
      type: 'line',
      animations: {
        enabled: true
      }
    },
    toolbar: {
        show: true,
        tools: {
          download: true,
          selection: true,
          zoom: true,
          zoomin: true,
          zoomout: true,
          pan: true,
          reset: true,
        },
        autoSelected: 'zoom'
      },
    stroke: {
      curve: 'smooth', // Option für glatte Linien
      width: 2 // Linienbreite
    },
    xaxis: {
        categories: data.categories,
        labels: {
          style: {
            colors: '#FFFFFF'  // Farbe für die x-Achsenbeschriftungen
          }
        }
      },
      yaxis: {
        title: {
          text: 'Values',
          style: {
            color: '#FFFFFF'  // Farbe für die y-Achsentitel
          }
        },
        labels: {
          style: {
            colors: '#FFFFFF'  // Farbe für die y-Achsenbeschriftungen
          }
        }
      },
    tooltip: {
        enabled: true,
        style: {
          fontSize: '12px',
          fontFamily: undefined,
          colors: ['#fff'] // Textfarbe im Tooltip
        },
        theme: 'dark', // Dunkles Thema für den Tooltip
        onDatasetHover: {
          highlightDataSeries: true,
        },
        x: {
          show: true,
          format: 'dd MMM', // Format für die x-Achse im Tooltip
        },
        marker: {
          show: true,
        },
        y: {
          formatter: (value) => { return value; } // Format für die y-Achse im Tooltip
        },
        fillSeriesColor: true,
      },
    markers: {
        size: 4,
        colors: ['#238321'], // Standardfarbe der Markierungen
        strokeColors: '#35898c',
        strokeWidth: 2,
        hover: {
          size: 7,
          sizeOffset: 3,
          fillColor: '#35898c',
          strokeColor: '#626363',
          strokeWidth: 3
        }
      },
      dataLabels: {
        enabled: false // Deaktiviert die Datenbeschriftungen
      }
  };

  const chartSeries = [
    {
      name: 'Balance',
      data: data.series
    }
  ];

  return (
    <div classname="chart-container">
      <Chart options={chartOptions} series={chartSeries} type="line" height={350} style={{marginTop: 50 + 'px'}}/>
    </div>
  );
};

export default MyChart;
