"use client"

import { useRouter } from "next/navigation"
import { useEffect, useState } from "react"
import { ArrowRight, Search } from "lucide-react"
import { serviceCatalog, type ServiceCategory } from "@/src/data/serviceCatalog"
import { useCivicFlow } from "@/lib/civicflow-store"
import { Button, Card, PageHeader, Status } from "@/components/page-primitives"

export default function NewApplicationPage() {
  const router = useRouter(); const { createApplication } = useCivicFlow(); const [requested, setRequested] = useState<string | null>(null)
  const [category, setCategory] = useState<ServiceCategory | "all">("all"); const [query, setQuery] = useState("")
  useEffect(() => { setRequested(new URLSearchParams(window.location.search).get("service")) }, [])
  const services = serviceCatalog.filter((service) => service.status === "available" && (category === "all" || service.category === category) && `${service.title} ${service.description}`.toLowerCase().includes(query.toLowerCase()))
  const start = (serviceId: string) => { const application = createApplication(serviceId); if (application) router.push(`/applications/${application.id}/workspace`) }
  return <><PageHeader eyebrow="New application" title="What service do you need?" description="Choose an available service to create a new application. Each application gets its own workspace and progress." /><Card className="mb-5"><div className="flex flex-col gap-3 md:flex-row"><label className="relative flex-1"><span className="sr-only">Search available services</span><Search className="absolute left-3 top-3 size-4 text-slate-400" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search available services..." className="w-full rounded-xl border border-slate-200 py-2.5 pl-9 pr-3 text-sm" /></label><select value={category} onChange={(event) => setCategory(event.target.value as ServiceCategory | "all")} className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm"><option value="all">All categories</option><option value="education">Education</option><option value="certificates">Certificates</option><option value="licenses">Licenses</option><option value="benefits">Benefits</option><option value="registrations">Registrations</option></select></div></Card><div className="grid gap-5 md:grid-cols-2">{services.map((service) => <Card key={service.id}><div className="flex items-start justify-between gap-3"><div><Status tone="green">Available</Status><h2 className="mt-3 text-lg font-bold">{service.title}</h2><p className="mt-2 text-sm text-slate-500">{service.description}</p></div></div><p className="mt-4 text-xs text-slate-500">{service.department} · {service.jurisdiction}</p><Button onClick={() => start(service.id)} className="mt-5">Start application<ArrowRight className="ml-2 size-4" /></Button></Card>)}{requested && !services.some((service) => service.id === requested) && <Card><p className="font-semibold">That service is not currently available for guided applications.</p><Button href={`/services/${requested}`} variant="secondary" className="mt-4">Explore service details</Button></Card>}</div></>
}
