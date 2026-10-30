"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Bell, Bot, BriefcaseBusiness, CheckCircle2, FileText, LayoutDashboard, Menu, Settings, UserRound, X } from "lucide-react"
import { useState, type ReactNode } from "react"
import { CivicFlowProvider, useCivicFlow } from "@/lib/civicflow-store"

const nav = [
  ["Dashboard", "/dashboard", LayoutDashboard], ["AI Assistant", "/assistant", Bot], ["Explore Services", "/services", BriefcaseBusiness], ["My Applications", "/applications", FileText], ["Documents", "/documents", FileText], ["Approvals", "/approvals", CheckCircle2], ["Notifications", "/notifications", Bell], ["Profile", "/profile", UserRound], ["Settings", "/settings", Settings],
] as const
function ShellInner({ children }: { children: ReactNode }) {
  const pathname = usePathname(); const [open, setOpen] = useState(false); const { state } = useCivicFlow()
  return <div className="min-h-screen bg-[#f7f9fe] text-slate-900">
    <button aria-label="Open navigation" onClick={() => setOpen(true)} className="fixed left-4 top-4 z-30 rounded-lg bg-[#102451] p-2 text-white shadow-lg lg:hidden"><Menu /></button>
    {open && <button aria-label="Close navigation" className="fixed inset-0 z-30 bg-slate-950/40 lg:hidden" onClick={() => setOpen(false)} />}
    <aside className={`fixed inset-y-0 left-0 z-40 flex w-64 flex-col bg-[#102451] px-4 py-5 text-white transition-transform lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}>
      <div className="mb-8 flex items-center justify-between px-2"><Link href="/dashboard" className="flex items-center gap-2 text-lg font-bold"><span className="grid size-9 place-items-center rounded-xl bg-blue-500">CF</span>CivicFlow</Link><button aria-label="Close navigation" onClick={() => setOpen(false)} className="lg:hidden"><X /></button></div>
      <nav className="flex flex-col gap-1">{nav.map(([label, href, Icon]) => <Link key={href} href={href} onClick={() => setOpen(false)} className={`flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition ${pathname === href || (href !== "/dashboard" && pathname.startsWith(href + "/")) ? "bg-blue-500 text-white" : "text-blue-100/75 hover:bg-white/10 hover:text-white"}`}><Icon className="size-4" />{label}</Link>)}</nav>
      <div className="mt-auto rounded-2xl bg-white/10 p-3"><div className="flex items-center gap-3"><div className="grid size-9 place-items-center rounded-full bg-blue-400 font-semibold">AP</div><div className="min-w-0"><p className="truncate text-sm font-semibold">{state.user.name}</p><p className="text-xs text-blue-100/60">Student account</p></div></div></div>
    </aside>
    <main className="min-h-screen lg:pl-64"><div className="mx-auto max-w-7xl px-4 py-6 pt-20 sm:px-6 lg:px-8 lg:pt-8">{children}</div></main>
  </div>
}
export default function AppShell({ children }: { children: ReactNode }) { return <CivicFlowProvider><ShellInner>{children}</ShellInner></CivicFlowProvider> }
