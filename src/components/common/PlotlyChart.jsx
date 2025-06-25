import Plot from 'react-plotly.js';

const defaultLayout = {
  margin: { t: 20, r: 20, b: 60, l: 60 },
  plot_bgcolor: 'white',
  paper_bgcolor: 'white',
  font: {
    family: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif',
  },
  autosize: true,
  xaxis: { showgrid: false },
  yaxis: { showgrid: true, gridcolor: '#f0f0f0' },
};

const defaultConfig = {
  responsive: true,
  displayModeBar: false,
};

function PlotlyChart({
  data,
  layout = {},
  config = {},
  style = { width: '100%', height: '400px' },
  ...props
}) {
  const mergedLayout = { ...defaultLayout, ...layout };
  const mergedConfig = { ...defaultConfig, ...config };

  return (
    <Plot
      data={data}
      layout={mergedLayout}
      config={mergedConfig}
      useResizeHandler={true}
      style={style}
      {...props}
    />
  );
}

export default PlotlyChart;
