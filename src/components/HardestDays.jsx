import { formatDate } from '../utils/helpers';
import Section from './common/Section';
import LoadingErrorWrapper from './common/LoadingErrorWrapper';
import InsightBox from './common/InsightBox';

function HardestDays({ hardestDays, loading, error }) {
  return (
    <Section title="The Hardest Days to HODL">
      <p>
        Some days are harder than others. These were the five most emotionally
        challenging days in Bitcoin's history—the days when HODLers were truly
        tested:
      </p>

      <LoadingErrorWrapper
        loading={loading}
        error={error}
        loadingMessage="Loading hardest days..."
        errorMessage="Failed to load hardest days"
      >
        {hardestDays && (
          <>
            <div className="hardest-days">
              {hardestDays.hardest_days.map((day, index) => (
                <HardestDayItem key={day.date} day={day} rank={index + 1} />
              ))}
            </div>

            <InsightBox title="The Easy Days" icon="🎉">
              <p>
                Out of {hardestDays.total_days.toLocaleString()} days in our
                dataset, only {hardestDays.easy_days_count} days (
                {hardestDays.easy_days_percentage.toFixed(1)}%) were "easy" days
                where Bitcoin hit a new all-time high. On these days, HODLers
                felt like absolute geniuses.
              </p>
            </InsightBox>
          </>
        )}
      </LoadingErrorWrapper>
    </Section>
  );
}

function HardestDayItem({ day, rank }) {
  return (
    <div className="day-item">
      <div className="day-info">
        <div className="day-rank">#{rank}</div>
        <div className="day-date">{formatDate(day.date)}</div>
        <div className="day-price">Price: ${day.price.toLocaleString()}</div>
      </div>
      <div className="day-loss">
        <div className="day-loss-pct">{day.distance_pct.toFixed(1)}% down</div>
        <div className="day-loss-dollars">
          -${day.dollar_loss.toLocaleString()}
        </div>
      </div>
    </div>
  );
}

export default HardestDays;
