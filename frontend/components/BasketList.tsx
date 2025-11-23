"use client";
import React, { useEffect, useState } from "react";
import type { BasketItem } from "../types/plan";

type Props = {
  items: BasketItem[];
};

export default function BasketList({ items }: Props) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    // trigger entrance animation when items change
    if (items && items.length > 0) {
      setVisible(false);
      const t = setTimeout(() => setVisible(true), 50);
      return () => clearTimeout(t);
    } else {
      setVisible(false);
    }
  }, [items]);

  if (!items || items.length === 0) {
    return (
      <p className="italic text-white/70">
        No items yet. Generate a plan to see your basket.
      </p>
    );
  }

  return (
    <div className="grid gap-3">
      {items.map((item, i) => (
        <div
          key={String(item.product_id)}
          className={`p-4 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-all duration-300 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-3"
            }`}
          style={{ transitionDelay: `${i * 50}ms` }}
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-medium text-white">{item.product_name}</h3>
              <p className="text-xs text-white/50 uppercase tracking-wider mt-0.5">
                {item.store} • {item.category}
              </p>
            </div>
            <span className="text-[var(--accent-primary)] font-mono">${item.estimated_cost.toFixed(2)}</span>
          </div>

          <div className="mt-3 flex gap-4 text-sm text-white/70">
            <span>{item.quantity_units} × {item.unit}</span>
            <span className="w-px h-4 bg-white/20"></span>
            <span className="text-[var(--accent-secondary)]">Health: {item.health_score}</span>
            <span className="w-px h-4 bg-white/20"></span>
            <span className="text-[var(--accent-tertiary)]">{item.cluster_label}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
