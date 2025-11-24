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
      <p className="italic text-gray-500 text-center py-8">
        No items yet. Generate a plan to see your basket.
      </p>
    );
  }

  const displayItems = items.slice(0, 10);
  const hasMore = items.length > 10;

  return (
    <div className="space-y-3">
      {hasMore && (
        <p className="text-sm text-gray-600 font-medium">
          Showing 10 of {items.length} items
        </p>
      )}
      <div className="grid gap-3 max-h-[500px] overflow-y-auto pr-2">
        {displayItems.map((item, i) => (
          <div
            key={String(item.product_id)}
            className={`p-4 rounded-lg bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 hover:border-amber-300 hover:shadow-md transition-all duration-300 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-3"
              }`}
            style={{ transitionDelay: `${i * 50}ms` }}
          >
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-800 text-base">{item.product_name}</h3>
                <p className="text-xs text-gray-600 uppercase tracking-wider mt-1">
                  {item.store} • {item.category}
                </p>
              </div>
              <span className="text-amber-700 font-bold text-lg font-mono">${item.estimated_cost.toFixed(2)}</span>
            </div>

            <div className="mt-3 flex flex-wrap gap-3 text-sm">
              <span className="px-2 py-1 bg-white rounded-md text-gray-700 font-medium">
                {item.quantity_units} units
              </span>
              <span className="px-2 py-1 bg-emerald-100 text-emerald-700 rounded-md font-medium">
                Health: {item.health_score?.toFixed(0) || 'N/A'}
              </span>
              <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-md font-medium text-xs">
                {item.cluster_label}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
