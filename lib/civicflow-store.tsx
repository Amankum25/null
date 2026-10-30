"use client"

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react"

type DocumentItem = { id: string; name: string; type: string; status: "pending" | "verified" }
type ChatMessage = { role: "user" | "assistant"; text: string }
type CivicFlowState = {
  user: { name: string; email: string; phone: string; location: string }
  selectedService: string | null
  selectedScholarship: string | null
  applicationStatus: string
  documents: DocumentItem[]
  chat: ChatMessage[]
  form: { applicantName: string; fatherName: string; income: string; dob: string; category: string }
  aiPaused: boolean
  userControl: boolean
  review: Record<string, boolean>
}
const initialState: CivicFlowState = {
  user: { name: "Aarav Patil", email: "aarav@example.com", phone: "+91 98765 43210", location: "Pune, Maharashtra" },
  selectedService: null, selectedScholarship: null, applicationStatus: "In progress",
  documents: [{ id: "aadhaar", name: "Aadhaar Card", type: "PDF", status: "verified" }, { id: "income", name: "Income Certificate", type: "PDF", status: "pending" }, { id: "marksheet", name: "Previous Marksheet", type: "PDF", status: "verified" }],
  chat: [{ role: "assistant", text: "Hello Aarav. I can help you discover services, check eligibility, and complete applications." }],
  form: { applicantName: "Aarav Patil", fatherName: "Rajesh Patil", income: "₹2,00,000", dob: "12/03/2004", category: "OBC" },
  aiPaused: false, userControl: false, review: { personal: true, education: true, financial: false, documents: false },
}
const StoreContext = createContext<{ state: CivicFlowState; update: (patch: Partial<CivicFlowState>) => void } | null>(null)
export function CivicFlowProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState(initialState)
  useEffect(() => { const saved = window.localStorage.getItem("civicflow-demo"); if (saved) setState({ ...initialState, ...JSON.parse(saved) }) }, [])
  useEffect(() => { window.localStorage.setItem("civicflow-demo", JSON.stringify(state)) }, [state])
  const value = useMemo(() => ({ state, update: (patch: Partial<CivicFlowState>) => setState((current) => ({ ...current, ...patch })) }), [state])
  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}
export function useCivicFlow() { const value = useContext(StoreContext); if (!value) throw new Error("useCivicFlow must be used inside CivicFlowProvider"); return value }
