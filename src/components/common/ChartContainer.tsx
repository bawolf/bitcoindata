import { cn } from '@/utils/cn';
import type { ChartContainerProps } from '@/types';

export default function ChartContainer({
  title,
  description,
  children,
  className = '',
}: ChartContainerProps) {
  return (
    <div
      className={cn(
        'bg-card-bg rounded-xl p-4 md:p-8 my-6 md:my-10 shadow-card border border-card-border flex flex-col gap-4',
        className
      )}
    >
      {title && (
        <div className="text-lg md:text-xl font-semibold mb-2 md:mb-4 text-text-dark">
          {title}
        </div>
      )}
      {description && (
        <div className="text-sm md:text-base text-text-light mb-4 md:mb-6 leading-relaxed">
          {description}
        </div>
      )}
      {children}
    </div>
  );
}
