import type { InsightBoxProps } from '@/types';

export default function InsightBox({
  title,
  icon,
  children,
  className = '',
}: InsightBoxProps) {
  return (
    <div className={`insight-box ${className}`}>
      {title && (
        <h4 className="insight-title">
          {icon && <span className="mr-2">{icon}</span>}
          {title}
        </h4>
      )}
      {children}
    </div>
  );
}
