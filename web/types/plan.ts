export type BasketItem = {
  product_id: string | number;
  name: string;
  store: string;
  category: string;
  clusterLabel: number;
  clusterName: string;
  unitGrams: number;
  units: number;
  cost: number;
  calories: number;
  protein: number;
};

export type PlanTotals = {
  cost: number;
  calories: number;
  protein: number;
};

export type PlanCoverage = {
  calories: number; // fraction (0-1)
  protein: number; // fraction (0-1)
};

export type PlanResponse = {
  basket: BasketItem[];
  totals: PlanTotals;
  coverage: PlanCoverage;
  cluster_breakdown: Record<string, number>;
  processing_breakdown: Record<string, number>;
};
