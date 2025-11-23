import PlanShell from "../components/PlanShell";
import ColorBends from "../components/ColorBends";
import GradualBlur from "../components/GradualBlur";
// import TopNav from "../components/TopNav";
// import Image from "next/image";

export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] relative overflow-hidden">
      <div className="fixed top-0 left-0 w-full h-full z-0">
        <ColorBends
          colors={["#00FFFF", "#0080FF", "#0000FF"]}
          rotation={30}
          speed={0.3}
          scale={1.2}
          frequency={1.4}
          warpStrength={1.2}
          mouseInfluence={0.8}
          parallax={0.6}
          noise={0.08}
          transparent
        />
      </div>
      
      {/* Vignette Overlay for Focus */}
      <div 
        className="fixed top-0 left-0 w-full h-full z-0 pointer-events-none"
        style={{
          background: 'radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.8) 100%)'
        }}
      />


      <main className="w-full max-w-[95vw] py-6 px-6 z-10 relative">
        {/* <TopNav /> */}
        <div className="py-6">
          <PlanShell />
        </div>
      </main>
      
      <GradualBlur
        position="bottom"
        height="12rem"
        strength={2}
        divCount={8}
        curve="bezier"
        exponential={true}
        opacity={1}
        target="page"
        zIndex={50}
      />
    </div>
  );
}
