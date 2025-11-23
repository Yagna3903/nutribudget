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
      className="w-full max-w-lg"
    >
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="flex flex-col">
          <span className="text-sm text-white/90">Budget</span>
          <input
            className="glass-input w-full px-3 py-2 text-white placeholder:text-white/40 rounded-t-md focus:border-b-2"
            type="number"
            value={budget}
            onChange={(e) => setBudget(Number(e.target.value))}
          />
        </label>

        <label className="flex flex-col">
          <span className="text-sm text-white/90">People</span>
          <input
            className="glass-input w-full px-3 py-2 text-white placeholder:text-white/40 rounded-t-md focus:border-b-2"
            type="number"
            value={people}
            onChange={(e) => setPeople(Number(e.target.value))}
          />
        </label>

        <label className="flex flex-col">
          <span className="text-sm text-white/90">Diet Type</span>
          <select
            className="glass-input w-full px-3 py-2 text-white rounded-t-md focus:border-b-2 [&>option]:bg-black"
            value={dietType}
            onChange={(e) => setDietType(e.target.value)}
          >
            <option value="veg">Vegetarian</option>
            <option value="non_veg">Non-vegetarian</option>
            <option value="vegan">Vegan</option>
          </select>
        </label>

        <label className="flex flex-col">
          <span className="text-sm text-white/90">Goal</span>
          <select
            className="glass-input w-full px-3 py-2 text-white rounded-t-md focus:border-b-2 [&>option]:bg-black"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
          >
            <option value="balanced">Balanced</option>
            <option value="high_protein">High Protein</option>
            <option value="low_sugar">Low Sugar</option>
          </select>
        </label>
      </div>

      <div className="mt-4">
        <button
          className={`w-full rounded-lg px-6 py-3 text-white font-medium tracking-wide transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed ${
            loading
              ? "bg-white/10"
              : "bg-gradient-to-r from-[var(--accent-primary)] via-[var(--accent-secondary)] to-[var(--accent-tertiary)] text-black hover:shadow-[0_0_20px_rgba(92,255,234,0.4)] hover:scale-[1.02]"
          }`}
          type="submit"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Plan"}
        </button>
      </div>
    </form>
  );
}
