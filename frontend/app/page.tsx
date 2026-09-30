export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-800 p-6">
          <h1 className="text-2xl font-bold">JobOS</h1>
          <p className="mt-1 text-sm text-slate-500">
            Career Operating System
          </p>

          <nav className="mt-10 space-y-2">
            <div className="rounded-lg bg-slate-800 px-4 py-3">
              Command Center
            </div>
            <div className="px-4 py-3 text-slate-400">
              Job Inbox
            </div>
            <div className="px-4 py-3 text-slate-400">
              Applications
            </div>
            <div className="px-4 py-3 text-slate-400">
              Networking
            </div>
            <div className="px-4 py-3 text-slate-400">
              Career Brain
            </div>
            <div className="px-4 py-3 text-slate-400">
              Analytics
            </div>
          </nav>
        </aside>

        {/* Main */}
        <section className="flex-1 p-10">

          <div>
            <p className="text-sm text-slate-500">COMMAND CENTER</p>
            <h2 className="mt-2 text-3xl font-bold">
              Good morning, Rishika.
            </h2>
            <p className="mt-2 text-slate-400">
              Your career pipeline at a glance.
            </p>
          </div>

          {/* Metrics */}
          <div className="mt-8 grid grid-cols-4 gap-5">

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-500">Jobs Found</p>
              <p className="mt-2 text-3xl font-bold">0</p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-500">Strong Fits</p>
              <p className="mt-2 text-3xl font-bold">0</p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-500">Applications</p>
              <p className="mt-2 text-3xl font-bold">0</p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-500">Interviews</p>
              <p className="mt-2 text-3xl font-bold">0</p>
            </div>

          </div>

          {/* Quick actions */}
          <div className="mt-8">
            <h3 className="text-lg font-semibold">Quick Actions</h3>

            <div className="mt-4 grid grid-cols-3 gap-5">

              <button className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-left hover:bg-slate-800">
                <p className="font-semibold">+ Analyze a Job</p>
                <p className="mt-2 text-sm text-slate-500">
                  Paste a job URL or description.
                </p>
              </button>

              <button className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-left hover:bg-slate-800">
                <p className="font-semibold">View Job Inbox</p>
                <p className="mt-2 text-sm text-slate-500">
                  Review your highest-potential opportunities.
                </p>
              </button>

              <button className="rounded-xl border border-slate-800 bg-slate-900 p-6 text-left hover:bg-slate-800">
                <p className="font-semibold">Career Brain</p>
                <p className="mt-2 text-sm text-slate-500">
                  Explore your experience and evidence.
                </p>
              </button>

            </div>
          </div>

          {/* Pipeline */}
          <div className="mt-10">
            <h3 className="text-lg font-semibold">
              Opportunity Pipeline
            </h3>

            <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900 p-6">
              <p className="text-slate-500">
                No opportunities analyzed yet.
              </p>
            </div>
          </div>

        </section>
      </div>
    </main>
  );
}
