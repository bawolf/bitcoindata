/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bitcoin: {
          orange: '#F7931A',
          'orange-light': 'rgba(247, 147, 26, 0.1)',
          'orange-dark': '#E6851F',
        },
        text: {
          dark: '#2c3e50',
          light: '#7f8c8d',
        },
        background: '#fefefe',
        card: {
          bg: '#ffffff',
          border: '#e8ecef',
        },
      },
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: ['SF Mono', 'Monaco', 'monospace'],
      },
      boxShadow: {
        card: '0 4px 20px rgba(0,0,0,0.08)',
        'day-item': '0 4px 12px rgba(231, 76, 60, 0.15)',
      },
      gradients: {
        insight: 'linear-gradient(120deg, #a8e6cf 0%, #dcedc1 100%)',
        highlight: 'linear-gradient(120deg, #ffd89b 0%, #19547b 100%)',
        'day-item': 'linear-gradient(135deg, #fff5f5 0%, #fef2f2 100%)',
      },
      spacing: {
        18: '4.5rem',
        22: '5.5rem',
      },
    },
  },
  plugins: [],
};
