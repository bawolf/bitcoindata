# Component Abstractions Guide

## Overview

I've created several reusable components and utilities to eliminate code duplication and provide consistent styling across the app.

## Common Components

### 🔄 `LoadingErrorWrapper`

Handles loading and error states consistently across components.

```jsx
import { LoadingErrorWrapper } from './components/common';

<LoadingErrorWrapper
  loading={loading}
  error={error}
  loadingMessage="Loading chart data..." // optional
  errorMessage="Failed to load data" // optional
>
  {data && <YourComponent data={data} />}
</LoadingErrorWrapper>;
```

### 📦 `Section`

Provides consistent section layout with optional title.

```jsx
import { Section } from './components/common';

<Section title="Section Title" className="custom-class">
  <p>Content goes here...</p>
</Section>;
```

### 📊 `ChartContainer`

Wraps charts with consistent styling, title, and description.

```jsx
import { ChartContainer } from './components/common';

<ChartContainer
  title="Chart Title"
  description="Chart description"
  className="custom-class"
>
  <YourChart />
</ChartContainer>;
```

### 💡 `InsightBox`

Creates styled insight/callout boxes.

```jsx
import { InsightBox } from './components/common';

<InsightBox title="Key Insight" icon="💡" className="custom-class">
  <p>Your insight content...</p>
</InsightBox>;
```

### 📈 `PlotlyChart`

Wrapper for Plotly charts with consistent configuration.

```jsx
import { PlotlyChart } from './components/common';

<PlotlyChart
  data={chartData}
  layout={{
    xaxis: { title: 'X Axis' },
    yaxis: { title: 'Y Axis' },
  }}
  style={{ width: '100%', height: '400px' }}
/>;
```

### 🛡️ `ErrorBoundary`

Catches and displays React errors gracefully.

```jsx
import { ErrorBoundary } from './components/common';

<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>;
```

## Custom Hooks

### 🔌 `useApiData`

Handles API calls with loading, error, and retry functionality.

```jsx
import useApiData from './hooks/useApiData';

const { data, loading, error, refetch } = useApiData('/api/endpoint');

// With dependencies (refetch when they change)
const { data, loading, error } = useApiData('/api/data', [param1, param2]);
```

## Chart Utilities

### 🎨 `chartStyles.js`

Provides consistent colors, line styles, and chart configuration utilities.

```jsx
import {
  COLORS,
  LINE_STYLES,
  createBasicLine,
  createFilledArea,
  createVerticalLine,
  createMarker,
  createAxis,
  HOVER_TEMPLATES,
} from './utils/chartStyles';

// Use predefined colors
const trace = {
  line: { color: COLORS.bitcoinOrange },
};

// Create common chart elements
const verticalLine = createVerticalLine(
  50,
  100,
  'Median',
  COLORS.red,
  LINE_STYLES.dashed
);
const axis = createAxis('Price ($)', { range: [0, 100] });
```

Available colors:

- `COLORS.bitcoinOrange`
- `COLORS.bitcoinOrangeLight`
- `COLORS.bitcoinOrangeDark`
- `COLORS.red`
- `COLORS.green`
- `COLORS.purple`
- `COLORS.gray`
- `COLORS.gridColor`

## File Structure After Abstractions

```
src/
├── components/
│   ├── common/                 # Reusable components
│   │   ├── index.js           # Export all common components
│   │   ├── ErrorBoundary.jsx
│   │   ├── LoadingErrorWrapper.jsx
│   │   ├── Section.jsx
│   │   ├── ChartContainer.jsx
│   │   ├── InsightBox.jsx
│   │   └── PlotlyChart.jsx
│   ├── CurrentStats.jsx       # Feature components
│   ├── HardestDays.jsx
│   ├── HistoricalChart.jsx
│   ├── DistributionChart.jsx
│   └── CumulativeChart.jsx
├── hooks/
│   └── useApiData.js          # Custom hooks
├── utils/
│   ├── helpers.js             # General utilities
│   └── chartStyles.js         # Chart-specific utilities
├── App.jsx
├── main.jsx
└── index.css
```

## Benefits of These Abstractions

### 🚀 **Development Speed**

- No need to rewrite loading/error states
- Consistent chart styling with minimal code
- Easy to create new sections and insights

### 🎯 **Consistency**

- All charts look and behave the same
- Uniform error handling across the app
- Consistent spacing and styling

### 🧹 **Maintainability**

- Change colors/styles in one place
- Fix bugs once, apply everywhere
- Easy to understand component structure

### 📏 **Code Reduction**

- Original DistributionChart: ~140 lines
- Refactored DistributionChart: ~80 lines
- 43% reduction while adding more features!

## Before vs After Example

### Before (Original DistributionChart):

```jsx
// 140+ lines with repetitive patterns
function DistributionChart() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/distribution-histogram')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setData(data.data)
        } else {
          throw new Error(data.error)
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="section">
      <h2>Chart Title</h2>
      <div className="chart-container">
        <div className="chart-title">Title</div>
        <Plot data={data} layout={{...}} />
        <div className="insight-box">
          <h4>💡 Insight</h4>
          <p>Content...</p>
        </div>
      </div>
    </div>
  )
}
```

### After (Refactored):

```jsx
// 80 lines, more readable, same functionality
function DistributionChart() {
  const { data, loading, error } = useApiData('/api/distribution-histogram');

  return (
    <Section title="Chart Title">
      <ChartContainer title="Title">
        <LoadingErrorWrapper loading={loading} error={error}>
          {data && <DistributionPlot data={data} />}
        </LoadingErrorWrapper>

        {data && (
          <InsightBox title="Insight" icon="💡">
            <p>Content...</p>
          </InsightBox>
        )}
      </ChartContainer>
    </Section>
  );
}
```

## Usage Guidelines

1. **Always use common components** when available
2. **Extract new patterns** into common components when you see repetition
3. **Import from common/index.js** for cleaner imports
4. **Use chartStyles utilities** for consistent chart appearance
5. **Wrap chart sections in ErrorBoundary** for robustness

These abstractions make the codebase much more maintainable while providing the same great user experience!
