import { useEffect } from 'react';
import useApiData from '@/hooks/useApiData';
import type { CurrentAnalysis, HardestDaysData } from '@/types';

// Common components
import { Section } from '@/components/common';

// Feature components
import CurrentStats from '@/components/CurrentStats';
import HardestDays from '@/components/HardestDays';
import HistoricalChart from '@/components/HistoricalChart';
import DistributionChart from '@/components/DistributionChart';
import CumulativeChart from '@/components/CumulativeChart';

function App() {
  const {
    data: currentAnalysis,
    loading: analysisLoading,
    error: analysisError,
  } = useApiData<CurrentAnalysis>('/api/current-analysis');

  const {
    data: hardestDays,
    loading: hardestLoading,
    error: hardestError,
  } = useApiData<HardestDaysData>('/api/hardest-days');

  // Auto-refresh every 5 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      window.location.reload();
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="essay-container">
      <div className="hero">
        <h1>
          How Hard Is It to <span className="highlight">HODL</span>?
        </h1>
        <p className="subtitle">
          An exploration of the emotional rollercoaster of holding Bitcoin
          through market cycles
        </p>
      </div>

      <Section>
        <p>
          Bitcoin's price chart is notorious for its dramatic peaks and valleys.
          But behind every red candle is a human story—someone staring at their
          portfolio, questioning their decisions, fighting the urge to sell.
        </p>

        <p>
          To understand the <em>emotional</em> difficulty of holding Bitcoin,
          I've developed a simple metric:{' '}
          <strong>
            how far is Bitcoin from its all-time high on any given day?
          </strong>
        </p>

        <div className="metric-formula">
          <strong>
            Distance from ATH = (Last ATH - Today's High) / Last ATH × 100
          </strong>
          <br />
          <br />
          Where "Last ATH" is the most recent all-time high as of that day, not
          today's ATH looking backward.
        </div>

        <p>
          This tells us something crucial: on days when this number is high,
          HODLers are staring at serious paper losses. These are the days that
          test your conviction, the days you question everything.
        </p>
      </Section>

      <Section title="Right Now: How Hard Is It?">
        <CurrentStats
          currentAnalysis={currentAnalysis}
          loading={analysisLoading}
          error={analysisError}
        />
      </Section>

      <Section title="The Hardest Days to HODL">
        <p>
          Some days are harder than others. These were the five most emotionally
          challenging days in Bitcoin's history—the days when HODLers were truly
          tested:
        </p>
        <HardestDays
          hardestDays={hardestDays}
          loading={hardestLoading}
          error={hardestError}
        />
      </Section>

      <Section title="The Emotional Journey Over Time">
        <p>
          Here's Bitcoin's emotional difficulty over time. I've inverted the
          chart so that <strong>higher numbers mean it's easier to HODL</strong>{' '}
          (you're closer to ATH and feeling good), while lower numbers mean
          maximum emotional pain.
        </p>
        <HistoricalChart />
      </Section>

      <Section title="How Does It Feel to Hold Bitcoin?">
        <p>
          This is where the story gets interesting. The distribution below shows
          something remarkable about the Bitcoin holding experience.
        </p>
        <DistributionChart />
      </Section>

      <Section title="Is It Easy to HODL Right Now?">
        <p>
          This final chart answers a simple question: compared to all of
          Bitcoin's history, is today an easy day or a hard day to hold?
        </p>
        <CumulativeChart currentAnalysis={currentAnalysis} />
      </Section>

      <Section>
        <h3>The Bottom Line</h3>
        <p>
          HODLing Bitcoin isn't just about believing in the technology or the
          monetary revolution. It's about psychology, emotion, and the very
          human challenge of watching numbers go up and down while the rest of
          the world tells you you're crazy.
        </p>

        <p>
          The data shows that for the majority of Bitcoin's existence, holders
          have been underwater from the last peak. That's the reality of being
          early to a revolutionary technology. The question isn't whether it's
          hard to HODL—it's whether you can handle the emotional rollercoaster
          when others cannot.
        </p>
      </Section>

      <div className="update-time">
        Last updated: {new Date().toLocaleString()}
      </div>
    </div>
  );
}

export default App;
