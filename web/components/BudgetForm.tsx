"use client";

import React, { useState } from "react";

type Props = {
  onSubmit: (params: {
    budget: number;
    people: number;
    dietType: string;
    goal: string;
  }) => void;
  loading?: boolean;
};

export default function BudgetForm({ onSubmit, loading = false }: Props) {
  const [budget, setBudget] = useState<number>(40);
  const [people, setPeople] = useState<number>(2);
  const [dietType, setDietType] = useState<string>("veg");
  const [goal, setGoal] = useState<string>("balanced");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({ budget, people, dietType, goal });
      }}
      className="w-full"
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col space-y-1.5">
          <span className="text-sm font-medium text-gray-700">Budget ($)</span>
          <input
            className="w-full px-4 py-2.5 bg-white border-2 border-gray-200 rounded-lg text-gray-800 placeholder:text-gray-400 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition-all"
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            value={budget}
            onChange={(e) => {
              const val = parseInt(e.target.value) || 0;
              setBudget(val);
            }}
          />
        </label>

        <label className="flex flex-col space-y-1.5">
          <span className="text-sm font-medium text-gray-700">People</span>
          <input
            className="w-full px-4 py-2.5 bg-white border-2 border-gray-200 rounded-lg text-gray-800 placeholder:text-gray-400 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition-all"
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            value={people}
            onChange={(e) => {
              const val = parseInt(e.target.value) || 0;
              setPeople(val);
            }}
          />
        </label>

        <label className="flex flex-col space-y-1.5">
          <span className="text-sm font-medium text-gray-700">Diet Type</span>
          <select
            className="w-full px-4 py-2.5 bg-white border-2 border-gray-200 rounded-lg text-gray-800 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition-all"
            value={dietType}
            onChange={(e) => setDietType(e.target.value)}
          >
            <option value="veg">🥬 Vegetarian</option>
            <option value="non_veg">🍗 Non-vegetarian</option>
            <option value="vegan">🌱 Vegan</option>
          </select>
        </label>

        <label className="flex flex-col space-y-1.5">
          <span className="text-sm font-medium text-gray-700">Goal</span>
          <select
            className="w-full px-4 py-2.5 bg-white border-2 border-gray-200 rounded-lg text-gray-800 focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition-all"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
          >
            <option value="balanced">⚖️ Balanced</option>
            <option value="high_protein">💪 High Protein</option>
            <option value="low_sugar">🍬 Low Sugar</option>
          </select>
        </label>
      </div>

      <div className="mt-6">
        <button
          className={`w-full rounded-lg px-6 py-3.5 font-semibold tracking-wide transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed ${loading
            ? "bg-gray-300 text-gray-500"
            : "bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white shadow-md hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
            }`}
          type="submit"
          disabled={loading}
        >
          {loading ? "✨ Generating..." : "🎯 Generate Smart Plan"}
        </button>
      </div>
    </form>
  );
}
