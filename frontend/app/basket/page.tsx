import BasketList from "../../components/BasketList";
import ColorBends from "../../components/ColorBends";
import TopNav from "../../components/TopNav";

export default function BasketPage() {
  return (
    <div className="relative flex min-h-screen items-start justify-center bg-[#05020a] font-sans">
      <div className="absolute inset-0 -z-10">
        <ColorBends
          rotation={20}
          speed={0.15}
          colors={["#6EF6FF", "#FF9FFC", "#FFCC66"]}
          transparent
          autoRotate={0.1}
          scale={1}
          frequency={1.2}
          warpStrength={0.9}
          mouseInfluence={0.9}
          parallax={0.5}
          noise={0.05}
        />
      </div>

      <main className="w-full max-w-5xl py-6 px-6 z-10">
        <TopNav />
        <div className="py-6 space-y-6">
          <h1 className="text-3xl font-bold text-white">Basket</h1>
          <div className="bg-[rgba(255,255,255,0.03)] rounded-lg p-4">
            {/* TODO: Connect to actual plan data source */}
            <BasketList items={[]} />
          </div>
        </div>
      </main>
    </div>
  );
}
