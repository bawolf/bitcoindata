import { LoadingErrorWrapper, InsightBox } from '@/components/common';
import { formatDate } from '@/utils/helpers';
import type { HardestDaysProps } from '@/types';

export default function HardestDays({
  hardestDays,
  loading,
  error,
}: HardestDaysProps) {
  return (
    <LoadingErrorWrapper
      loading={loading}
      error={error}
      loadingMessage="Loading hardest days..."
    >
      {hardestDays && (
        <>
          <div className="hardest-days">
            {hardestDays.hardest_days.map((day, index) => (
              <div key={day.date} className="day-item">
                <div className="day-info">
                  <div className="day-rank">#{index + 1}</div>
                  <div className="day-date">{formatDate(day.date)}</div>
                  <div className="day-price">
                    Price: ${day.price.toLocaleString()}
                  </div>
                </div>
                <div className="day-loss">
                  <div className="day-loss-pct">
                    {day.distance_pct.toFixed(1)}% down
                  </div>
                  <div className="day-loss-dollars">
                    -${day.dollar_loss.toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <InsightBox title="🎉 The Easy Days">
            <p>
              Out of {hardestDays.total_days.toLocaleString()} days in our
              dataset, only {hardestDays.easy_days_count} days (
              {hardestDays.easy_days_percentage.toFixed(1)}%) were "easy" days
              where Bitcoin hit a new all-time high. On these days, HODLers felt
              like absolute geniuses.
            </p>
          </InsightBox>
        </>
      )}
    </LoadingErrorWrapper>
  );
}
