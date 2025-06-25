// Format numbers to K format (e.g., 1000 -> 1k, 50000 -> 50k)
export const formatToK = (value: number): string => {
  if (value >= 1000) {
    return Math.round(value / 1000) + 'k';
  }
  return Math.round(value).toString();
};

// Format date to readable format
export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString();
};

// Format currency
export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

// Format percentage with specified decimal places
export const formatPercentage = (
  value: number,
  decimals: number = 1
): string => {
  return `${value.toFixed(decimals)}%`;
};

// Format large numbers with commas
export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US').format(value);
};

// Calculate percentile ranking
export const calculatePercentile = (
  value: number,
  sortedArray: number[]
): number => {
  const index = sortedArray.findIndex((item) => item >= value);
  if (index === -1) return 100;
  return (index / sortedArray.length) * 100;
};

// Debounce function for performance optimization
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout | undefined;

  return (...args: Parameters<T>) => {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};
