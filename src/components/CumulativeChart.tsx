import {
  ChartContainer,
  PlotlyChart,
  LoadingErrorWrapper,
} from '@/components/common';
import useApiData from '@/hooks/useApiData';
import {
  COLORS,
  getResponsiveLayoutNoLegend,
  LINE_STYLES,
  HOVER_TEMPLATES,
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
      title="Cumulative Distribution of Percent of All-Time High"
      description="The percentage of days bitcoin was valued at or below a given percent of all-time high."
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
                x: data.cumulative.percentages,
                y: data.cumulative.cumulative_percentages,
                type: 'scatter',
                mode: 'lines',
                name: 'Cumulative %',
                line: { color: COLORS.bitcoinOrange, width: 3 },
                fill: 'tonexty',
                fillcolor: COLORS.bitcoinOrangeLight,
                hovertemplate: HOVER_TEMPLATES.cumulativeFlipped,
              },
              ...(currentAnalysis
                ? [
                    // Today's vertical line
                    {
                      x: [
                        currentAnalysis.current_percent_of_ath,
                        currentAnalysis.current_percent_of_ath,
                      ],
                      y: [0, 100],
                      type: 'scatter',
                      mode: 'lines',
                      name: 'Today',
                      line: { ...LINE_STYLES.dashed, color: COLORS.red },
                      showlegend: false,
                      hovertemplate: `Today Bitcoin is at ${currentAnalysis.current_percent_of_ath.toFixed(
                        1
                      )}% of ATH.<br>${currentAnalysis.percentile_rank.toFixed(
                        1
                      )}% of days have been at this level or worse.<extra></extra>`,
                    },
                    // Today's marker
                    {
                      x: [currentAnalysis.current_percent_of_ath],
                      y: [currentAnalysis.percentile_rank],
                      type: 'scatter',
                      mode: 'markers',
                      name: 'Today',
                      marker: { color: COLORS.red, size: 12, symbol: 'circle' },
                      hovertemplate: `Today Bitcoin is at ${currentAnalysis.current_percent_of_ath.toFixed(
                        1
                      )}% of ATH.<br>${currentAnalysis.percentile_rank.toFixed(
                        1
                      )}% of days have been at this level or worse.<extra></extra>`,
                    },
                  ]
                : []),
            ]}
            layout={getResponsiveLayoutNoLegend({
              xaxis: { title: 'Percent of ATH (%)', showgrid: false },
              yaxis: {
                title: 'Percentage of Days (%)',
                range: [0, 105],
                showgrid: true,
                gridcolor: COLORS.gridColor,
              },
              showlegend: false,
            })}
          />
        )}
      </LoadingErrorWrapper>
    </ChartContainer>
  );
}
