"use client"

import Link from "next/link"
import { useParams } from "next/navigation"
import { ArrowRight, FileText } from "lucide-react"
import { useCivicFlow } from "@/lib/civicflow-store"
import { serviceCatalog } from "@/src/data/serviceCatalog"
import { BrowserViewer } from "@/components/browser-viewer"
import { Button, Card, PageHeader, Status } from "@/components/page-primitives"

export default function WorkspacePage() {
  const params=useParams<{id:string}>();const {getApplication,updateApplication}=useCivicFlow();const application=getApplication(params.id)
  if(!application)return <Card><p className="font-bold">Application not found</p><p className="mt-2 text-sm text-slate-500">This application ID is not in your account.</p><Button href="/applications">Back to applications</Button></Card>
  const service=serviceCatalog.find(item=>item.id===application.serviceId);const title=service?.title??application.customRequest??"Custom service request"
  const openForm=()=>updateApplication(application.id,{currentStep:Math.max(application.currentStep,1),progress:Math.max(application.progress,25)})
  return <><PageHeader eyebrow={application.applicationMode==="custom"?"Custom application workspace":"Application workspace"} title={title} description={application.applicationMode==="custom"?`${application.customState??"Jurisdiction not set"}${application.customDistrict?` · ${application.customDistrict}`:""} · Source verification required`:`${service?.department??"Government service"} · ${service?.jurisdiction??"India"}`} action={<Status tone={application.status==="submitted"?"green":"amber"}>{application.status.replaceAll("_"," ")}</Status>}/><div className="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-[#e9e1d5] bg-[#fffefb] px-4 py-3 text-sm"><span className="text-[#60756f]">Application ID: <strong className="text-[#10272b]">{application.id}</strong></span><Link href={service?`/services/${service.id}`:"/services/custom"} className="font-semibold text-[#08785e]">{service?"View service details":"Review discovery details"}</Link></div><BrowserViewer applicationId={application.id} activities={application.activity}/><Card className="mt-4 flex flex-wrap items-center justify-between gap-4"><div className="flex items-center gap-3"><FileText className="size-6 text-[#08785e]"/><div><p className="font-semibold text-[#10272b]">Continue your application</p><p className="mt-1 text-xs text-[#60756f]">Your information is saved to this application only.</p></div></div><div className="flex flex-wrap gap-2"><Button href={`/applications/${application.id}/form`} onClick={openForm}>Edit details <ArrowRight className="ml-2 size-4"/></Button><Button href={`/applications/${application.id}/review`} variant="secondary">Review</Button></div></Card></>
}
