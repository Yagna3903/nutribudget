"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

export default function TopNav() {
    const pathname = usePathname();

    const items: { href: string; label: string }[] = [
        { href: "/", label: "Home" },
        { href: "/plan", label: "Plan" },
        { href: "/basket", label: "Basket" },
        { href: "/charts", label: "Charts" },
    ];

    return (
        <nav className="w-full max-w-5xl mx-auto mb-6 z-20">
            <div className="flex gap-3 items-center px-2">
                {items.map((it) => {
                    const active = pathname === it.href;
                    return (
                        <Link
                            key={it.href}
                            href={it.href}
                            className={`px-3 py-1 rounded-md text-sm font-medium transition-colors duration-150 ${active
                                    ? "bg-white text-black/90"
                                    : "text-white/80 hover:bg-white/10"
                                }`}
                        >
                            {it.label}
                        </Link>
                    );
                })}
            </div>
        </nav>
    );
}
