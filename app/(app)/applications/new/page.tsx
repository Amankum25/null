"use client"

import { useMemo, useState } from "react"
import { useRouter } from "next/navigation"
import { ArrowRight, Award, Building2, FileCheck2, FileText, GraduationCap, HandCoins, IdCard, Search } from "lucide-react"
import { categoryMeta, serviceCatalog, type ServiceCategory } from "@/src/data/serviceCatalog"
import { useCivicFlow } from "@/lib/civicflow-store"
import { Button, Card, PageHeader, Status } from "@/components/page-primitives"

const categories: { id: ServiceCategory; icon: typeof GraduationCap }[] = [
  { id: "education", icon: GraduationCap },
  { id: "certificates", icon: FileCheck2 },
  { id: "licenses", icon: IdCard },
  { id: "benefits", icon: HandCoins },
  { id: "registrations", icon: Building2 },
  { id: "other", icon: Award },
]

export default function NewApplicationPage() {
  const router = useRouter()
  const { createApplication } = useCivicFlow()
  const [query, setQuery] = useState("")
  const results = useMemo(() => serviceCatalog.filter((service) => `${service.title} ${service.description} ${service.department ?? ""}`.toLowerCase().includes(query.trim().toLowerCase())), [query])
  const start = (serviceId: string) => { const application = createApplication(serviceId); if (application) router.push(`/applications/${application.id}/workspace`) }
  return <>
    <PageHeader eyebrow="New application" title="What service do you need?" description="Choose a category or search for a government service to get started." />
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {categories.map(({ id, icon: Icon }) => { const meta = categoryMeta[id]; const isOther = id === "other"; return <button key={id} type="button" onClick={() => router.push(isOther ? "/services" : `/services?category=${id}`)} className="group text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 rounded-2xl"><Card className="h-full transition group-hover:-translate-y-0.5 group-hover:border-blue-300 group-focus-visible:border-blue-400"><div className="flex items-start justify-between gap-4"><div className="grid size-12 place-items-center rounded-2xl bg-blue-50 text-blue-600 transition group-hover:bg-blue-600 group-hover:text-white"><Icon className="size-6" /></div><ArrowRight className="size-5 text-slate-300 transition group-hover:translate-x-1 group-hover:text-blue-600" /></div><h2 className="mt-5 text-lg font-bold text-slate-950">{meta.label}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{meta.description}</p></Card></button> })}
    </div>
    <Card className="mt-6"><div className="flex items-center gap-3"><div className="grid size-10 place-items-center rounded-xl bg-blue-50 text-blue-600"><Search className="size-5" /></div><div><h2 className="font-bold">Search all services</h2><p className="text-sm text-slate-500">Find a specific service without choosing a category first.</p></div></div><label className="relative mt-5 block"><span className="sr-only">Search services</span><Search className="absolute left-3 top-3 size-4 text-slate-400" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search services, certificates, scholarships..." className="h-11 w-full rounded-xl border border-slate-200 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" /></label>{query && <div className="mt-4 grid gap-3 md:grid-cols-2">{results.length ? results.map((service) => <div key={service.id} className="flex items-center gap-3 rounded-xl border border-slate-200 p-3"><FileText className="size-5 shrink-0 text-blue-600" /><div className="min-w-0 flex-1"><p className="truncate text-sm font-semibold">{service.title}</p><p className="text-xs text-slate-500">{service.department}</p></div>{service.status === "available" ? <Button className="shrink-0" onClick={() => start(service.id)}>Start<ArrowRight className="ml-1 size-3" /></Button> : <Status tone="amber">{service.status === "coming_soon" ? "Coming soon" : "Info only"}</Status>}</div>) : <p className="text-sm text-slate-500">No services match that search.</p>}</div>}</Card>
  </>
}
