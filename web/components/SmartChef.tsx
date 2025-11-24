"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, ChefHat, Clock, Flame, ChevronDown, ChevronUp } from "lucide-react";
import type { BasketItem } from "../types/plan";

type Recipe = {
    name: string;
    time: string;
    difficulty: string;
    ingredients: string[];
    instructions: string[];
    calories: number;
};

type Props = {
    items: BasketItem[];
};

export default function SmartChef({ items }: Props) {
    const [loading, setLoading] = useState(false);
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [expandedRecipe, setExpandedRecipe] = useState<number | null>(null);

    const generateRecipes = async () => {
        if (!items || items.length === 0) return;

        setLoading(true);
        setError(null);
        setRecipes([]);

        try {
            const response = await fetch("http://127.0.0.1:5000/api/recipes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ items }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Failed to generate recipes");
            }

            setRecipes(data.recipes);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="rounded-xl p-6 bg-white border-2 border-purple-200 hover:border-purple-300 transition-all duration-300 shadow-md hover:shadow-lg">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center">
                        <ChefHat className="w-5 h-5 text-purple-600" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-gray-800">Smart Chef</h2>
                        <p className="text-xs text-purple-600 font-medium">AI-Powered Recipes</p>
                    </div>
                </div>

                <button
                    onClick={generateRecipes}
                    disabled={loading || items.length === 0}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-sm transition-all duration-300 ${loading
                            ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                            : "bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-md hover:shadow-lg hover:scale-105"
                        }`}
                >
                    {loading ? (
                        <>
                            <Sparkles className="w-4 h-4 animate-spin" />
                            Cooking...
                        </>
                    ) : (
                        <>
                            <Sparkles className="w-4 h-4" />
                            Generate Recipes
                        </>
                    )}
                </button>
            </div>

            {error && (
                <div className="p-4 mb-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                    ⚠️ {error}
                </div>
            )}

            {!loading && recipes.length === 0 && !error && (
                <div className="text-center py-8 text-gray-500">
                    <p className="mb-2">👨‍🍳</p>
                    <p className="text-sm">Click "Generate Recipes" to turn your basket into delicious meals!</p>
                </div>
            )}

            <div className="space-y-4">
                <AnimatePresence>
                    {recipes.map((recipe, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="border border-gray-200 rounded-xl overflow-hidden bg-gray-50 hover:bg-white hover:shadow-md transition-all duration-300"
                        >
                            <div
                                className="p-4 flex items-center justify-between cursor-pointer"
                                onClick={() => setExpandedRecipe(expandedRecipe === idx ? null : idx)}
                            >
                                <div className="flex-1">
                                    <h3 className="font-bold text-gray-800">{recipe.name}</h3>
                                    <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                                        <span className="flex items-center gap-1">
                                            <Clock className="w-3 h-3" /> {recipe.time}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Flame className="w-3 h-3 text-orange-500" /> {recipe.calories} kcal
                                        </span>
                                        <span className={`px-2 py-0.5 rounded-full text-[10px] uppercase font-bold ${recipe.difficulty === "Easy" ? "bg-green-100 text-green-700" :
                                                recipe.difficulty === "Medium" ? "bg-yellow-100 text-yellow-700" :
                                                    "bg-red-100 text-red-700"
                                            }`}>
                                            {recipe.difficulty}
                                        </span>
                                    </div>
                                </div>
                                {expandedRecipe === idx ? (
                                    <ChevronUp className="w-5 h-5 text-gray-400" />
                                ) : (
                                    <ChevronDown className="w-5 h-5 text-gray-400" />
                                )}
                            </div>

                            <AnimatePresence>
                                {expandedRecipe === idx && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: "auto", opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        className="overflow-hidden border-t border-gray-200"
                                    >
                                        <div className="p-4 bg-white space-y-4">
                                            <div>
                                                <h4 className="text-sm font-bold text-gray-700 mb-2">Ingredients</h4>
                                                <ul className="grid grid-cols-2 gap-2">
                                                    {recipe.ingredients.map((ing, i) => (
                                                        <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                                                            <span className="text-purple-500">•</span>
                                                            {ing}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                            <div>
                                                <h4 className="text-sm font-bold text-gray-700 mb-2">Instructions</h4>
                                                <ol className="space-y-2">
                                                    {recipe.instructions.map((step, i) => (
                                                        <li key={i} className="text-sm text-gray-600 flex gap-3">
                                                            <span className="flex-shrink-0 w-5 h-5 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-xs font-bold">
                                                                {i + 1}
                                                            </span>
                                                            <span>{step}</span>
                                                        </li>
                                                    ))}
                                                </ol>
                                            </div>
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </div>
    );
}
