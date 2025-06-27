import { cn } from '@/utils/cn';
import type { SectionProps } from '@/types';

export default function Section({
  title,
  children,
  className = '',
}: SectionProps) {
  return (
    <div className={cn('mb-20', className)}>
      {title && (
        <h2 className="text-4xl font-semibold mb-5 text-text-dark">{title}</h2>
      )}
      {children}
    </div>
  );
}
