"use client"

import Link from "next/link"
import {
  ArrowRight,
  CalendarDays,
  CheckCircle2,
  Clock3,
  FileCheck2,
  FolderOpen,
  GraduationCap,
  Landmark,
  Plus,
  Search,
  ShieldCheck,
  Sparkles,
  UploadCloud,
} from "lucide-react"
import { useCivicFlow } from "@/lib/civicflow-store"
import { serviceCatalog } from "@/src/data/serviceCatalog"
import { Button, Card, Status } from "@/components/page-primitives"

const statusLabel = {
  draft: "Draft",
  prepared: "Prepared",
  validation_complete: "Ready for review",
  waiting_for_approval: "Waiting for approval",
  approved_for_submission: "Approved",
  submission_in_progress: "Submission in progress",
  submitted: "Submitted",
  failed: "Needs attention",
  uncertain: "Needs confirmation",
} as const

const quickActions = [
  { title: "Browse services", text: "Find public programs and certificates", href: "/services", Icon: Landmark },
  { title: "Track an application", text: "Review saved work and progress", href: "/applications", Icon: Search },
  { title: "Your documents", text: "Manage files for your applications", href: "/documents", Icon: FolderOpen },
  { title: "Check eligibility", text: "Explore education support options", href: "/services/scholarships", Icon: ShieldCheck },
]

