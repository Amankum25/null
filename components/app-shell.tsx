"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import {
  Bell,
  Bot,
  BriefcaseBusiness,
  CheckCircle2,
  CircleHelp,
  FileText,
  Landmark,
  LayoutDashboard,
  Menu,
  Search,
  Settings,
  UserRound,
  X,
} from "lucide-react"
import { useState, type FormEvent, type ReactNode } from "react"
import { CivicFlowProvider, useCivicFlow } from "@/lib/civicflow-store"

const nav = [
  ["Dashboard", "/dashboard", LayoutDashboard],
  ["AI Assistant", "/assistant", Bot],
  ["Explore Services", "/services", BriefcaseBusiness],
  ["My Applications", "/applications", FileText],
  ["Documents", "/documents", FileText],
  ["Approvals", "/approvals", CheckCircle2],
  ["Notifications", "/notifications", Bell],
  ["Settings", "/settings", Settings],
] as const

function ShellInner({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const [query, setQuery] = useState("")
  const { state } = useCivicFlow()
  const firstName = state.user.name.split(" ")[0]
  const initials = state.user.name.split(" ").map((part) => part[0]).slice(0, 2).join("").toUpperCase()

  function search(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const value = query.trim()
    router.push(value ? `/services?query=${encodeURIComponent(value)}` : "/services")
  }

  return (
    <div className="min-h-screen bg-[#f7f8fc] text-[#0b1c30]">
      {open && <button aria-label="Close navigation" className="fixed inset-0 z-30 bg-slate-950/40 lg:hidden" onClick={() => setOpen(false)} />}
      <aside className={`fixed inset-y-0 left-0 z-40 flex w-[236px] flex-col bg-[#0b1c30] px-4 py-5 text-white transition-transform lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="mb-7 flex items-center justify-between px-1">
          <Link href="/dashboard" onClick={() => setOpen(false)} className="flex items-center gap-3">
            <span className="grid size-10 place-items-center rounded-xl bg-blue-600"><Landmark className="size-5" /></span>
            <span><strong className="block text-base leading-tight">CivicFlow</strong><span className="text-[11px] text-slate-300">AI Civic Workspace</span></span>
          </Link>
          <button aria-label="Close navigation" onClick={() => setOpen(false)} className="rounded-lg p-2 text-slate-300 hover:bg-white/10 lg:hidden"><X className="size-5" /></button>
        </div>

        <Link href="/applications/new" onClick={() => setOpen(false)} className="mb-6 inline-flex h-10 items-center justify-center gap-2 rounded-lg bg-blue-600 text-sm font-semibold text-white transition hover:bg-blue-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-300">
          <span className="text-lg leading-none">+</span> New application
        </Link>

        <nav aria-label="Main navigation" className="flex flex-col gap-1">
          {nav.map(([label, href, Icon]) => {
            const active = pathname === href || (href !== "/dashboard" && pathname.startsWith(`${href}/`))
            return <Link key={href} href={href} onClick={() => setOpen(false)} aria-current={active ? "page" : undefined} className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] font-medium transition ${active ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-white/10 hover:text-white"}`}>
              <Icon className="size-[18px]" />{label}
              {label === "Notifications" && <span className="ml-auto size-2 rounded-full bg-blue-400" />}
            </Link>
          })}
        </nav>

        <div className="mt-auto border-t border-white/10 pt-4">
          <Link href="/profile" onClick={() => setOpen(false)} className="flex items-center gap-3 rounded-xl px-2 py-2 hover:bg-white/10">
            <span className="grid size-9 shrink-0 place-items-center rounded-full bg-blue-100 text-xs font-bold text-blue-800">{initials}</span>
            <span className="min-w-0"><strong className="block truncate text-xs">{state.user.name}</strong><span className="block text-[11px] text-slate-400">Verified citizen</span></span>
            <UserRound className="ml-auto size-4 text-slate-400" />
          </Link>
          <div className="mt-3 flex items-center justify-between px-2 text-[10px] text-slate-400"><span>Public portal v3.4</span><span className="flex items-center gap-1.5"><i className="size-1.5 rounded-full bg-emerald-400" />Live</span></div>
        </div>
      </aside>

      <div className="min-h-screen lg:pl-[236px]">
        <header className="sticky top-0 z-20 flex h-[68px] items-center gap-3 border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:px-6 lg:px-8">
          <button aria-label="Open navigation" onClick={() => setOpen(true)} className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden"><Menu className="size-5" /></button>
          <form onSubmit={search} className="relative w-full max-w-[430px]">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
            <input value={query} onChange={(event) => setQuery(event.target.value)} aria-label="Search services" placeholder="Search services, forms, or application IDs…" className="h-10 w-full rounded-lg border border-slate-200 bg-white pl-10 pr-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-100" />
          </form>
          <div className="ml-auto flex items-center gap-2 sm:gap-3">
            <span className="hidden items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-[11px] text-slate-600 md:inline-flex"><CheckCircle2 className="size-3.5 text-blue-600" />Verified citizen</span>
            <Link href="/notifications" aria-label="Notifications" className="relative rounded-lg p-2 text-slate-600 hover:bg-slate-100"><Bell className="size-[18px]" /><i className="absolute right-1.5 top-1.5 size-1.5 rounded-full bg-red-500" /></Link>
            <Link href="/assistant" aria-label="Help and assistant" className="rounded-lg p-2 text-slate-600 hover:bg-slate-100"><CircleHelp className="size-[18px]" /></Link>
            <Link href="/profile" className="hidden items-center gap-2 border-l border-slate-200 pl-3 sm:flex">
              <span className="grid size-9 place-items-center rounded-full bg-blue-100 text-xs font-bold text-blue-800">{initials}</span>
              <span className="hidden xl:block"><strong className="block text-xs">{state.user.name}</strong><span className="text-[11px] text-slate-500">{firstName}&apos;s workspace</span></span>
            </Link>
          </div>
        </header>
        <main className="mx-auto min-h-[calc(100vh-68px)] max-w-[1600px] px-4 py-7 sm:px-6 lg:px-8 lg:py-8">{children}</main>
      </div>
    </div>
  )
}

export default function AppShell({ children }: { children: ReactNode }) {
  return <CivicFlowProvider><ShellInner>{children}</ShellInner></CivicFlowProvider>
}
