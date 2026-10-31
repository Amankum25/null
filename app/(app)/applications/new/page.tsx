"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { ArrowRight, Search, X } from "lucide-react"
import { useState } from "react"
import { PageHeader, Card, Button } from "@/components/page-primitives"
import { categoryMeta, serviceCatalog, type ServiceCategory } from "@/src/data/serviceCatalog"
import { CategoryIcon } from "@/components/service-catalog"
import { useCivicFlow } from "@/lib/civicflow-store"

const categories: ServiceCategory[] = ["education", "certificates", "licenses", "benefits", "registrations", "other"]

export default function NewApplicationPage() {
  const router = useRouter()
  const { createApplication } = useCivicFlow()
  const [query, setQuery] = useState("")
  const shown = query ? serviceCatalog.filter((item) => `${item.title} ${item.description}`.toLowerCase().includes(query.toLowerCase())) : []
  const start = (serviceId: string) => { const application = createApplication(serviceId); if (application) router.push(`/applications/${application.id}/workspace`) }

  return <>
    <PageHeader eyebrow="New application" title="What service do you need?" description="Choose any government or public-service process. CivicFlow will guide you through it." />
    <div className="relative mb-7 max-w-3xl"><Search className="absolute left-4 top-3.5 size-5 text-slate-400" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search for certificates, scholarships, licenses, subsidies..." className="w-full rounded-2xl border border-slate-200 bg-white px-12 py-3.5 text-sm shadow-sm outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100" aria-label="Search government services" />{query && <button type="button" onClick={() => setQuery("")} aria-label="Clear service search" className="absolute right-4 top-3 rounded-md p-1 text-slate-400 hover:text-slate-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"><X className="size-4" /></button>}{query && shown.length === 0 && <div className="absolute inset-x-0 top-14 z-10 rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600 shadow-xl">No services match “{query}”. <button type="button" onClick={() => setQuery("")} className="font-semibold text-blue-600 underline">Clear search</button></div>}{shown.length > 0 && <div className="absolute inset-x-0 top-14 z-10 rounded-2xl border border-slate-200 bg-white p-2 shadow-xl">{shown.map((service) => <div key={service.id} className="flex items-center justify-between rounded-xl px-3 py-3 hover:bg-blue-50"><span><strong className="block text-sm">{service.title}</strong><span className="text-xs text-slate-500">{categoryMeta[service.category].label}</span></span>{service.status === "available" ? <Button onClick={() => start(service.id)} className="py-2">Start<ArrowRight className="ml-2 size-4" /></Button> : <Link href={`/services/${service.id}`} className="rounded-lg p-2 text-blue-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500" aria-label={`View ${service.title}`}><ArrowRight className="size-4" /></Link>}</div>)}</div>}</div>
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{categories.map((category) => { const meta = categoryMeta[category]; const count = serviceCatalog.filter((service) => service.category === category).length; return <Link key={category} href={category === "other" ? "/services" : `/services?category=${category}`} className="group block h-full rounded-2xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"><Card className="h-full transition duration-200 group-hover:-translate-y-1 group-hover:border-blue-300 group-hover:shadow-md"><div className="flex items-start justify-between"><div className="grid size-12 place-items-center rounded-2xl bg-blue-50 text-blue-600"><CategoryIcon category={category} /></div><ArrowRight className="size-5 text-slate-300 transition group-hover:text-blue-600" /></div><h2 className="mt-5 text-lg font-bold">{meta.label}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{meta.description}</p>{count > 0 && <p className="mt-4 text-xs font-semibold text-blue-600">{count} listed services</p>}<span className="mt-5 inline-flex text-sm font-semibold text-blue-600">Explore services <ArrowRight className="ml-2 size-4" /></span></Card></Link>})}</div>
  </>
}
