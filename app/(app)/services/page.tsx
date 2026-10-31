import { Suspense } from "react"
import { PageHeader } from "@/components/page-primitives"
import { ServiceDirectory } from "@/components/service-catalog"
export default function ServicesPage() { return <><PageHeader title="Explore services" description="Browse the CivicFlow catalogue, or search for a government service that is not listed. Other Services is a directory entry point, not a claim that every service is supported." /><Suspense fallback={<div className="h-40 rounded-2xl border border-slate-200 bg-white" />}><ServiceDirectory /></Suspense></> }
