function ChartContainer({ title, description, children, className = '' }) {
  return (
    <div className={`chart-container ${className}`}>
      {title && <div className="chart-title">{title}</div>}
      {description && <div className="chart-description">{description}</div>}
      {children}
    </div>
  );
}

export default ChartContainer;
