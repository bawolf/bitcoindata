import { LoadingErrorWrapper } from '@/components/common';
import { formatToK } from '@/utils/helpers';
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
        <div className="current-stats">
          <p>
            As of today, here's where Bitcoin stands in the emotional difficulty
            spectrum:
          </p>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-value">
                {currentAnalysis.current_distance_from_ath.toFixed(1)}%
              </div>
              <div className="stat-label">Distance from ATH</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">
                ${formatToK(currentAnalysis.current_price)}
              </div>
              <div className="stat-label">Current Price</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">
                ${formatToK(currentAnalysis.dollar_difference_from_ath)}
              </div>
              <div className="stat-label">Dollars Below ATH</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">
                {currentAnalysis.percentile_rank.toFixed(0)}%
              </div>
              <div className="stat-label">
                of days are harder to hold than today
              </div>
            </div>
          </div>
        </div>
      )}
    </LoadingErrorWrapper>
  );
}