export default function DashboardPage() {
  const { state } = useCivicFlow()
  const applications = Object.values(state.applications).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))
  const activeApplications = applications.filter((application) => application.status !== "submitted").slice(0, 3)
  const pendingApprovals = applications.filter((application) => application.approvalState === "not_started" && application.status !== "draft").length
  const recentEvents = applications.flatMap((application) => {
    const service = serviceCatalog.find((item) => item.id === application.serviceId)
    return application.activity.map((event) => ({ ...event, serviceName: service?.title ?? "Application", applicationId: application.id }))
  }).sort((a, b) => b.timestamp.localeCompare(a.timestamp)).slice(0, 4)

  return <div className="space-y-8">
    <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <div className="mb-3 flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.12em] text-blue-700"><span>Civic workspace</span><span className="text-slate-300">•</span><span className="normal-case tracking-normal text-slate-500">Your public services in one place</span></div>
        <h1 className="text-3xl font-semibold tracking-tight text-[#0b1c30] sm:text-[34px]">Welcome back, {state.user.name}</h1>
        <p className="mt-2 text-sm text-slate-600">Review your applications, discover services, and see what needs your attention.</p>
      </div>
      <div className="flex flex-wrap gap-2"><Button href="/applications" variant="secondary"><Clock3 className="mr-2 size-4" />Recent activity</Button><Button href="/applications/new"><Plus className="mr-2 size-4" />New application</Button></div>
    </section>

    <section className="grid gap-5 xl:grid-cols-[minmax(0,1.7fr)_minmax(270px,0.9fr)]">
      <Card className="overflow-hidden border-blue-200 bg-gradient-to-br from-white via-white to-blue-50/80 p-0">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-blue-100 px-6 py-5 sm:px-7">
          <div className="flex items-center gap-3"><span className="grid size-10 place-items-center rounded-xl bg-blue-50 text-blue-700"><Sparkles className="size-5" /></span><div><h2 className="font-semibold">CivicFlow AI Assistant</h2><p className="mt-0.5 text-xs text-slate-500">Get help understanding services and next steps</p></div></div>
          <Status tone="blue">Demo assistant</Status>
        </div>
        <div className="px-6 py-5 sm:px-7">
          <p className="max-w-2xl text-sm leading-6 text-slate-600">Ask a question about public services, eligibility, or your application checklist. You stay in control of every submission.</p>
          <Link href="/assistant" className="mt-5 flex min-h-12 items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 text-sm text-slate-500 shadow-sm transition hover:border-blue-300 hover:text-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"><Search className="size-4 shrink-0" /><span className="flex-1">Ask about a service or application…</span><span className="rounded-lg bg-blue-600 px-3 py-2 text-xs font-semibold text-white">Ask CivicFlow <ArrowRight className="ml-1 inline size-3.5" /></span></Link>
          <div className="mt-4 flex flex-wrap items-center gap-2 text-xs"><span className="mr-1 text-slate-500">Try asking</span><Link href="/services/scholarships" className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1.5 font-medium text-blue-800 hover:bg-blue-100">What scholarships can I apply for?</Link><Link href="/applications" className="rounded-full border border-slate-200 bg-white px-3 py-1.5 font-medium text-slate-700 hover:border-blue-200">How do I track my application?</Link></div>
        </div>
      </Card>

      <Card className="relative overflow-hidden border-l-4 border-l-blue-600 bg-white p-6">
        <div className="flex items-center justify-between"><span className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-blue-700"><ShieldCheck className="size-4" />Service spotlight</span><Status tone="green">Available</Status></div>
        <h2 className="mt-5 text-xl font-semibold leading-snug">Post-Matric Scholarship</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">Explore education support for eligible students in Maharashtra and review the requirements before you begin.</p>
        <div className="mt-5 flex items-center gap-2 border-t border-slate-100 pt-4 text-xs text-slate-500"><GraduationCap className="size-4 text-blue-600" />Maharashtra Government</div>
        <Button href="/services/post-matric-scholarship" variant="secondary" className="mt-5 w-full">Review service <ArrowRight className="ml-2 size-4" /></Button>
      </Card>
    </section>

    <section>
      <div className="mb-4 flex items-end justify-between gap-3"><div><h2 className="text-xl font-semibold">Active applications</h2><p className="mt-1 text-sm text-slate-500">Pick up where you left off.</p></div><Link href="/applications" className="inline-flex items-center gap-1 text-sm font-semibold text-blue-700 hover:text-blue-900">View all <ArrowRight className="size-4" /></Link></div>
      {activeApplications.length ? <div className="grid gap-4 lg:grid-cols-3">{activeApplications.map((application) => {
        const service = serviceCatalog.find((item) => item.id === application.serviceId)
        const tone = application.status === "failed" || application.status === "uncertain" ? "amber" : application.status === "validation_complete" || application.status === "approved_for_submission" ? "green" : "blue"
        return <Card key={application.id} className="flex min-h-[220px] flex-col p-5 transition hover:border-blue-200 hover:shadow-md">
          <div className="flex items-start justify-between gap-3"><span className="rounded-full bg-blue-50 px-2.5 py-1 text-[11px] font-semibold tracking-wide text-blue-800">APP · {application.id.slice(-6).toUpperCase()}</span><Status tone={tone}>{statusLabel[application.status]}</Status></div>
          <h3 className="mt-4 text-base font-semibold leading-snug">{service?.title ?? "Public service application"}</h3><p className="mt-1 text-xs text-slate-500">{service?.department ?? "Government service"}</p>
          <div className="mt-auto pt-5"><div className="mb-2 flex justify-between text-xs"><span className="text-slate-500">Application progress</span><span className="font-semibold tabular-nums">{application.progress}%</span></div><div className="h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-blue-600 transition-all" style={{ width: `${application.progress}%` }} /></div><Link href={`/applications/${application.id}/workspace`} className="mt-4 inline-flex items-center text-sm font-semibold text-blue-700 hover:text-blue-900">Continue application <ArrowRight className="ml-1 size-4" /></Link></div>
        </Card>
      })}</div> : <Card className="flex flex-col items-start gap-4 border-dashed bg-white/70 p-6 sm:flex-row sm:items-center"><span className="grid size-11 place-items-center rounded-xl bg-blue-50 text-blue-700"><FileCheck2 className="size-5" /></span><div className="flex-1"><h3 className="font-semibold">Your applications will appear here</h3><p className="mt-1 text-sm text-slate-500">Browse the service directory to find a program or start a new application.</p></div><Button href="/services" variant="secondary">Explore services <ArrowRight className="ml-2 size-4" /></Button></Card>}
    </section>

    <section>
      <div className="mb-4"><h2 className="text-xl font-semibold">Quick actions</h2><p className="mt-1 text-sm text-slate-500">Common tasks, ready when you are.</p></div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{quickActions.map(({ title, text, href, Icon }) => <Link href={href} key={title} className="group rounded-2xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"><Card className="h-full min-h-[150px] transition group-hover:-translate-y-0.5 group-hover:border-blue-200 group-hover:shadow-md"><span className="grid size-10 place-items-center rounded-xl bg-blue-50 text-blue-700 transition group-hover:bg-blue-600 group-hover:text-white"><Icon className="size-5" /></span><h3 className="mt-4 font-semibold">{title}</h3><p className="mt-1 text-sm leading-5 text-slate-500">{text}</p></Card></Link>)}</div>
    </section>

    <section className="grid gap-5 lg:grid-cols-[minmax(0,1.4fr)_minmax(260px,0.8fr)]">
      <Card className="p-0"><div className="flex items-center justify-between border-b border-slate-100 px-5 py-4"><div><h2 className="font-semibold">Recent activity</h2><p className="mt-0.5 text-xs text-slate-500">Updates from your application workspace</p></div><CalendarDays className="size-5 text-slate-400" /></div>
        {recentEvents.length ? <div className="divide-y divide-slate-100">{recentEvents.map((event) => <div key={event.id} className="flex items-start gap-3 px-5 py-4"><span className={`mt-0.5 grid size-8 shrink-0 place-items-center rounded-full ${event.tone === "green" ? "bg-emerald-50 text-emerald-700" : event.tone === "amber" ? "bg-amber-50 text-amber-700" : "bg-blue-50 text-blue-700"}`}><FileCheck2 className="size-4" /></span><div className="min-w-0 flex-1"><p className="text-sm font-medium">{event.label}</p><p className="mt-1 text-xs text-slate-500">{event.serviceName} · {new Date(event.timestamp).toLocaleString()}</p></div><Link href={`/applications/${event.applicationId}/workspace`} aria-label={`Open ${event.serviceName}`} className="rounded-lg p-2 text-slate-400 hover:bg-slate-50 hover:text-blue-700"><ArrowRight className="size-4" /></Link></div>)}</div> : <div className="px-5 py-7 text-sm text-slate-500">No recent updates yet. Once you start an application, you&apos;ll see its progress here.</div>}
      </Card>
      <Card className="flex flex-col justify-between bg-[#0b1c30] text-white"><div><div className="flex items-center gap-2 text-blue-200"><ShieldCheck className="size-4" /><span className="text-xs font-semibold uppercase tracking-wide">Your workspace</span></div><h2 className="mt-4 text-lg font-semibold">Secure, clear, and in your control.</h2><p className="mt-2 text-sm leading-6 text-slate-300">Review information before it is used. CivicFlow keeps your application progress on this device.</p></div><div className="mt-6 grid grid-cols-2 gap-3 border-t border-white/10 pt-4"><div><p className="text-2xl font-semibold tabular-nums">{applications.length}</p><p className="mt-1 text-xs text-slate-400">Saved applications</p></div><div><p className="text-2xl font-semibold tabular-nums">{pendingApprovals}</p><p className="mt-1 text-xs text-slate-400">Items needing review</p></div><Link href="/documents" className="col-span-2 mt-1 inline-flex items-center gap-2 text-sm font-semibold text-blue-200 hover:text-white"><UploadCloud className="size-4" />Manage your documents <ArrowRight className="size-4" /></Link></div></Card>
    </section>
  </div>
}
