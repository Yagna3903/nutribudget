"use client";

export default function PlanSkeleton() {
    return (
        <div className="grid gap-6 grid-cols-1 lg:grid-cols-2 max-w-6xl mx-auto animate-pulse">
            {/* Form Skeleton */}
            <div className="rounded-xl p-6 bg-white/90 backdrop-blur-sm border-2 border-gray-200 shadow-lg">
                <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
                <div className="space-y-4">
                    <div className="h-10 bg-gray-200 rounded"></div>
                    <div className="h-10 bg-gray-200 rounded"></div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="h-10 bg-gray-200 rounded"></div>
                        <div className="h-10 bg-gray-200 rounded"></div>
                    </div>
                    <div className="h-12 bg-emerald-200 rounded"></div>
                </div>
            </div>

            {/* Nutrition Skeleton */}
            <div className="rounded-xl p-6 bg-white/90 backdrop-blur-sm border-2 border-gray-200 shadow-lg">
                <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
                <div className="space-y-3">
                    <div className="h-8 bg-gray-200 rounded"></div>
                    <div className="h-8 bg-gray-200 rounded"></div>
                    <div className="h-8 bg-gray-200 rounded"></div>
                </div>
            </div>

            {/* Basket Skeleton */}
            <div className="rounded-xl p-6 bg-white/90 backdrop-blur-sm border-2 border-gray-200 shadow-lg lg:col-span-2">
                <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
                <div className="space-y-2">
                    {[...Array(5)].map((_, i) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-gray-100 rounded-lg">
                            <div className="flex-1">
                                <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
                                <div className="h-3 bg-gray-300 rounded w-1/2"></div>
                            </div>
                            <div className="h-5 bg-gray-300 rounded w-16"></div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
