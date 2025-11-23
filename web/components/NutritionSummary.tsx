import React, { useEffect, useState } from "react";
import type { PlanTotals, PlanCoverage } from "../types/plan";

type Props = {
  totals: PlanTotals | null;
  coverage: PlanCoverage | null;
};

export default function NutritionSummary({ totals, coverage }: Props) {
  const [dispCost, setDispCost] = useState(0);
  const [dispCalories, setDispCalories] = useState(0);
  const [dispProtein, setDispProtein] = useState(0);

  useEffect(() => {
    if (!totals) {
      setDispCost(0);
      setDispCalories(0);
      setDispProtein(0);
      return;
    }

    const duration = 700;
    const start = performance.now();
    const fromCost = dispCost;
    const fromCal = dispCalories;
    const fromProt = dispProtein;
    const targetCost = totals.cost;
    const targetCalories = totals.calories;
    const targetProtein = totals.protein;

    let raf = 0;
    function animate(now: number) {
      const t = Math.min(1, (now - start) / duration);
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // simple ease
      setDispCost(
        Math.round((fromCost + (targetCost - fromCost) * ease) * 100) / 100
      );
      setDispCalories(Math.round(fromCal + (targetCalories - fromCal) * ease));
      setDispProtein(
        Math.round((fromProt + (targetProtein - fromProt) * ease) * 10) / 10
      );
      if (t < 1) raf = requestAnimationFrame(animate);
    }

    raf = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [totals]);

  if (!totals || !coverage) {
    return <p className="italic text-white/70">No summary yet.</p>;
  }

  return (
    <section className="h-full flex flex-col justify-center text-white">
      <h2 className="text-xl font-medium mb-6 border-b border-white/10 pb-2">Summary</h2>
      
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div>
          <p className="text-sm text-white/60">Cost</p>
          <p className="text-2xl font-light text-[var(--accent-primary)]">${dispCost.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-sm text-white/60">Calories</p>
          <p className="text-2xl font-light text-[var(--accent-secondary)]">{dispCalories.toFixed(0)}</p>
        </div>
        <div>
          <p className="text-sm text-white/60">Protein</p>
          <p className="text-2xl font-light text-[var(--accent-tertiary)]">{dispProtein.toFixed(1)}g</p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-white/80">Calorie Coverage</span>
            <span>{(coverage.calories * 100).toFixed(0)}%</span>
          </div>
          <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
            <div 
              className="h-full bg-[var(--accent-secondary)] transition-all duration-1000 ease-out"
              style={{ width: `${Math.min(coverage.calories * 100, 100)}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-white/80">Protein Coverage</span>
            <span>{(coverage.protein * 100).toFixed(0)}%</span>
          </div>
          <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
            <div 
              className="h-full bg-[var(--accent-tertiary)] transition-all duration-1000 ease-out"
              style={{ width: `${Math.min(coverage.protein * 100, 100)}%` }}
            />
          </div>
        </div>
      </div>
    </section>
  );
}
