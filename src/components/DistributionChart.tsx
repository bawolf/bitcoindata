import {
  ChartContainer,
  PlotlyChart,
  LoadingErrorWrapper,
} from '@/components/common';
import useApiData from '@/hooks/useApiData';
import {
  COLORS,
  getResponsiveLayout,
  HOVER_TEMPLATES,
} from '@/utils/chartStyles';
import type { DistributionData, CurrentAnalysis } from '@/types';

interface DistributionChartProps {
  currentAnalysis?: CurrentAnalysis | null;
}

export default function DistributionChart({
  currentAnalysis,
}: DistributionChartProps) {
  const { data, loading, error } = useApiData<DistributionData>(
    '/api/distribution-histogram'
  );

  // Custom layout for distribution chart with extra spacing for legend
  const getDistributionLayout = (baseLayout: any = {}) => {
    const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
    const responsiveLayout = getResponsiveLayout(baseLayout);

    // Position legend below the chart for both mobile and desktop
    if (isMobile) {
      // Mobile: Extra space for legend
      responsiveLayout.margin = { t: 20, r: 10, b: 120, l: 50 };
      responsiveLayout.legend = {
        x: 0.5,
        y: -0.25, // Below the chart
        xanchor: 'center',
        orientation: 'h',
      };
    } else {
      // Desktop: Position legend below the chart
      responsiveLayout.margin = { t: 20, r: 20, b: 100, l: 60 }; // Increased bottom margin
      responsiveLayout.legend = {
        x: 0.5,
        y: -0.25, // Below the chart
        xanchor: 'center',
        orientation: 'h',
      };
    }

    return responsiveLayout;
  };

  const medianPercent = data?.statistics.median_percent.toFixed(1);

  return (
    <LoadingErrorWrapper
      loading={loading}
      error={error}
      loadingMessage="Loading distribution data..."
    >
      {data && (
        <p className="text-lg mb-5 text-text-dark leading-relaxed">
          While the chart above shows the story of the emotional moments over
          time, the histogram captures the overall vibe. On the median day,
          Bitcoin is at {medianPercent}% of its previous all-time high. This
          means for half of all days, holders have been staring at a price
          that's only {medianPercent}% of what they could have sold for at some
          point earlier.
        </p>
      )}
      <ChartContainer title="Distribution of Percent of All-Time High">
        {data && (
          <>
            <PlotlyChart
              data={[
                {
                  x: data.histogram.bins,
                  y: data.histogram.counts,
                  type: 'bar',
                  name: 'Distribution',
                  marker: { color: COLORS.bitcoinOrange },
                  hovertemplate: HOVER_TEMPLATES.count,
                },
                // Median line
                {
                  x: [
                    data.statistics.median_percent,
                    data.statistics.median_percent,
                  ],
                  y: [0, Math.max(...data.histogram.counts)],
                  type: 'scatter',
                  mode: 'lines',
                  name: 'Median',
                  line: { color: COLORS.purple, width: 3, dash: 'dash' },
                  hovertemplate: `Median: ${data.statistics.median_percent.toFixed(
                    1
                  )}%<extra></extra>`,
                  showlegend: false,
                },
                // Median marker at top for hover
                {
                  x: [data.statistics.median_percent],
                  y: [Math.max(...data.histogram.counts) * 1.05],
                  type: 'scatter',
                  mode: 'markers',
                  name: 'Median',
                  marker: {
                    color: COLORS.purple,
                    size: 12,
                    symbol: 'triangle-down',
                  },
                  hovertemplate: `Median: ${data.statistics.median_percent.toFixed(
                    1
                  )}%<extra></extra>`,
                },
                // Mean line
                {
                  x: [
                    data.statistics.mean_percent,
                    data.statistics.mean_percent,
                  ],
                  y: [0, Math.max(...data.histogram.counts)],
                  type: 'scatter',
                  mode: 'lines',
                  name: 'Mean',
                  line: { color: COLORS.gray, width: 3, dash: 'dot' },
                  hovertemplate: `Mean: ${data.statistics.mean_percent.toFixed(
                    1
                  )}%<extra></extra>`,
                  showlegend: false,
                },
                // Mean marker at top for hover
                {
                  x: [data.statistics.mean_percent],
                  y: [Math.max(...data.histogram.counts) * 1.05],
                  type: 'scatter',
                  mode: 'markers',
                  name: 'Mean',
                  marker: {
                    color: COLORS.gray,
                    size: 12,
                    symbol: 'triangle-down',
                  },
                  hovertemplate: `Mean: ${data.statistics.mean_percent.toFixed(
                    1
                  )}%<extra></extra>`,
                },
                // Current day marker (if available)
                ...(currentAnalysis
                  ? [
                      {
                        x: [
                          currentAnalysis.current_percent_of_ath,
                          currentAnalysis.current_percent_of_ath,
                        ],
                        y: [0, Math.max(...data.histogram.counts)],
                        type: 'scatter',
                        mode: 'lines',
                        name: 'Today',
                        line: { color: COLORS.red, width: 4 },
                        hovertemplate: `Today: ${currentAnalysis.current_percent_of_ath.toFixed(
                          1
                        )}%<extra></extra>`,
                        showlegend: false,
                      },
                      {
                        x: [currentAnalysis.current_percent_of_ath],
                        y: [Math.max(...data.histogram.counts) * 1.05],
                        type: 'scatter',
                        mode: 'markers',
                        name: 'Today',
                        marker: {
                          color: COLORS.red,
                          size: 12,
                          symbol: 'triangle-down',
                        },
                        hovertemplate: `Today: ${currentAnalysis.current_percent_of_ath.toFixed(
                          1
                        )}%<extra></extra>`,
                      },
                    ]
                  : []),
              ]}
              layout={getDistributionLayout({
                xaxis: { title: 'Percent of ATH (%)', showgrid: false },
                yaxis: {
                  title: 'Number of Days',
                  showgrid: true,
                  gridcolor: COLORS.gridColor,
                },
                showlegend: true,
              })}
            />
          </>
        )}
      </ChartContainer>
    </LoadingErrorWrapper>
  );
}
