import { LoadingErrorWrapper } from '@/components/common';
import { cn, formatCurrency } from '@/utils';
import type { HardestDaysProps } from '@/types';

export default function HardestDaysTable({
  hardestDays,
  loading,
  error,
}: HardestDaysProps) {
  return (
    <LoadingErrorWrapper
      loading={loading}
      error={error}
      loadingMessage="Loading hardest days..."
    >
      {hardestDays && (
        <div className="my-8">
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
            <table className="w-auto min-w-full">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="px-3 py-3 text-left text-xs md:text-sm font-semibold text-gray-900 whitespace-nowrap">
                    Rank
                  </th>
                  <th className="px-3 py-3 text-left text-xs md:text-sm font-semibold text-gray-900 whitespace-nowrap">
                    Date
                  </th>
                  <th className="px-3 py-3 text-right text-xs md:text-sm font-semibold text-gray-900 whitespace-nowrap">
                    Price
                  </th>
                  <th className="px-3 py-3 text-right text-xs md:text-sm font-semibold text-gray-900 whitespace-nowrap">
                    ATH
                  </th>
                  <th className="px-3 py-3 text-right text-xs md:text-sm font-semibold text-gray-900 whitespace-nowrap">
                    Loss
                  </th>
                  <th className="px-3 py-3 text-right text-xs md:text-sm font-semibold text-gray-900 whitespace-nowrap">
                    PoPATH
                  </th>
                </tr>
              </thead>
              <tbody>
                {hardestDays.hardest_days.map((day, index) => (
                  <tr
                    key={day.date}
                    className={cn(
                      'border-b border-gray-100 hover:bg-gray-50 transition-colors',
                      index === 0 && 'bg-red-50' // Highlight worst day
                    )}
                  >
                    <td className="px-3 py-3 whitespace-nowrap">
                      <div
                        className={cn(
                          'inline-flex items-center justify-center w-5 h-5 md:w-6 md:h-6 rounded-full text-xs font-bold text-white',
                          index === 0 ? 'bg-red-600' : 'bg-gray-400'
                        )}
                      >
                        {index + 1}
                      </div>
                    </td>
                    <td className="px-3 py-3 whitespace-nowrap">
                      <div className="font-medium text-gray-900 text-xs md:text-sm">
                        {new Date(day.date).toLocaleDateString('en-US', {
                          year: '2-digit',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </div>
                    </td>
                    <td className="px-3 py-3 text-right font-mono text-xs md:text-sm whitespace-nowrap">
                      {formatCurrency(day.price)}
                    </td>
                    <td className="px-3 py-3 text-right font-mono text-xs md:text-sm text-green-600 whitespace-nowrap">
                      {formatCurrency(day.ath_at_time)}
                    </td>
                    <td className="px-3 py-3 text-right font-mono text-xs md:text-sm text-red-600 whitespace-nowrap">
                      -{formatCurrency(day.dollar_loss)}
                    </td>
                    <td className="px-3 py-3 text-right font-mono text-xs md:text-sm text-red-600 whitespace-nowrap">
                      {day.percent_of_ath.toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </LoadingErrorWrapper>
  );
}
