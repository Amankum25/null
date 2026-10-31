"use client"

import { FormEvent, useState } from "react"
import Link from "next/link"
import { Bot, Info, Send, Sparkles, ArrowRight } from "lucide-react"
import { useCivicFlow } from "@/lib/civicflow-store"
import { Button, Card, PageHeader, Status } from "@/components/page-primitives"
import { serviceCatalog } from "@/src/data/serviceCatalog"

export default function AssistantPage() {
  const { state, update } = useCivicFlow()
  const [text, setText] = useState("")

  function send(event: FormEvent) {
    event.preventDefault()
    const question = text.trim()
    if (!question) return

    // Deterministic catalog lookup for transparent fallback
    const qLower = question.toLowerCase()
    const matched = serviceCatalog.filter((s) => {
      const matchText = [s.title, s.description, s.jurisdiction, ...(s.aliases || [])].join(" ").toLowerCase()
      return matchText.includes(qLower) || (qLower.includes("scholarship") && s.category === "education") || (qLower.includes("certificate") && s.category === "certificates")
    }).slice(0, 3)

    let reply = "The deep reasoning AI pipeline is currently pending Member 2's LangGraph integration. In the meantime, I can guide you to confirmed services in our catalog:"
    if (matched.length > 0) {
      reply = `Based on your request "${question}", here are relevant public services in our catalog:\n` +
        matched.map((m) => `• ${m.title} (${m.jurisdiction}): ${m.description}`).join("\n")
    }

    update({
      chat: [
        ...state.chat,
        { role: "user", text: question },
        { role: "assistant", text: reply },
      ],
    })
    setText("")
  }

  return (
    <>
      <PageHeader
        title="CivicFlow Assistant"
        description="Guidance for finding public services, understanding eligibility, and navigating government portals."
        action={<Status tone="blue">Manual Guidance Mode</Status>}
      />

      <div className="mb-5 flex items-start gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900">
        <Info className="size-5 shrink-0 text-amber-700" />
        <div>
          <strong className="font-semibold text-amber-900">AI Reasoning Service Boundary:</strong> Member 2 is implementing the LangGraph RAG, eligibility, and form reasoning graphs. The assistant currently provides deterministic guidance and verified catalog referrals. Sensitive credentials (passwords, OTPs, CAPTCHAs) are never processed by AI.
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
        <Card className="flex min-h-[540px] flex-col">
          <div className="flex items-center gap-3 border-b border-[#e9e1d5] pb-4">
            <div className="grid size-10 place-items-center rounded-full bg-[#08785e] text-white">
              <Bot className="size-5" />
            </div>
            <div>
              <p className="font-bold text-[#10272b]">CivicFlow Public Service Guide</p>
              <p className="text-xs text-[#60756f]">Deterministic catalog guidance · Member 2 AI pending</p>
            </div>
          </div>

          <div className="flex flex-1 flex-col gap-4 overflow-auto py-5">
            {state.chat.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={`max-w-[85%] whitespace-pre-line rounded-2xl px-4 py-3 text-sm ${
                  message.role === "user"
                    ? "ml-auto bg-[#08785e] text-white"
                    : "bg-[#f7f5ee] text-[#10272b] border border-[#e9e1d5]"
                }`}
              >
                {message.text}
              </div>
            ))}
          </div>

          <form onSubmit={send} className="flex gap-2 border-t border-[#e9e1d5] pt-4">
            <label className="sr-only" htmlFor="assistant-message">
              Message
            </label>
            <input
              id="assistant-message"
              value={text}
              onChange={(event) => setText(event.target.value)}
              placeholder="Ask about a certificate, scholarship, or license..."
              className="min-w-0 flex-1 rounded-xl border border-[#d9cfc0] bg-white px-4 py-3 text-sm outline-none focus:border-[#08785e] focus:ring-2 focus:ring-[#e3f2e8]"
            />
            <button
              aria-label="Send message"
              className="grid size-11 place-items-center rounded-xl bg-[#08785e] text-white hover:bg-[#065f4a] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#08785e]"
            >
              <Send className="size-4" />
            </button>
          </form>
        </Card>

        <div className="space-y-4">
          <Card>
            <div className="flex items-center gap-2 font-bold text-[#10272b]">
              <Sparkles className="size-4 text-[#08785e]" /> Common Inquiries
            </div>
            <div className="mt-4 flex flex-col gap-2">
              {[
                "Income Certificate",
                "Caste Certificate in Bihar",
                "Driving Licence Renewal",
                "Post-Matric Scholarship",
                "Aadhaar Address Update",
              ].map((item) => (
                <Button key={item} variant="secondary" onClick={() => setText(item)}>
                  {item}
                </Button>
              ))}
            </div>
          </Card>

          <Card>
            <h3 className="font-bold text-sm text-[#10272b]">Need a Custom Service?</h3>
            <p className="mt-1 text-xs text-[#60756f]">
              If a service is not in our direct catalog, tell us the requirement and state to create a custom application.
            </p>
            <div className="mt-3">
              <Button href="/services/custom" variant="secondary" className="w-full justify-center">
                Custom Service Request <ArrowRight className="ml-1 size-3.5" />
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </>
  )
}
