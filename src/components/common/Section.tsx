import type { SectionProps } from '@/types';

export default function Section({
  title,
  children,
  className = '',
}: SectionProps) {
  return (
    <div className={`section ${className}`}>
      {title && <h2 className="section-title">{title}</h2>}
      {children}
    </div>
  );
}
