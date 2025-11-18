export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingSpinner({ size = 'md', className = '' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div
        className={`${sizeClasses[size]} border-4 border-primary/30 border-t-primary rounded-full animate-spin`}
      ></div>
    </div>
  );
}

export function LoadingSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="bg-slate-800 rounded-2xl overflow-hidden">
            <div className="h-80 bg-slate-700"></div>
            <div className="p-5 space-y-3">
              <div className="h-6 bg-slate-700 rounded w-3/4"></div>
              <div className="h-4 bg-slate-700 rounded w-1/2"></div>
              <div className="h-16 bg-slate-700 rounded"></div>
              <div className="h-10 bg-slate-700 rounded"></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
