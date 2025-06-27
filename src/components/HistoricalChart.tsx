import {
  ChartContainer,
  PlotlyChart,
  LoadingErrorWrapper,
} from '@/components/common';
import useApiData from '@/hooks/useApiData';
import {
  COLORS,
  getResponsiveLayoutNoLegend,
  HOVER_TEMPLATES,
} from '@/utils/chartStyles';
import type { HistoricalData } from '@/types';

export default function HistoricalChart() {
  const { data, loading, error } = useApiData<HistoricalData>(
    '/api/historical-data?days=-1'
  );

  return (
    <ChartContainer title="Percent of Previous All Time High Over Time (All Data)">
      <LoadingErrorWrapper
        loading={loading}
        error={error}
        loadingMessage="Loading historical data..."
      >
        {data && (
          <PlotlyChart
            data={[
              {
                x: data.dates,
                y: data.percentages,
                type: 'scatter',
                mode: 'lines',
                name: 'Percent of ATH',
                line: { color: COLORS.bitcoinOrange, width: 2 },
                fill: 'tonexty',
                fillcolor: COLORS.bitcoinOrangeLight,
                hovertemplate: HOVER_TEMPLATES.percentage,
              },
            ]}
            layout={{
              ...getResponsiveLayoutNoLegend({
                xaxis: { title: 'Date', showgrid: false },
                yaxis: {
                  title: 'Percent of ATH (%)',
                  range: [0, 105],
                  showgrid: true,
                  gridcolor: COLORS.gridColor,
                },
              }),
              showlegend: false,
            }}
          />
        )}
      </LoadingErrorWrapper>
    </ChartContainer>
  );
}
