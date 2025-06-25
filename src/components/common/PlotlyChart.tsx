import Plot from 'react-plotly.js';
import type { PlotlyChartProps } from '@/types';
import { CHART_CONFIG } from '@/utils/chartStyles';

export default function PlotlyChart({
  data,
  layout = {},
  config = CHART_CONFIG,
  style = { width: '100%', height: '400px' },
}: PlotlyChartProps) {
  return <Plot data={data} layout={layout} config={config} style={style} />;
}
