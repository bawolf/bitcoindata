# Bitcoin HODL Dashboard - Development Setup

This guide explains how to set up the development environment for the Bitcoin HODL difficulty dashboard, which uses React/Vite with TypeScript frontend and Tailwind CSS, paired with a Flask backend.

## Prerequisites

- **Python 3.8+** with `uv` package manager
- **Node.js 18+** with npm
- Git

## Tech Stack

### Frontend

- **React 18** - UI framework
- **TypeScript** - Type safety and better developer experience
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server
- **Plotly.js** - Interactive charts and visualizations

### Backend

- **Flask** - Python web framework
- **Python** - Data processing and API endpoints

## Quick Start

### Install Dependencies

```bash
# Install React/TypeScript dependencies
npm install

# Install Python dependencies (if not already done)
uv sync --extra web
```

### Development Mode

```bash
# Terminal 1: Start Flask API server
uv run python web_deployment_example_react.py

# Terminal 2: Start Vite dev server with TypeScript
npm run dev
```

The Vite dev server will run on `http://localhost:5173` and proxy API requests to Flask at `http://localhost:8080`.

### Production Build

```bash
# Build React app (includes TypeScript compilation)
npm run build

# Run Flask server (serves built React files)
uv run python web_deployment_example_react.py
```

## Project Structure

```
bitcoin-data/
├── src/                          # React TypeScript source files
│   ├── components/               # React components
│   │   ├── common/              # Reusable common components
│   │   │   ├── LoadingErrorWrapper.tsx
│   │   │   ├── Section.tsx
│   │   │   ├── ChartContainer.tsx
│   │   │   ├── InsightBox.tsx
│   │   │   ├── PlotlyChart.tsx
│   │   │   └── index.ts
│   │   ├── CurrentStats.tsx     # Current Bitcoin stats
│   │   ├── HardestDays.tsx      # Hardest days to HODL
│   │   ├── HistoricalChart.tsx  # Historical timeline chart
│   │   ├── DistributionChart.tsx # Distribution histogram
│   │   └── CumulativeChart.tsx  # Cumulative distribution
│   ├── hooks/                   # Custom React hooks
│   │   └── useApiData.ts        # Generic API data fetching hook
│   ├── utils/                   # Utility functions
│   │   ├── helpers.ts           # Formatting helpers
│   │   └── chartStyles.ts       # Chart colors and styling utilities
│   ├── types/                   # TypeScript type definitions
│   │   ├── index.ts             # Main type definitions
│   │   └── plotly.d.ts          # Plotly.js type declarations
│   ├── App.tsx                  # Main React component
│   ├── main.tsx                 # React entry point
│   └── index.css                # Global styles with Tailwind directives
├── static/                      # Flask static files
│   └── dist/                    # Vite build output (created by npm run build)
├── package.json                 # React/Vite/TypeScript dependencies
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── vite.config.js              # Vite configuration with path aliases
├── index.html                  # React app entry point
├── web_deployment_example_react.py  # Flask app with React support
└── web_deployment_example.py        # Original Flask app
```

## Available Scripts

### Frontend (npm)

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production (includes TypeScript compilation)
- `npm run preview` - Preview production build locally
- `npm run type-check` - Run TypeScript type checking without emitting files

### Backend (uv)

- `uv run python web_deployment_example_react.py` - Start Flask dev server
- `uv sync` - Install/update Python dependencies

## TypeScript Features

### Type Safety

- **API Response Types:** Strongly typed API responses and data structures
- **Component Props:** Type-safe component props and state
- **Custom Hooks:** Generic hooks with type parameters
- **Chart Data:** Typed Plotly.js configurations and data

### Path Aliases

TypeScript is configured with path aliases for clean imports:

```typescript
import useApiData from '@/hooks/useApiData';
import { CurrentAnalysis } from '@/types';
import { COLORS } from '@/utils/chartStyles';
```

### IDE Integration

- Full IntelliSense and autocomplete
- Real-time error highlighting
- Refactoring support
- Go-to-definition navigation

## Tailwind CSS Features

### Custom Design System

Tailwind is configured with Bitcoin-themed colors and utilities:

```javascript
colors: {
  bitcoin: {
    orange: '#F7931A',
    'orange-light': 'rgba(247, 147, 26, 0.1)',
  },
  text: {
    dark: '#2c3e50',
    light: '#7f8c8d',
  },
}
```

### Component Classes

CSS classes are organized in `@layer components` for maintainability:

