import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utility function to merge class names with clsx and tailwind-merge
 *
 * This function:
 * 1. Uses clsx to conditionally join classNames
 * 2. Uses tailwind-merge to intelligently merge Tailwind classes and resolve conflicts
 *
 * @param inputs - Class values (strings, objects, arrays, etc.)
 * @returns Merged and optimized class string
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
