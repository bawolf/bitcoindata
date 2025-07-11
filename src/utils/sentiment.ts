/**
 * Sentiment utilities for Bitcoin percentage of ATH
 * Consolidates all sentiment-related helper functions used throughout the app
 */

export interface SentimentData {
  color: string;
  bgColor: string;
  word: string;
  intensity: 'legendary' | 'euphoric' | 'good' | 'okay' | 'tough' | 'hard';
}

/**
 * Get sentiment color classes based on percent of ATH
 */
export const getSentimentColor = (percentOfAth: number): string => {
  if (percentOfAth > 100) return 'text-green-700'; // New ATH territory - ultra euphoric
  if (percentOfAth >= 90) return 'text-green-600'; // Very close to ATH - euphoric
  if (percentOfAth >= 70) return 'text-green-500'; // Pretty good
  if (percentOfAth >= 50) return 'text-yellow-500'; // Okay
  if (percentOfAth >= 30) return 'text-orange-500'; // Getting tough
  return 'text-red-500'; // Really hard
};

/**
 * Get sentiment background classes based on percent of ATH
 */
export const getSentimentBg = (percentOfAth: number): string => {
  if (percentOfAth > 100) return 'bg-green-100 border-green-300'; // New ATH territory - ultra euphoric
  if (percentOfAth >= 90) return 'bg-green-50 border-green-200';
  if (percentOfAth >= 70) return 'bg-green-50 border-green-200';
  if (percentOfAth >= 50) return 'bg-yellow-50 border-yellow-200';
  if (percentOfAth >= 30) return 'bg-orange-50 border-orange-200';
  return 'bg-red-50 border-red-200';
};

/**
 * Get sentiment word/phrase based on percent of ATH
 */
export const getSentimentWord = (percentOfAth: number): string => {
  if (percentOfAth > 100) return 'an amazing';
  if (percentOfAth >= 90) return 'an easy';
  if (percentOfAth >= 70) return 'a medium';
  if (percentOfAth >= 50) return 'a hard';
  return 'really hard';
};

/**
 * Get gradient color for intensity visualization
 */
export const getIntensityColor = (percentOfAth: number): string => {
  if (percentOfAth > 100) return 'from-green-600 to-green-700';
  if (percentOfAth >= 90) return 'from-green-500 to-green-600';
  if (percentOfAth >= 70) return 'from-green-400 to-green-500';
  if (percentOfAth >= 50) return 'from-yellow-400 to-yellow-500';
  if (percentOfAth >= 35) return 'from-orange-400 to-orange-500';
  if (percentOfAth >= 20) return 'from-orange-500 to-red-500';
  return 'from-red-600 to-red-700';
};

/**
 * Get comprehensive sentiment data in one call
 */
export const getSentimentData = (percentOfAth: number): SentimentData => {
  let intensity: SentimentData['intensity'];

  if (percentOfAth > 100) intensity = 'legendary';
  else if (percentOfAth >= 90) intensity = 'euphoric';
  else if (percentOfAth >= 70) intensity = 'good';
  else if (percentOfAth >= 50) intensity = 'okay';
  else if (percentOfAth >= 30) intensity = 'tough';
  else intensity = 'hard';

  return {
    color: getSentimentColor(percentOfAth),
    bgColor: getSentimentBg(percentOfAth),
    word: getSentimentWord(percentOfAth),
    intensity,
  };
};
