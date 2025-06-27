import { LoadingErrorWrapper } from '@/components/common';
import {
  formatRoundedNumber,
  cn,
  getSentimentColor,
  getSentimentBg,
} from '@/utils';
import type { CurrentStatsProps } from '@/types';

export default function CurrentStats({
  currentAnalysis,
  loading,
  error,
}: CurrentStatsProps) {
  return (
    <LoadingErrorWrapper
      loading={loading}
      error={error}
      loadingMessage="Loading current stats..."
    >
      {currentAnalysis && (
        <div
          className={cn(
            'rounded-xl p-8 my-10 shadow-card border-2 transition-colors duration-300',
            getSentimentBg(currentAnalysis.current_percent_of_ath)
          )}
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-black mb-1">
                ${formatRoundedNumber(currentAnalysis.current_price)}
              </div>
              <div className="text-sm text-text-light font-medium">
                Current Price
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-black mb-1">
                $
                {formatRoundedNumber(
                  currentAnalysis.dollar_difference_from_ath
                )}
              </div>
              <div className="text-sm text-text-light font-medium">
                Dollars Below ATH
              </div>
            </div>
            <div className="text-center">
              <div
                className={cn(
                  'text-3xl font-bold mb-1 transition-colors duration-300',
                  getSentimentColor(currentAnalysis.current_percent_of_ath)
                )}
              >
                {currentAnalysis.current_percent_of_ath.toFixed(1)}%
              </div>
              <div className="text-sm text-text-light font-medium">
                Percent of previous ATH (PoPATH)
              </div>
            </div>
            <div className="text-center">
              <div
                className={cn(
                  'text-3xl font-bold mb-1',
                  currentAnalysis.percentile_rank > 50
                    ? 'text-green-600'
                    : 'text-red-500'
                )}
              >
                {currentAnalysis.percentile_rank.toFixed(0)}%
              </div>
              <div className="text-sm text-text-light font-medium">
                of days were further from ATH
              </div>
            </div>
          </div>
        </div>
      )}
    </LoadingErrorWrapper>
  );
}
