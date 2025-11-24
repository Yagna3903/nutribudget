"use client";

import { motion } from "framer-motion";
import { Heart, TrendingUp } from "lucide-react";

type Props = {
    totalSpent: number;
    proteinPerDollar: number;
};

export default function SDGSection({ totalSpent, proteinPerDollar }: Props) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl p-6 bg-white border-2 border-emerald-200 hover:border-emerald-300 transition-all duration-300 shadow-md hover:shadow-lg overflow-hidden"
        >
            {/* Gradient header background */}
            <div className="absolute top-0 left-0 right-0 h-32 bg-gradient-to-br from-emerald-50 to-blue-50 -z-10 opacity-60" />

            <div className="flex items-center gap-2 mb-4">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-100 to-blue-100 flex items-center justify-center">
                    <Heart className="w-5 h-5 text-emerald-600" fill="currentColor" />
                </div>
                <h3 className="font-bold text-gray-800 text-lg">🌍 Social Impact</h3>
            </div>

            <p className="text-sm text-gray-600 mb-4">
                This plan contributes to UN Sustainable Development Goals:
            </p>

            <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-lg p-4 border-2 border-emerald-200 hover:border-emerald-300 transition-all">
                    <div className="text-4xl mb-2">🌾</div>
                    <div className="text-xs text-emerald-700 font-bold">SDG 2</div>
                    <div className="text-sm font-semibold text-gray-700">Zero Hunger</div>
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg p-4 border-2 border-blue-200 hover:border-blue-300 transition-all">
                    <div className="text-4xl mb-2">💪</div>
                    <div className="text-xs text-blue-700 font-bold">SDG 3</div>
                    <div className="text-sm font-semibold text-gray-700">Good Health</div>
                </div>
            </div>

            <div className="space-y-3 text-sm">
                <div className="flex items-center gap-3 p-3 rounded-lg bg-amber-50 border border-amber-200">
                    <div className="text-2xl">💰</div>
                    <div className="flex-1">
                        <div className="text-amber-700 text-xs font-medium">Optimized Budget</div>
                        <div className="text-gray-800 font-bold text-lg">${totalSpent.toFixed(2)}</div>
                    </div>
                </div>

                <div className="flex items-center gap-3 p-3 rounded-lg bg-emerald-50 border border-emerald-200">
                    <div className="text-2xl">🥗</div>
                    <div className="flex-1">
                        <div className="text-emerald-700 text-xs font-medium">Protein Value</div>
                        <div className="text-gray-800 font-bold text-lg">{proteinPerDollar.toFixed(1)}g per dollar</div>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
