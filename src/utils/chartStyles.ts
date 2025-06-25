import type { ChartColors, LineStyle, PlotlyTrace } from '@/types';

// Chart Colors
export const COLORS: ChartColors = {
  bitcoinOrange: '#F7931A',
  bitcoinOrangeLight: 'rgba(247, 147, 26, 0.1)',
  bitcoinOrangeDark: '#E6851F',
  red: '#e74c3c',
  green: '#2ecc71',
  purple: '#9b59b6',
  gray: '#95a5a6',
  gridColor: '#f0f0f0',
};

// Line Styles
export const LINE_STYLES: Record<string, LineStyle> = {
  solid: { width: 3 },
  dashed: { width: 3, dash: 'dash' },
  dotted: { width: 2, dash: 'dot' },
  thin: { width: 1 },
};

// Common Chart Functions
export const createVerticalLine = (
  x: number,
  yMax: number,
  name: string,
  color: string,
  lineStyle: LineStyle
): PlotlyTrace => ({
  x: [x, x],
  y: [0, yMax],
  type: 'scatter',
  mode: 'lines',
  name,
  line: { ...lineStyle, color },
});

export const createHorizontalLine = (
  y: number,
  xRange: [number, number],
  name: string,
  color: string,
  lineStyle: LineStyle
): PlotlyTrace => ({
  x: xRange,
  y: [y, y],
  type: 'scatter',
  mode: 'lines',
  name,
  line: { ...lineStyle, color },
});

export const createMarker = (
  x: number,
  y: number,
  text: string,
  color: string,
  size: number = 12
): PlotlyTrace => ({
  x: [x],
  y: [y],
  type: 'scatter',
  mode: 'markers+text',
  name: text,
  marker: { color, size, symbol: 'circle' },
  text: [text],
  textposition: 'top center',
  textfont: { size: 12, color, family: 'Arial Black' },
});

export const createAxis = (title: string, options: any = {}) => ({
  title,
  showgrid: options.showgrid !== false,
  gridcolor: COLORS.gridColor,
  ...options,
});

// Hover Templates
export const HOVER_TEMPLATES = {
  price: '<b>%{x}</b><br>Price: $%{y:,.0f}<extra></extra>',
  percentage: '<b>%{x}</b><br>%{y:.1f}%<extra></extra>',
  count: '<b>%{x:.1f}%</b><br>Days: %{y}<extra></extra>',
  cumulative:
    '<b>Distance: %{x:.1f}%</b><br>Percentile: %{y:.1f}%<extra></extra>',
};

// Common Layout Configurations
export const BASE_LAYOUT = {
  margin: { t: 20, r: 20, b: 50, l: 60 },
  plot_bgcolor: 'white',
  paper_bgcolor: 'white',
  font: {
    family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`,
  },
  showlegend: true,
  legend: { x: 0.65, y: 0.95 },
};

export const CHART_CONFIG = {
  responsive: true,
  displayModeBar: false,
};
