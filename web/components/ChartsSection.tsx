"use client";
import React from "react";

type Props = {
  clusterBreakdown?: Record<string, number>;
  processingBreakdown?: Record<string, number>;
};

export default function ChartsSection({
  clusterBreakdown = {},
  processingBreakdown = {},
}: Props) {
  const [visible, setVisible] = React.useState(false);

  React.useEffect(() => {
    if (
      Object.keys(clusterBreakdown).length > 0 ||
      Object.keys(processingBreakdown).length > 0
    ) {
      const t = setTimeout(() => setVisible(true), 80);
      return () => clearTimeout(t);
    }
    setVisible(false);
  }, [clusterBreakdown, processingBreakdown]);
  return (
    <section className="h-full text-white">
      <h2 className="text-xl font-medium mb-6 border-b border-white/10 pb-2">Breakdown</h2>

      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-medium text-white/60 mb-3 uppercase tracking-wider">By Health Persona</h3>
          <ul className="space-y-3">
            {Object.entries(clusterBreakdown).length === 0 && (
              <li className="text-white/40 italic text-sm">No data available</li>
            )}
            {Object.entries(clusterBreakdown).map(([label, share], i) => (
              <li
                key={label}
                className={`transition-all duration-500 ${visible ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-3"
                  }`}
                style={{ transitionDelay: `${i * 80}ms` }}
              >
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="text-white/90">{label}</span>
                  <span className="font-mono text-[var(--accent-primary)]">{(share * 100).toFixed(0)}%</span>
                </div>
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-[var(--accent-primary)] transition-all duration-1000 ease-out"
                    style={{
                      width: `${Math.round(share * 100)}%`,
                      transitionDelay: `${i * 80 + 80}ms`,
                    }}
                  />
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-medium text-white/60 mb-3 uppercase tracking-wider">By Processing Level</h3>
          <ul className="space-y-3">
            {Object.entries(processingBreakdown).length === 0 && (
              <li className="text-white/40 italic text-sm">No data available</li>
            )}
            {Object.entries(processingBreakdown).map(([label, share], i) => (
              <li
                key={label}
                className={`transition-all duration-500 ${visible ? "opacity-100 translate-x-0" : "opacity-0 -translate-x-3"
                  }`}
                style={{ transitionDelay: `${i * 80}ms` }}
              >
                <div className="flex justify-between text-sm mb-1.5">
                  <span className="text-white/90">{label}</span>
                  <span className="font-mono text-[var(--accent-secondary)]">{(share * 100).toFixed(0)}%</span>
                </div>
                <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-[var(--accent-secondary)] transition-all duration-1000 ease-out"
                    style={{
                      width: `${Math.round(share * 100)}%`,
                      transitionDelay: `${i * 80 + 80}ms`,
                    }}
                  />
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
