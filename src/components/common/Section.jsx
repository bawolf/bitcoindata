function Section({ title, children, className = '' }) {
  return (
    <div className={`section ${className}`}>
      {title && <h2>{title}</h2>}
      {children}
    </div>
  );
}

export default Section;
