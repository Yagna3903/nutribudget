"use client";

import { useState } from "react";
import { Download, TrendingDown } from "lucide-react";
import BudgetForm from "./BudgetForm";
import BasketList from "./BasketList";
import NutritionSummary from "./NutritionSummary";
import ChartsSection from "./ChartsSection";
import MagicBento from "./MagicBento";
import SDGSection from "./SDGSection";
import MealSuggestions from "./MealSuggestions";
import SmartChef from "./SmartChef";
import LocalShopper from "./LocalShopper"; // Added SmartChef import
import { exportShoppingList } from "../utils/exportList";
import type { PlanResponse } from "../types/plan";

export default function PlanShell() {
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(params: {
    budget: number;
    people: number;
    dietType: string;
    goal: string;
  }) {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/plan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || `Server error: ${res.status}`);
      }

      const data: PlanResponse = await res.json();
      setPlan(data);
    } catch (err: any) {
      console.error("Plan generation error:", err);
      setError(err.message || "Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  }

  const proteinPerDollar = plan
    ? plan.totals.protein / plan.totals.total_spent
    : 0;

  return (
    <div className="mx-auto w-full max-w-7xl space-y-8 py-8">
      {/* Hero Header */}
      <section className="text-center space-y-4 mb-12">
        <div className="inline-flex items-center gap-3 mb-2">
          <span className="text-5xl">🥗</span>
          <h1 className="text-5xl sm:text-6xl font-bold text-emerald-600 tracking-tight">
            NutriBudget
          </h1>
        </div>
        <p className="text-gray-600 text-lg sm:text-xl max-w-2xl mx-auto">
          Smart grocery planning that balances <span className="text-emerald-600 font-semibold">nutrition</span> and <span className="text-amber-600 font-semibold">budget</span>
        </p>

        {/* Savings Badge */}
        {plan?.savings && (
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-full text-amber-900 font-medium text-sm shadow-sm animate-in fade-in slide-in-from-top">
            <TrendingDown className="w-5 h-5 text-amber-600" />
            <span>
              You saved <strong className="text-amber-700">${plan.savings.amount.toFixed(2)}</strong> ({plan.savings.percentage}% less than typical shopping)
            </span>
          </div>
        )}
      </section>

      <div className="grid gap-6 grid-cols-1 lg:grid-cols-2 max-w-6xl mx-auto">
        {/* Input Form */}
        <div className="rounded-xl p-6 bg-white border-2 border-emerald-200 hover:border-emerald-300 transition-all duration-300 shadow-md hover:shadow-lg">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">🎯</span>
            <h2 className="text-xl font-semibold text-gray-800">Plan Your Budget</h2>
          </div>
          <BudgetForm onSubmit={handleSubmit} loading={loading} />
          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
              {error}
            </div>
          )}
        </div>

        {/* SDG Impact */}
        {plan && (
          <SDGSection
            totalSpent={plan.totals.total_spent}
            proteinPerDollar={proteinPerDollar}
          />
        )}

        {/* Nutrition Summary */}
        <div className="rounded-xl p-6 bg-white border-2 border-emerald-200 hover:border-emerald-300 transition-all duration-300 shadow-md hover:shadow-lg">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">🥗</span>
            <h2 className="text-xl font-semibold text-gray-800">Nutrition Summary</h2>
          </div>
          <NutritionSummary
            totals={plan ? plan.totals : null}
            coverage={plan ? plan.coverage : null}
          />
        </div>

        {/* Meal Suggestions */}
        {plan && plan.items.length > 0 && (
          <div className="rounded-xl p-6 bg-white border-2 border-blue-200 hover:border-blue-300 transition-all duration-300 shadow-md hover:shadow-lg">
            <MealSuggestions items={plan.items} dietType={plan.inputs.dietType} />
          </div>
        )}

        {/* Smart Chef */}
        {plan && plan.items.length > 0 && (
          <div className="lg:col-span-2">
            <SmartChef items={plan.items} />
          </div>
        )}

        {/* Basket with Export */}
        <div className="rounded-xl p-6 bg-white border-2 border-amber-200 hover:border-amber-300 transition-all duration-300 shadow-md hover:shadow-lg lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🛒</span>
              <h2 className="text-xl font-semibold text-gray-800">Your Shopping Basket</h2>
            </div>
            {plan && plan.items.length > 0 && (
              <button
                onClick={() => exportShoppingList(plan.items, plan.totals)}
                className="flex items-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-sm font-medium transition-all duration-200 shadow-sm hover:shadow-md"
              >
                <Download className="w-4 h-4" />
                Export List
              </button>
            )}
          </div>
          <BasketList items={plan ? plan.items : []} />
        </div>

        {/* Charts & Local Shopper Grid */}
        {plan && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:col-span-2">
            <div className="lg:col-span-2 rounded-xl p-6 bg-white border-2 border-blue-200 hover:border-blue-300 transition-all duration-300 shadow-md hover:shadow-lg">
              <div className="flex items-center gap-2 mb-4">
                <span className="text-2xl">📊</span>
                <h2 className="text-xl font-semibold text-gray-800">Basket Analysis</h2>
              </div>
              <ChartsSection
                clusterBreakdown={plan.clusterBreakdown}
                processingBreakdown={plan.processingBreakdown}
              />
            </div>
            <div className="lg:col-span-1">
              <LocalShopper items={plan.items} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
