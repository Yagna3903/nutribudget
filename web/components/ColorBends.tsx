"use client";

import React, { useRef, useEffect } from 'react';

interface ColorBendsProps {
    rotation?: number;
    speed?: number;
    colors?: string[];
    transparent?: boolean;
    autoRotate?: number;
    scale?: number;
    frequency?: number;
    warpStrength?: number;
    mouseInfluence?: number;
    parallax?: number;
    noise?: number;
}

export default function ColorBends({
    rotation = 0,
    speed = 0.1,
    colors = ["#6EF6FF", "#FF9FFC", "#FFCC66"],
    transparent = false,
    autoRotate = 0,
    scale = 1,
    frequency = 1,
    warpStrength = 0.5,
    mouseInfluence = 0.5,
    parallax = 0,
    noise = 0,
}: ColorBendsProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const animationRef = useRef<number>();

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Set canvas size
        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        resize();
        window.addEventListener('resize', resize);

        // Animation variables
        let time = 0;
        let mouseX = 0;
        let mouseY = 0;

        const handleMouseMove = (e: MouseEvent) => {
            mouseX = e.clientX / window.innerWidth;
            mouseY = e.clientY / window.innerHeight;
        };
        window.addEventListener('mousemove', handleMouseMove);

        // Draw function
        const draw = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Create gradient
            const gradient = ctx.createLinearGradient(
                0,
                0,
                canvas.width,
                canvas.height
            );

            colors.forEach((color, index) => {
                const offset = (index / (colors.length - 1) + time * speed) % 1;
                gradient.addColorStop(offset, color);
            });

            ctx.fillStyle = gradient;
            ctx.globalAlpha = transparent ? 0.3 : 1;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            time += 0.01;
            animationRef.current = requestAnimationFrame(draw);
        };

        draw();

        return () => {
            window.removeEventListener('resize', resize);
            window.removeEventListener('mousemove', handleMouseMove);
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [colors, speed, transparent]);

    return (
        <canvas
            ref={canvasRef}
            className="fixed inset-0 w-full h-full"
            style={{ pointerEvents: 'none' }}
        />
    );
}
