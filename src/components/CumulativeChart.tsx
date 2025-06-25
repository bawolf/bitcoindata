import {
  ChartContainer,
  PlotlyChart,
  LoadingErrorWrapper,
} from '@/components/common';
import useApiData from '@/hooks/useApiData';
import {
  COLORS,
  BASE_LAYOUT,
  createVerticalLine,
  createMarker,
  LINE_STYLES,
} from '@/utils/chartStyles';
import type { DistributionData, CumulativeChartProps } from '@/types';

export default function CumulativeChart({
  currentAnalysis,
}: CumulativeChartProps) {
  const { data, loading, error } = useApiData<DistributionData>(
    '/api/distribution-histogram'
  );

  return (
    <ChartContainer
      title="Where Do We Stand?"
      description="If you're toward the left, congrats—today is relatively easy. Toward the right? You're being tested."
    >
      <LoadingErrorWrapper
        loading={loading}
        error={error}
        loadingMessage="Loading cumulative data..."
      >
        {data && (
          <PlotlyChart
            data={[
              {
                x: data.cumulative_distances,
                y: data.cumulative_percentages,
                type: 'scatter',
                mode: 'lines',
                name: 'Cumulative %',
                line: { color: COLORS.bitcoinOrange, width: 3 },
                fill: 'tonexty',
                fillcolor: COLORS.bitcoinOrangeLight,
              },
              ...(currentAnalysis
                ? [
                    createVerticalLine(
                      currentAnalysis.current_distance_from_ath,
                      100,
                      'Today',
                      COLORS.red,
                      LINE_STYLES.dashed
                    ),
                    createMarker(
                      currentAnalysis.current_distance_from_ath,
                      currentAnalysis.percentile_rank,
                      'YOU ARE HERE',
                      COLORS.red
                    ),
                  ]
                : []),
            ]}
            layout={{
              ...BASE_LAYOUT,
              xaxis: { title: 'Distance from ATH (%)', showgrid: false },
              yaxis: {
                title: 'Percentage of Days (%)',
                range: [0, 105],
                showgrid: true,
                gridcolor: COLORS.gridColor,
              },
              showlegend: false,
            }}
          />
        )}
      </LoadingErrorWrapper>
    </ChartContainer>
  );
}
