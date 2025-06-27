import type { LoadingErrorWrapperProps } from '@/types';

export default function LoadingErrorWrapper({
  loading,
  error,
  loadingMessage = 'Loading...',
  errorMessage = 'Failed to load data',
  children,
}: LoadingErrorWrapperProps) {
  if (loading) {
    return (
      <div className="text-center py-16 px-5 text-text-light text-lg">
        {loadingMessage}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 text-center py-10 px-5 bg-red-50 rounded-lg border border-red-200 my-5">
        <p>{errorMessage}</p>
        <p className="text-sm opacity-75">{error}</p>
      </div>
    );
  }

  return <>{children}</>;
}
