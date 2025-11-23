import PlanShell from "../../components/PlanShell";
import ColorBends from "../../components/ColorBends";
import TopNav from "../../components/TopNav";

export default function PlanPage() {
  return (
    <div className="relative flex min-h-screen items-start justify-center bg-[#05020a] font-sans">
      <div className="absolute inset-0 -z-10">
        <ColorBends
          rotation={45}
          speed={0.2}
          colors={["#FF9FFC", "#392e4e", "#6EF6FF", "#FFCC66"]}
          transparent
          autoRotate={0.2}
          scale={1}
          frequency={1.0}
          warpStrength={1.0}
          mouseInfluence={1.0}
          parallax={0.6}
          noise={0.08}
        />
      </div>

      <main className="w-full max-w-5xl py-6 px-6 z-10">
        <TopNav />
        <div className="py-6">
          <PlanShell />
        </div>
      </main>
    </div>
  );
}
