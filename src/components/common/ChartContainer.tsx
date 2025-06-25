import type { ChartContainerProps } from '@/types';

export default function ChartContainer({
  title,
  description,
  children,
  className = '',
}: ChartContainerProps) {
  return (
    <div className={`chart-container ${className}`}>
      {title && <div className="chart-title">{title}</div>}
      {description && <div className="chart-description">{description}</div>}
      {children}
    </div>
  );
}
