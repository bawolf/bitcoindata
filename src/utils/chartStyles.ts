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
  cumulativeFlipped:
    'In %{y:.1f}% of days, Bitcoin was at<br>%{x:.1f}% or less of its ATH <extra></extra>',
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

// Mobile-optimized layout with better legend positioning
export const MOBILE_LAYOUT = {
  ...BASE_LAYOUT,
  margin: { t: 20, r: 10, b: 80, l: 50 }, // Increased bottom margin for legend
  font: {
    family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`,
    size: 12,
  },
  legend: {
    x: 0.5,
    y: -0.15, // Position below the chart
    xanchor: 'center',
    orientation: 'h',
  },
};

// Utility function to get responsive layout
export const getResponsiveLayout = (baseLayout: any = {}) => {
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
  return {
    ...(isMobile ? MOBILE_LAYOUT : BASE_LAYOUT),
    ...baseLayout,
  };
};

// Helper for charts that don't need legends on mobile
export const getResponsiveLayoutNoLegend = (baseLayout: any = {}) => {
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
  const layout = {
    ...(isMobile ? MOBILE_LAYOUT : BASE_LAYOUT),
    ...baseLayout,
  };

  if (isMobile) {
    layout.showlegend = false;
    layout.margin = { t: 10, r: 10, b: 40, l: 50 }; // Tighter margins when no legend
  }

  return layout;
};

export const CHART_CONFIG = {
  responsive: true,
  displayModeBar: false,
};
