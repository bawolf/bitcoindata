import { cn } from '@/utils/cn';
import type { InsightBoxProps } from '@/types';

export default function InsightBox({
  title,
  icon,
  children,
  className = '',
}: InsightBoxProps) {
  return (
    <div
      className={cn('rounded-xl p-6 border-l-4 border-green-500', className)}
      style={{
        background: 'linear-gradient(120deg, #a8e6cf 0%, #dcedc1 100%)',
      }}
    >
      {title && (
        <h4 className="text-xl font-semibold mb-3 text-text-dark">
          {icon && <span className="mr-2">{icon}</span>}
          {title}
        </h4>
      )}
      <div className="mb-0 text-text-dark">{children}</div>
    </div>
  );
}
