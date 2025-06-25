import {
  ChartContainer,
  PlotlyChart,
  LoadingErrorWrapper,
} from '@/components/common';
import useApiData from '@/hooks/useApiData';
import { COLORS, BASE_LAYOUT, HOVER_TEMPLATES } from '@/utils/chartStyles';
import type { HistoricalData } from '@/types';

export default function HistoricalChart() {
  const { data, loading, error } = useApiData<HistoricalData>(
    '/api/historical-data?days=-1'
  );

  return (
    <ChartContainer
      title="HODL Difficulty Over Time (All Data)"
      description="Higher values = easier to hold (closer to ATH). Lower values = maximum emotional pain."
    >
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
                y: data.distances.map((d) => 100 - d), // Invert for ease score
                type: 'scatter',
                mode: 'lines',
                name: 'HODL Ease Score',
                line: { color: COLORS.bitcoinOrange, width: 2 },
                fill: 'tonexty',
                fillcolor: COLORS.bitcoinOrangeLight,
                hovertemplate: HOVER_TEMPLATES.percentage,
              },
            ]}
            layout={{
              ...BASE_LAYOUT,
              xaxis: { title: 'Date', showgrid: false },
              yaxis: {
                title: 'HODL Ease Score (%)',
                range: [0, 105],
                showgrid: true,
                gridcolor: COLORS.gridColor,
              },
            }}
          />
        )}
      </LoadingErrorWrapper>
    </ChartContainer>
  );
}
