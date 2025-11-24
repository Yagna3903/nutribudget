import PlanShell from "../components/PlanShell";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-emerald-50/30 to-green-50/50 relative overflow-hidden">
      {/* Subtle pattern overlay */}
      <div
        className="fixed inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2310B981' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}
      />

      {/* Decorative elements */}
      <div className="fixed top-20 right-10 w-64 h-64 bg-emerald-200/20 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-20 left-10 w-96 h-96 bg-amber-200/20 rounded-full blur-3xl pointer-events-none" />

      <main className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PlanShell />
      </main>
    </div>
  );
}
