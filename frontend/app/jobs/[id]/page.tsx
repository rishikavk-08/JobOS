"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type Job = {
  id: number;
  company: string;
  title: string;
  job_url?: string;
  location: string;
  source: string;
  status: string;
  fit_score?: number;
  fit_category?: string;
};

export default function JobAnalysisPage() {
  const params = useParams();
  const id = params.id;

  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadJob() {
      try {
        const response = await fetch(
          `http://localhost:8000/jobs/${id}`
        );

        if (!response.ok) {
          throw new Error("Job not found");
        }

        const data = await response.json();
        setJob(data);
      } catch (err) {
        console.error(err);
        setError("Could not load this job.");
      } finally {
        setLoading(false);
      }
    }

    loadJob();
  }, [id]);

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 p-10 text-white">
        <p className="text-slate-400">Loading JobOS analysis...</p>
      </main>
    );
  }

  if (error || !job) {
    return (
      <main className="min-h-screen bg-slate-950 p-10 text-white">
        <p className="text-red-400">
          {error || "Job not found."}
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-800 p-6">

          <h1 className="text-2xl font-bold">
            JobOS
          </h1>

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
              className="block px-4 py-3 text-slate-400 hover:text-white"
            >
              Job Inbox
            </a>

            <div className="rounded-lg bg-slate-800 px-4 py-3">
              Job Analysis
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

          {/* Header */}
          <div className="flex items-start justify-between">

            <div>

              <p className="text-sm text-slate-500">
                JOB ANALYSIS · #{job.id}
              </p>

              <h2 className="mt-2 text-3xl font-bold">
                {job.title}
              </h2>

              <p className="mt-2 text-slate-400">
                {job.company} · {job.location} · {job.source}
              </p>

            </div>

            {job.job_url && (
              <a
                href={job.job_url}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-lg border border-slate-700 px-5 py-3 text-sm hover:bg-slate-900"
              >
                View Job ↗
              </a>
            )}

          </div>

          {/* Status */}
          <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-7">

            <div className="flex items-center justify-between">

              <div>

                <p className="text-sm text-slate-500">
                  JOB STATUS
                </p>

                <h3 className="mt-2 text-3xl font-bold">
                  {job.status}
                </h3>

                <p className="mt-2 text-slate-400">
                  This opportunity has been added to your JobOS pipeline.
                </p>

              </div>

              <div className="text-center">

                <p className="text-5xl font-bold">
                  {job.fit_score ?? "—"}
                </p>

                <p className="mt-1 text-sm text-slate-500">
                  FIT SCORE
                </p>

              </div>

            </div>

          </div>

          {/* Analysis placeholder */}
          <div className="mt-8 grid grid-cols-2 gap-6">

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

              <h3 className="text-lg font-semibold">
                🟢 Strengths
              </h3>

              <p className="mt-4 text-sm text-slate-500">
                AI evidence matching will appear here.
              </p>

            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">

              <h3 className="text-lg font-semibold">
                🔴 Gaps
              </h3>

              <p className="mt-4 text-sm text-slate-500">
                AI-identified gaps will appear here.
              </p>

            </div>

          </div>

          {/* Requirements */}
          <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">

            <h3 className="text-lg font-semibold">
              Requirement Match
            </h3>

            <p className="mt-2 text-sm text-slate-500">
              Requirements will be extracted from the job description
              and mapped against your Career Brain.
            </p>

            <div className="mt-6 rounded-lg border border-dashed border-slate-700 p-8 text-center">

              <p className="text-slate-500">
                AI analysis pending
              </p>

            </div>

          </div>

          {/* Career Opportunity */}
          <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">

            <h3 className="text-lg font-semibold">
              Career Opportunity
            </h3>

            <div className="mt-6 grid grid-cols-4 gap-4">

              {[
                "Career Compounding",
                "Strategic Ownership",
                "Learning Velocity",
                "Exit Opportunities",
              ].map((label) => (
                <div
                  key={label}
                  className="rounded-lg border border-slate-800 p-4"
                >
                  <p className="text-sm text-slate-500">
                    {label}
                  </p>

                  <p className="mt-2 text-2xl font-bold">
                    —
                  </p>
                </div>
              ))}

            </div>

            <p className="mt-6 text-sm text-slate-500">
              Strategic opportunity scoring will be generated by the
              JobOS AI Engine.
            </p>

          </div>

          {/* Actions */}
          <div className="mt-8 flex gap-4">

            <button className="rounded-lg bg-white px-6 py-3 font-semibold text-slate-950">
              Apply
            </button>

            <button className="rounded-lg border border-slate-700 px-6 py-3">
              Save for Later
            </button>

            <button className="rounded-lg border border-slate-700 px-6 py-3 text-red-400">
              Skip
            </button>

          </div>

        </section>
      </div>
    </main>
  );
}
