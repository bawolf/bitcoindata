import { useState, useEffect } from 'react';
import type { UseApiDataReturn, ApiResponse } from '@/types';

function useApiData<T>(
  url: string,
  dependencies: unknown[] = []
): UseApiDataReturn<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = () => {
    if (!url) return;

    setLoading(true);
    setError(null);

    fetch(url)
      .then((res) => res.json())
      .then((result: ApiResponse<T>) => {
        if (result.success) {
          setData(result.data || null);
        } else {
          throw new Error(result.error || 'API request failed');
        }
      })
      .catch((err: Error | unknown) => {
        const errorMessage =
          err instanceof Error ? err.message : 'Network error occurred';
        setError(errorMessage);
      })
      .finally(() => setLoading(false));
  };

  useEffect(refetch, [url, ...dependencies]);

  return { data, loading, error, refetch };
}

export default useApiData;
