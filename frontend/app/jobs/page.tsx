"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function JobsPage() {
  const router = useRouter();

  const [description, setDescription] = useState("");
  const [company, setCompany] = useState("");
  const [title, setTitle] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyzeJob() {
    if (!description.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/jobs", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company: company || "Unknown Company",
          title: title || "Untitled Role",
          location: location || "Unknown",
          raw_description: description,
          source: "Manual",
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create job");
      }

      const job = await response.json();

      router.push(`/jobs/${job.id}`);
    } catch (err) {
      console.error(err);
      setError("Could not connect to JobOS backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="flex min-h-screen">

        <aside className="w-64 border-r border-slate-800 p-6">
          <h1 className="text-2xl font-bold">JobOS</h1>

          <p className="mt-1 text-sm text-slate-500">
            Career Operating System
          </p>

          <nav className="mt-10 space-y-2">

            <a
              href="/"
              className="block px-4 py-3 text-slate-400 hover:text-white"
            >
              Command Center
            </a>

            <a
              href="/jobs"
              className="block rounded-lg bg-slate-800 px-4 py-3"
            >
              Job Inbox
            </a>

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

        <section className="flex-1 p-10">

          <p className="text-sm text-slate-500">
            JOB INBOX
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            Analyze an opportunity
          </h2>

          <p className="mt-2 text-slate-400">
            Add the job details and let JobOS evaluate it against your Career Brain.
          </p>

          <div className="mt-8 max-w-4xl">

            <div className="grid grid-cols-2 gap-4">

              <div>
                <label className="text-sm text-slate-400">
                  Company
                </label>

                <input
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="e.g. McKinsey"
                  className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 p-3 outline-none focus:border-slate-600"
                />
              </div>

              <div>
                <label className="text-sm text-slate-400">
                  Job Title
                </label>

                <input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Strategy Consultant"
                  className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 p-3 outline-none focus:border-slate-600"
                />
              </div>

            </div>

            <div className="mt-4">

              <label className="text-sm text-slate-400">
                Location
              </label>

              <input
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. Bangalore, India"
                className="mt-2 w-full rounded-lg border border-slate-800 bg-slate-900 p-3 outline-none focus:border-slate-600"
              />

            </div>

            <div className="mt-4">

              <label className="text-sm text-slate-400">
                Job Description
              </label>

              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Paste the full job description here..."
                className="mt-2 h-80 w-full rounded-xl border border-slate-800 bg-slate-900 p-5 text-sm outline-none focus:border-slate-600"
              />

            </div>

            <div className="mt-4 flex items-center justify-between">

              <p className="text-sm text-slate-500">
                {description.length.toLocaleString()} characters
              </p>

              <button
                onClick={analyzeJob}
                disabled={!description.trim() || loading}
                className="rounded-lg bg-white px-6 py-3 font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-30"
              >
                {loading ? "Creating..." : "Analyze Job →"}
              </button>

            </div>

            {error && (
              <div className="mt-4 rounded-lg border border-red-900 bg-red-950/30 p-4 text-sm text-red-400">
                {error}
              </div>
            )}

          </div>

          <div className="mt-12 max-w-5xl">

            <h3 className="text-lg font-semibold">
              Recent Opportunities
            </h3>

            <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900 p-6">

              <div className="flex items-center justify-between">

                <div>
                  <p className="font-semibold">
                    Slalom
                  </p>

                  <p className="mt-1 text-sm text-slate-400">
                    Corporate and Growth Strategist
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    Boston, MA · LinkedIn
                  </p>
                </div>

                <div className="text-right">

                  <p className="text-2xl font-bold">
                    70
                  </p>

                  <p className="text-xs text-yellow-500">
                    REVIEW
                  </p>

                </div>

              </div>

            </div>

          </div>

        </section>
      </div>
    </main>
  );
}
