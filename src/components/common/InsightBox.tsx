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
      className={cn(
        'bg-blue-50 border border-blue-200 p-4 rounded-lg',
        className
      )}
    >
      {title && (
        <h4 className="text-lg font-semibold mb-3 text-gray-800">
          {icon && <span className="mr-2">{icon}</span>}
          {title}
        </h4>
      )}
      <div className="text-gray-700 leading-relaxed">{children}</div>
    </div>
  );
}
