"use client";

import { useEffect, useRef } from "react";

type Props = {
  sensitivity?: number; // controls scan speed (0-1)
  lineThickness?: number;
  linesColor?: string;
  gridScale?: number; // 0-1 relative spacing
  scanColor?: string;
  scanOpacity?: number; // 0-1
  enablePost?: boolean; // unused here, reserved
  bloomIntensity?: number; // mock effect strength
  chromaticAberration?: number; // 0-0.01
  noiseIntensity?: number; // 0-0.05
};

export default function GridScan({
  sensitivity = 0.5,
  lineThickness = 1,
  linesColor = "#392e4e",
  gridScale = 0.1,
  scanColor = "#FF9FFC",
  scanOpacity = 0.4,
  enablePost = false,
  bloomIntensity = 0.6,
  chromaticAberration = 0.002,
  noiseIntensity = 0.01,
}: Props) {
  const ref = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctxOrNull = canvas.getContext("2d");
    if (!ctxOrNull) return;
    const ctx = ctxOrNull;

    let width = 0;
    let height = 0;
    let raf = 0;
    let last = performance.now();

    function resize() {
      if (!canvas) return;
      const dpr = Math.max(1, window.devicePixelRatio || 1);
      const parent = canvas.parentElement || document.body;
      width = parent.clientWidth;
      height = parent.clientHeight;
      canvas.style.width = width + "px";
      canvas.style.height = height + "px";
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function drawGrid() {
      ctx.clearRect(0, 0, width, height);

      // soft background
      ctx.fillStyle = "rgba(10,8,15,0.6)";
      ctx.fillRect(0, 0, width, height);

      const spacing = Math.max(22, Math.round(Math.min(width, height) * gridScale));
      ctx.lineWidth = Math.max(0.5, lineThickness);
      ctx.strokeStyle = linesColor;
      ctx.globalAlpha = 0.22;

      // vertical lines
      for (let x = 0; x <= width; x += spacing) {
        ctx.beginPath();
        ctx.moveTo(x + 0.5, 0);
        ctx.lineTo(x + 0.5, height);
        ctx.stroke();
      }

      // horizontal lines
      for (let y = 0; y <= height; y += spacing) {
        ctx.beginPath();
        ctx.moveTo(0, y + 0.5);
        ctx.lineTo(width, y + 0.5);
        ctx.stroke();
      }

      ctx.globalAlpha = 1;
    }

    let tpos = 0;

    function frame(now: number) {
      const dt = (now - last) / 1000;
      last = now;

      // speed scaled by sensitivity and size
      const speed = 0.06 + sensitivity * 0.6; // relative
      tpos = (tpos + dt * speed * 100) % (height + 200);

      drawGrid();

      // draw scanning band
      const bandHeight = Math.max(24, Math.round(80 * (0.5 + sensitivity)));
      const y = (tpos - 100) % (height + bandHeight);

      // main scan gradient
      const grad = ctx.createLinearGradient(0, y, 0, y + bandHeight);
      grad.addColorStop(0, "transparent");
      grad.addColorStop(0.45, `rgba(255,255,255,${0.02 * bloomIntensity})`);
      grad.addColorStop(0.5, `rgba(255,255,255,${0.04 * bloomIntensity})`);
      grad.addColorStop(0.55, `rgba(255,255,255,${0.02 * bloomIntensity})`);
      grad.addColorStop(1, "transparent");

      ctx.fillStyle = grad;
      ctx.globalAlpha = Math.min(1, 0.12 * bloomIntensity + 0.02);
      ctx.fillRect(0, y - bandHeight * 0.4, width, bandHeight * 1.8);
      ctx.globalAlpha = 1;

      // colored scan line with chromatic aberration
      const centerY = y + bandHeight / 2;
      const lineW = Math.max(2, Math.round(lineThickness * 2));

      // red channel
      const ca = Math.max(0, chromaticAberration);
      const caOffset = Math.round(width * ca * 6);
      ctx.globalAlpha = scanOpacity * 0.9;
      ctx.fillStyle = scanColor;
      ctx.fillRect(-caOffset, centerY - lineW / 2, width + caOffset * 2, lineW);
      // subtle colored edges (simulate chromatic separation)
      if (ca > 0) {
        ctx.globalAlpha = scanOpacity * 0.55;
        ctx.fillStyle = "rgba(255,120,180,0.5)";
        ctx.fillRect(-caOffset, centerY - lineW, width + caOffset * 2, lineW / 2);
        ctx.fillStyle = "rgba(120,180,255,0.45)";
        ctx.fillRect(-caOffset, centerY + lineW / 2, width + caOffset * 2, lineW / 2);
      }
      ctx.globalAlpha = 1;

      // noise overlay
      if (noiseIntensity && noiseIntensity > 0) {
        const noiseAmount = Math.round(width * height * noiseIntensity * 0.0005);
        ctx.fillStyle = "rgba(255,255,255,0.02)";
        for (let i = 0; i < noiseAmount; i++) {
          const nx = Math.random() * width;
          const ny = Math.random() * height;
          ctx.fillRect(nx, ny, 1, 1);
        }
      }

      raf = requestAnimationFrame(frame);
    }

    function start() {
      resize();
      last = performance.now();
      raf = requestAnimationFrame(frame);
    }

    start();
    window.addEventListener("resize", resize);

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [sensitivity, lineThickness, linesColor, gridScale, scanColor, scanOpacity, bloomIntensity, chromaticAberration, noiseIntensity, enablePost]);

  return (
    <canvas
      ref={ref}
      aria-hidden
      className="pointer-events-none absolute inset-0 h-full w-full"
    />
  );
}
