"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function TopNav() {
    const pathname = usePathname();

    const navLinks = [
        { href: "/", label: "Home" },
        { href: "/plan", label: "Plan" },
        { href: "/basket", label: "Basket" },
        { href: "/charts", label: "Charts" },
    ];

    return (
        <nav className="flex items-center justify-between mb-8">
            <Link href="/" className="text-2xl font-bold text-white hover:text-emerald-400 transition-colors">
                🥗 NutriBudget
            </Link>

            <div className="flex gap-6">
                {navLinks.map((link) => (
                    <Link
                        key={link.href}
                        href={link.href}
                        className={`text-sm font-medium transition-colors ${pathname === link.href
                                ? "text-emerald-400"
                                : "text-gray-400 hover:text-white"
                            }`}
                    >
                        {link.label}
                    </Link>
                ))}
            </div>
        </nav>
    );
}
