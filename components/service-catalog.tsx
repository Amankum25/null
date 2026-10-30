"use client"
import Link from "next/link"
import { ArrowRight, Building2, CheckCircle2, FileCheck, FileText, Grid2X2, HandCoins, IdCard, Search, GraduationCap, Info } from "lucide-react"
import { useEffect, useMemo, useState } from "react"
import { categoryMeta, serviceCatalog, type Service, type ServiceCategory, type ServiceStatus } from "@/src/data/serviceCatalog"
import { Button, Card, Status } from "@/components/page-primitives"

const icons = { education: GraduationCap, certificates: FileCheck, licenses: IdCard, benefits: HandCoins, registrations: Building2, other: Grid2X2 }
const statusLabels: Record<ServiceStatus, string> = { available: "Available", coming_soon: "Coming soon", information_only: "Information only" }
const statusTone: Record<ServiceStatus, "green" | "amber" | "blue"> = { available: "green", coming_soon: "amber", information_only: "blue" }

export function ServiceCard({ service }: { service: Service }) {
  return <Card className="flex h-full flex-col transition hover:-translate-y-0.5 hover:border-blue-300"><div className="flex items-start justify-between gap-3"><div className="grid size-11 place-items-center rounded-xl bg-blue-50 text-blue-600"><FileText className="size-5" /></div><Status tone={statusTone[service.status]}>{statusLabels[service.status]}</Status></div><h2 className="mt-5 text-lg font-bold">{service.title}</h2><p className="mt-1 text-sm text-slate-500">{service.description}</p><p className="mt-4 text-xs text-slate-500">{service.department ?? "Government department"} · {service.jurisdiction ?? "India"}</p><Link href={`/services/${service.id}`} className="mt-auto pt-6"><Button variant="secondary">View service <ArrowRight className="ml-2 size-4" /></Button></Link></Card>
}

export function CategoryIcon({ category }: { category: ServiceCategory }) { const Icon = icons[category]; return <Icon className="size-6" /> }

export function ServiceDirectory() {
  const [query, setQuery] = useState(""); const [category, setCategory] = useState("all");
  useEffect(() => { const requestedCategory = new URLSearchParams(window.location.search).get("category"); if (requestedCategory) setCategory(requestedCategory) }, []); const [status, setStatus] = useState("all"); const [department, setDepartment] = useState("all")
  const departments = useMemo(() => Array.from(new Set(serviceCatalog.map((service) => service.department).filter(Boolean))), [])
  const results = serviceCatalog.filter((service) => { const matchesQuery = `${service.title} ${service.description} ${service.department}`.toLowerCase().includes(query.toLowerCase()); return matchesQuery && (category === "all" || service.category === category) && (status === "all" || service.status === status) && (department === "all" || service.department === department) })
  return <div className="flex flex-col gap-5"><div className="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 md:grid-cols-[1.5fr_1fr_1fr_1fr]"><label className="relative"><span className="sr-only">Search services</span><Search className="absolute left-3 top-3 size-4 text-slate-400" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search services..." className="w-full rounded-xl border border-slate-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-blue-400" /></label><select value={category} onChange={(event) => setCategory(event.target.value)} className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm"><option value="all">All categories</option>{Object.entries(categoryMeta).slice(0, 5).map(([key, value]) => <option key={key} value={key}>{value.label}</option>)}</select><select value={status} onChange={(event) => setStatus(event.target.value)} className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm"><option value="all">All availability</option><option value="available">Available</option><option value="coming_soon">Coming soon</option><option value="information_only">Information only</option></select><select value={department} onChange={(event) => setDepartment(event.target.value)} className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm"><option value="all">All departments</option>{departments.map((item) => <option key={item} value={item}>{item}</option>)}</select></div><p className="text-sm text-slate-500">Showing {results.length} services from the CivicFlow catalogue.</p>{results.length ? <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">{results.map((service) => <ServiceCard key={service.id} service={service} />)}</div> : <Card><Info className="size-5 text-blue-600" /><p className="mt-3 font-semibold">No services found</p><p className="mt-1 text-sm text-slate-500">Try a different search or filter.</p></Card>}</div>
}
