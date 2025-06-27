import { useEffect } from 'react';
import useApiData from '@/hooks/useApiData';
import { getSentimentWord } from '@/utils';
import type { CurrentAnalysis, HardestDaysData } from '@/types';

// Common components
import { InsightBox, Section } from '@/components/common';

// Feature components
import CurrentStats from '@/components/CurrentStats';
import HardestDaysTable from '@/components/HardestDaysTable';
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
    <div className="max-w-4xl mx-auto px-5 py-10">
      <div className="text-center mb-10 py-10">
        <h1 className="text-5xl md:text-6xl font-bold text-text-dark mb-5 leading-tight">
          How Hard Is It to{' '}
          <span className="font-semibold bg-gradient-to-r from-yellow-400 via-orange-500 to-blue-600 bg-clip-text text-transparent">
            HODL
          </span>
          ?
        </h1>
        <p className="text-xl text-text-light max-w-2xl mx-auto">
          Measuring the emotional rollercoaster of holding Bitcoin over the
          years
        </p>
      </div>

      <Section>
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          Bitcoin is famously volatile and trades 24/7, with occasional meteoric
          rises that have changed people's lives. It's the perfect storm for
          stress and anxiety. I wanted to understand the <em>emotional</em>{' '}
          difficulty of holding Bitcoin, so I explored a simple metric:{' '}
          <strong>
            what percentage of the previous all-time high is Bitcoin trading at
            on any given day?
          </strong>
        </p>

        <div className="bg-gray-50 border-l-4 border-bitcoin-orange p-6 my-8 rounded-r-lg">
          <div className="text-center">
            <div className="text-xl font-bold mb-4 text-gray-800">
              Percent of Previous ATH (PoPATH)
            </div>
            <div className="flex items-center justify-center gap-4 text-lg mb-4">
              <span className="font-semibold text-gray-800">PoPATH =</span>
              <div className="flex flex-col items-center">
                <div className="px-4 py-2 border-b-2 border-gray-800 font-mono text-base">
                  Day's High
                </div>
                <div className="px-4 py-2 font-mono text-base">ATH on Date</div>
              </div>
              <span className="font-semibold text-gray-800">× 100</span>
            </div>
          </div>
          <div className="text-sm text-gray-600 leading-relaxed">
            Where "ATH on Date" is the highest price Bitcoin had ever been from
            the vantage point of that day.
          </div>
        </div>

        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          I assumed that like me, most people anchor their mental value of
          Bitcoin to the all-time high when thinking about their investment,
          even if the asset was only valued at that number for days or even
          hours, and only a minimal amount of volume actually changed hands.
        </p>
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          When the current value is close to the all-time high, you feel good!
          After all, you can sell your stash for roughly what you believe it to
          be worth. And why not hold on longer? Maybe you'll find out it's even
          worth more! Whereas when the current value is comparatively low, you
          feel bad because you could have sold it for more. The lower it goes,
          the worse you feel.
        </p>

        <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
          <p className="text-sm text-gray-700 leading-relaxed">
            <strong>Disclaimers:</strong> None of this is financial advice. You
            probably shouldn't use it to trade. Bitcoin might go up, it might
            also go down. I hold some Bitcoin.
          </p>
        </div>
      </Section>

      <Section title="How Hard is it to Hold Today?">
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          Based on today's price relative to Bitcoin's historical all-time high,
          we can get a sense of where we are in the emotional cycle of holding.
        </p>
        {currentAnalysis?.current_percent_of_ath && (
          <p className="text-xl mb-5 font-semibold text-center p-4 bg-gray-50 rounded-lg">
            Today is a{' '}
            {getSentimentWord(currentAnalysis.current_percent_of_ath)} day to
            hold Bitcoin.
          </p>
        )}
        <CurrentStats
          currentAnalysis={currentAnalysis}
          loading={analysisLoading}
          error={analysisError}
        />
      </Section>

      <Section title="The Hardest Days to HODL">
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          Out of the {hardestDays && hardestDays.total_days.toLocaleString()}{' '}
          days since my datasets began on{' '}
          {hardestDays &&
            new Date(hardestDays.first_date).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          , these are the ten days that Bitcoin was the furthest from its
          all-time high. Most of the top 100 are all from late 2011 to early
          2012 back when trading was mostly done on Mt. Gox.
        </p>
        <HardestDaysTable
          hardestDays={hardestDays}
          loading={hardestLoading}
          error={hardestError}
        />
        {hardestDays && (
          <InsightBox title="🎉 The Easy Days">
            <p>
              On the lighter side, there were {hardestDays.easy_days_count} days
              ({hardestDays.easy_days_percentage.toFixed(1)}%) since{' '}
              {new Date(hardestDays.first_date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}{' '}
              that Bitcoin hit a new all-time high.
            </p>
          </InsightBox>
        )}
      </Section>

      <Section title="The Emotional Journey Over Time">
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          In this chart of PoPATH over time, you can see clusters at the top
          where it felt good to hold, extended dips where it felt bad, and some
          spiky periods where it was an emotionally volatile rollercoaster. It
          does appear that the drops are getting less extreme percentage-wise.
          The difference in experience between a 75% drop (Nov 2022) and a 93%
          drop (Nov 2011) is that a 93% drop is your investment dropping by 75%,
          then that remaining amount dropping by 75% again.
        </p>
        <HistoricalChart />
      </Section>

      <Section title="When Up Feels Down">
        <DistributionChart currentAnalysis={currentAnalysis} />
      </Section>

      <Section title="Position in the Emotional Cycle">
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          The cumulative version of the distribution chart seems to capture the
          current position in the emotional cycle. Space to the right of the
          line represents the number of days that feel better than today, and
          space to the left represents the number of days that feel worse.
        </p>
        <CumulativeChart currentAnalysis={currentAnalysis} />
      </Section>

      <Section>
        <h3 className="text-2xl font-semibold mb-4 text-text-dark">
          Conclusion
        </h3>
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          Hindsight is 20/20. We can look back and with the knowledge that the
          toughest days to hold Bitcoin were actually the best times to buy the
          dip, but in real time, that decision isn't easy.
        </p>
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          There were moments where it wasn't clear that Bitcoin would continue
          to exist at all, let alone return to its prior heights. The regret of
          not selling can be just as painful as the regret of not buying, and
          from that standpoint, despite being the best performing asset in
          history, most of the time Bitcoin holders are feeling like they missed
          out on a great time to sell.
        </p>
      </Section>

      <div className="text-center text-text-light text-sm mt-10 pt-5 border-t border-card-border">
        Last updated: {new Date().toLocaleString()}
      </div>
    </div>
  );
}

export default App;
