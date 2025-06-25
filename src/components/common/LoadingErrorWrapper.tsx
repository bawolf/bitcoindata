import type { LoadingErrorWrapperProps } from '@/types';

export default function LoadingErrorWrapper({
  loading,
  error,
  loadingMessage = 'Loading...',
  errorMessage = 'Failed to load data',
  children,
}: LoadingErrorWrapperProps) {
  if (loading) {
    return <div className="loading">{loadingMessage}</div>;
  }

  if (error) {
    return (
      <div className="error">
        <p>{errorMessage}</p>
        <p className="text-sm opacity-75">{error}</p>
      </div>
    );
  }

  return <>{children}</>;
}
