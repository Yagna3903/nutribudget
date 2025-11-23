"use client";

import { useState } from "react";
import BudgetForm from "./BudgetForm";
import BasketList from "./BasketList";
import NutritionSummary from "./NutritionSummary";
import ChartsSection from "./ChartsSection";
import MagicBento from "./MagicBento";
import type { PlanResponse } from "../types/plan";

const MOCK_PLAN: PlanResponse = {
  basket: [
    {
      product_id: 1,
      name: "Whole Wheat Bread",
      store: "Local Store",
      category: "Bakery",
      clusterLabel: 0,
      clusterName: "Staples",
      unitGrams: 500,
      units: 1,
      cost: 3.5,
      calories: 1200,
      protein: 40,
    },
  ],
  totals: { cost: 3.5, calories: 1200, protein: 40 },
  coverage: { calories: 0.25, protein: 0.3 },
  cluster_breakdown: { Staples: 1.0 },
  processing_breakdown: { "Minimally processed": 1.0 },
};

export default function PlanShell() {
  const [plan, setPlan] = useState<PlanResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  async function handleSubmit(params: {
    budget: number;
    people: number;
    dietType: string;
    goal: string;
  }) {
    // In Phase 1 we don't call the backend yet — show mock plan for UI development.
    console.log("Generate plan with", params);
    // Simulate network latency and show loading/animations
    setLoading(true);
    // small delay to allow button/loader animation
    await new Promise((res) => setTimeout(res, 700));
    setPlan(MOCK_PLAN);
    // let animations run
    setLoading(false);
  }

  return (
    <div className="mx-auto w-full max-w-full space-y-6 py-8 text-white">
      <section>
        <h1 className="text-3xl font-bold text-black mb-2 tracking-tight text-center">
          NutriBudget — Plan Builder
        </h1>
      </section>

      <MagicBento
        className="grid gap-6 grid-cols-1 max-w-2xl mx-auto"
        textAutoHide={true}
        enableStars={true}
        enableSpotlight={true}
        enableBorderGlow={true}
        enableTilt={true}
        enableMagnetism={true}
        clickEffect={true}
        spotlightRadius={300}
        particleCount={12}
        glowColor="132, 0, 255"
      >
        <div className="rounded-2xl p-6 bg-black/40 backdrop-blur-md border border-white/10 h-full">
          <BudgetForm onSubmit={handleSubmit} loading={loading} />
        </div>

        <div className="rounded-2xl p-6 bg-black/40 backdrop-blur-md border border-white/10 h-full">
          <NutritionSummary
            totals={plan ? plan.totals : null}
            coverage={plan ? plan.coverage : null}
          />
        </div>

        <div className="rounded-2xl p-6 bg-black/40 backdrop-blur-md border border-white/10 h-full">
          <h2 className="text-xl font-medium text-white mb-4">Basket</h2>
          <BasketList items={plan ? plan.basket : []} />
        </div>

        <div className="rounded-2xl p-6 bg-black/40 backdrop-blur-md border border-white/10 h-full">
          <ChartsSection
            clusterBreakdown={plan ? plan.cluster_breakdown : {}}
            processingBreakdown={plan ? plan.processing_breakdown : {}}
          />
        </div>
      </MagicBento>
    </div>
  );
}