- `.essay-container` - Main layout wrapper
- `.hero` - Hero section styling
- `.current-stats` - Statistics grid styling
- `.day-item` - Interactive day item cards

### Responsive Design

Built-in responsive utilities for all screen sizes:

```css
@apply text-5xl md:text-6xl /* Responsive text sizing */
@apply grid grid-cols-2 md:grid-cols-4; /* Responsive grid layouts */
```

## Component Architecture

The app uses a clean, typed component architecture:

### Common Components (TypeScript)

- **LoadingErrorWrapper:** Generic loading and error state handler
- **Section:** Layout component with optional titles
- **ChartContainer:** Chart wrapper with titles and descriptions
- **InsightBox:** Highlighted content boxes
- **PlotlyChart:** Typed Plotly.js wrapper

### Feature Components (TypeScript)

- **CurrentStats:** Real-time Bitcoin metrics display
- **HardestDays:** Historical difficulty rankings
- **HistoricalChart:** Time series visualization
- **DistributionChart:** Statistical distribution analysis
- **CumulativeChart:** Percentile ranking visualization

### Custom Hooks

- **useApiData<T>:** Generic typed API data fetching hook
- Automatic loading states, error handling, and retries
- Type-safe data returned based on endpoint

### Utilities

- **chartStyles:** Consistent chart colors and configurations
- **helpers:** Formatting and utility functions
- All utilities are fully typed with TypeScript

## Development Workflow

### Hot Reload & Type Checking

- **Frontend:** Vite provides instant hot reload for React components
- **TypeScript:** Real-time type checking and IntelliSense
- **Tailwind:** CSS classes are processed and optimized automatically
- **Backend:** Flask runs in debug mode with auto-reload on file changes

### API Proxy

The Vite dev server is configured to proxy API requests to Flask:

- Frontend requests to `/api/*` → Flask server at `http://localhost:8080`
- This allows seamless development without CORS issues

1. **API Development**: Make changes to Flask backend, server restarts automatically
2. **Frontend Development**: Make changes to React components, Vite provides hot reload with TypeScript checking
3. **Type Safety**: TypeScript catches errors at compile time
4. **Styling**: Tailwind provides consistent, responsive styling with utility classes

## Benefits of This Setup

- **Type Safety**: TypeScript prevents runtime errors and improves code quality
- **Consistent Styling**: Tailwind provides a unified design system
- **Hot Reload**: Changes to React components update instantly
- **Component Structure**: Better code organization with typed React components
- **Modern Tooling**: Vite + TypeScript provide excellent dev experience
- **Bundle Optimization**: Vite automatically optimizes the production build
- **API Separation**: Clean separation between frontend and backend
- **Error Boundaries**: Robust error handling prevents complete app crashes
- **Individual Component Loading**: Each chart loads independently with proper loading states
- **Reusable Components**: Components can be easily reused or modified

## API Endpoints

The Flask backend provides these REST endpoints:

- `/api/current-analysis` - Current Bitcoin metrics and analysis
- `/api/hardest-days` - Historical hardest days to HODL
- `/api/historical-data` - Time series data for charts
- `/api/distribution-histogram` - Distribution and statistical data

All API responses are strongly typed with TypeScript interfaces.

## Troubleshooting

### TypeScript Errors

- Run `npm run type-check` to see all TypeScript errors
- Check that all imports use correct paths (`@/` aliases)
- Ensure all API responses match defined interfaces

### Tailwind Issues

- Verify `tailwind.config.js` content paths include all source files
- Check that PostCSS is processing Tailwind directives
- Ensure custom classes are defined in `@layer components`

### Port Conflicts

- Flask runs on port 8080 (configurable via `PORT` env var)
- Vite dev server runs on port 5173
- Make sure these ports are available

### API Connection Issues

- Verify Flask server is running on port 8080
- Check Vite proxy configuration in `vite.config.js`
- Ensure no firewall blocking localhost connections

### Build Issues

- Clear `node_modules` and run `npm install` again
- Check Node.js and TypeScript version compatibility
- Verify all dependencies are properly installed
- Run `npm run type-check` before building

## Production Deployment

The production deployment process remains the same - Docker will build both the React app and serve it through Flask:

```bash
# Update your Dockerfile to include React build step
FROM node:18 AS frontend
WORKDIR /app
COPY package*.json ./
COPY tsconfig*.json ./
COPY tailwind.config.js postcss.config.js ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
# Copy built React files
COPY --from=frontend /app/static/dist ./static/dist
COPY . .
RUN uv sync --extra web
CMD .venv/bin/gunicorn web_deployment_example_react:app
```
