// Bitcoin Analysis Data Types
export interface CurrentAnalysis {
  current_percent_of_ath: number;
  current_price: number;
  dollar_difference_from_ath: number;
  percentile_rank: number;
}

export interface HardestDay {
  date: string;
  percent_of_ath: number;
  price: number;
  ath_at_time: number;
  dollar_loss: number;
}

export interface EasiestDay {
  date: string;
  percent_of_ath: number;
  price: number;
  ath_at_time: number;
  dollar_gain: number;
}

export interface HardestDaysData {
  hardest_days: HardestDay[];
  easiest_days: EasiestDay[];
  above_ath_count: number;
  above_ath_percentage: number;
  total_days: number;
  recent_above_ath_days: Array<{
    date: string;
    price: number;
    percent_of_ath: number;
  }>;
  first_date: string;
}

export interface HistoricalData {
  dates: string[];
  percentages: number[];
  ath_values: number[];
  high_values: number[];
}

export interface DistributionData {
  histogram: {
    bins: number[];
    counts: number[];
  };
  cumulative: {
    percentages: number[];
    cumulative_percentages: number[];
  };
  statistics: {
    mean_percent: number;
    median_percent: number;
    std_percent: number;
    coefficient_of_variation: number;
    min_percent: number;
    max_percent: number;
    days_at_ath: number;
    total_days: number;
  };
  volatility_bands: {
    mean_minus_2std: number;
    mean_minus_1std: number;
    mean_plus_1std: number;
    mean_plus_2std: number;
  };
  percentiles: {
    '10th': number;
    '25th': number;
    '75th': number;
    '90th': number;
    '95th': number;
    '99th': number;
  };
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  last_updated?: string;
}

// Component Props Types
export interface LoadingErrorWrapperProps {
  loading: boolean;
  error: string | null;
  loadingMessage?: string;
  errorMessage?: string;
  children: React.ReactNode;
}

export interface SectionProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export interface ChartContainerProps {
  title?: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}

export interface InsightBoxProps {
  title?: string;
  icon?: string;
  children: React.ReactNode;
  className?: string;
}

export interface PlotlyChartProps {
  data: any[];
  layout?: any;
  config?: any;
  style?: React.CSSProperties;
}

export interface CurrentStatsProps {
  currentAnalysis: CurrentAnalysis | null;
  loading: boolean;
  error: string | null;
}

export interface HardestDaysProps {
  hardestDays: HardestDaysData | null;
  loading: boolean;
  error: string | null;
}

export interface EasiestDaysProps {
  easiestDays: EasiestDay[] | null;
  loading: boolean;
  error: string | null;
}

export interface HistoricalChartProps {
  historicalData: HistoricalData | null;
  loading: boolean;
  error: string | null;
}

export interface CumulativeChartProps {
  currentAnalysis: CurrentAnalysis | null;
}

// Hook Return Types
export interface UseApiDataReturn<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

// Chart Style Types
export interface ChartColors {
  bitcoinOrange: string;
  bitcoinOrangeLight: string;
  bitcoinOrangeDark: string;
  red: string;
  green: string;
  purple: string;
  gray: string;
  gridColor: string;
}

export interface LineStyle {
  width: number;
  dash?: string;
}

export interface PlotlyTrace {
  x?: any[];
  y?: any[];
  type?: string;
  mode?: string;
  name?: string;
  line?: LineStyle & { color?: string };
  marker?: any;
  fill?: string;
  fillcolor?: string;
  hovertemplate?: string;
  text?: string[];
  textposition?: string;
  textfont?: any;
}
