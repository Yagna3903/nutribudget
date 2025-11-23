import ChartsSection from "../../components/ChartsSection";
import ColorBends from "../../components/ColorBends";
import TopNav from "../../components/TopNav";

export default function ChartsPage() {
  return (
    <div className="relative flex min-h-screen items-start justify-center bg-[#05020a] font-sans">
      <div className="absolute inset-0 -z-10">
        <ColorBends
          rotation={0}
          speed={0.25}
          colors={["#392e4e", "#6EF6FF"]}
          transparent
          autoRotate={0.05}
          scale={1}
          frequency={0.9}
          warpStrength={1.1}
          mouseInfluence={1.0}
          parallax={0.4}
          noise={0.06}
        />
      </div>

      <main className="w-full max-w-5xl py-6 px-6 z-10">
        <TopNav />
        <div className="py-6 space-y-6">
          <h1 className="text-3xl font-bold text-white">Charts</h1>
          <div className="bg-[rgba(255,255,255,0.03)] rounded-lg p-4">
            <ChartsSection />
          </div>
        </div>
      </main>
    </div>
  );
}
