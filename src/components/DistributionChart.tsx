import {
  ChartContainer,
  PlotlyChart,
  LoadingErrorWrapper,
  InsightBox,
} from '@/components/common';
import useApiData from '@/hooks/useApiData';
import {
  COLORS,
  BASE_LAYOUT,
  createVerticalLine,
  LINE_STYLES,
} from '@/utils/chartStyles';
import type { DistributionData } from '@/types';

export default function DistributionChart() {
  const { data, loading, error } = useApiData<DistributionData>(
    '/api/distribution-histogram'
  );

  return (
    <ChartContainer
      title="Distribution of HODL Difficulty"
      description="How many days Bitcoin spent at each distance from its all-time high"
    >
      <LoadingErrorWrapper
        loading={loading}
        error={error}
        loadingMessage="Loading distribution data..."
      >
        {data && (
          <>
            <PlotlyChart
              data={[
                {
                  x: data.bin_centers,
                  y: data.counts,
                  type: 'bar',
                  name: 'Days',
                  marker: { color: COLORS.bitcoinOrange, opacity: 0.8 },
                },
                createVerticalLine(
                  data.median_distance,
                  Math.max(...data.counts),
                  `Median: ${data.median_distance.toFixed(1)}%`,
                  COLORS.red,
                  LINE_STYLES.dashed
                ),
                createVerticalLine(
                  data.mean_distance,
                  Math.max(...data.counts),
                  `Mean: ${data.mean_distance.toFixed(1)}%`,
                  COLORS.green,
                  LINE_STYLES.dashed
                ),
              ]}
              layout={{
                ...BASE_LAYOUT,
                xaxis: { title: 'Distance from ATH (%)', showgrid: false },
                yaxis: { title: 'Number of Days', showgrid: true },
              }}
            />

            <InsightBox title="💡 The Uncomfortable Truth">
              <p>
                The median distance from ATH is{' '}
                <strong>{data.median_distance.toFixed(1)}%</strong> - meaning
                half of all days, holders were down this much or more. Most
                Bitcoin days are psychologically challenging!
              </p>
            </InsightBox>
          </>
        )}
      </LoadingErrorWrapper>
    </ChartContainer>
  );
}
