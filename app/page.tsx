'use client'

import { useState } from 'react'
import {
  ArrowRight, Bell, BookOpen, BriefcaseBusiness, Check, ChevronDown, ChevronRight,
  CircleHelp, ClipboardCheck, Clock3, FileCheck2, FileText, FolderOpen, GraduationCap,
  Home, Landmark, LayoutDashboard, LifeBuoy, ListChecks, Menu, MessageSquareText,
  MoreHorizontal, Paperclip, Plus, Search, Send, Settings, ShieldCheck, Sparkles,
  Upload, UserRound, WalletCards, X, Zap,
} from 'lucide-react'

const nav = [
  { label: 'Dashboard', icon: LayoutDashboard },
  { label: 'AI Assistant', icon: Sparkles },
  { label: 'Explore services', icon: CompassIcon },
  { label: 'My applications', icon: ClipboardCheck },
  { label: 'Documents', icon: FolderOpen },
  { label: 'Approvals', icon: FileCheck2 },
]
const tools = [
  { label: 'My profile', icon: UserRound },
  { label: 'Notifications', icon: Bell },
  { label: 'Settings', icon: Settings },
]
const services = [
  { title: 'Scholarships', desc: 'Find financial support for your education', icon: GraduationCap, tone: 'blue' },
  { title: 'Certificates', desc: 'Get income, caste & domicile certificates', icon: FileText, tone: 'teal' },
  { title: 'Licenses', desc: 'Apply for and renew official licenses', icon: BriefcaseBusiness, tone: 'purple' },
  { title: 'Subsidies', desc: 'Discover benefits you may be eligible for', icon: WalletCards, tone: 'amber' },
]
const applications = [
  { name: 'Post-Matric Scholarship', id: 'CF-2024-0892', status: 'In progress', progress: 68, updated: 'Updated 2 hours ago', icon: GraduationCap, color: '#3478e5' },
  { name: 'Income Certificate', id: 'CF-2024-0817', status: 'Needs review', progress: 42, updated: 'Updated yesterday', icon: FileText, color: '#277b78' },
]

function CompassIcon(props: any) { return <LifeBuoy {...props} /> }

export default function Page() {
  const [active, setActive] = useState('Dashboard')
  const [query, setQuery] = useState('')
  const [sent, setSent] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <div className="app-shell">
      <aside className={menuOpen ? 'sidebar sidebar-open' : 'sidebar'}>
        <div className="brand">
          <div className="brand-mark"><Landmark size={20} /></div>
          <div><div className="brand-name">CivicFlow</div><div className="brand-sub">Public service assistant</div></div>
          <button className="mobile-close" onClick={() => setMenuOpen(false)} aria-label="Close navigation"><X size={18} /></button>
        </div>
        <div className="side-label">Workspace</div>
        <nav className="nav-list">
          {nav.map(item => { const Icon = item.icon; return <button key={item.label} className={active === item.label ? 'nav-item active' : 'nav-item'} onClick={() => {setActive(item.label); setMenuOpen(false)}}><Icon size={18} /><span>{item.label}</span>{item.label === 'Approvals' && <span className="nav-count">2</span>}</button> })}
        </nav>
        <div className="side-label side-label-tools">Account</div>
        <nav className="nav-list">
          {tools.map(item => { const Icon = item.icon; return <button key={item.label} className="nav-item" onClick={() => setActive(item.label)}><Icon size={18} /><span>{item.label}</span>{item.label === 'Notifications' && <span className="dot" />}</button> })}
        </nav>
        <div className="sidebar-bottom">
          <div className="help-card"><div className="help-icon"><CircleHelp size={17}/></div><div><strong>Need help?</strong><span>Talk to CivicFlow AI</span></div><ChevronRight size={15}/></div>
          <div className="profile-row"><div className="avatar">AS</div><div className="profile-copy"><strong>Aarav Sharma</strong><span>Citizen account</span></div><MoreHorizontal size={18} className="muted-icon"/></div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <button className="menu-btn" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu size={20}/></button>
          <div className="breadcrumbs"><span>Workspace</span><ChevronRight size={14}/><strong>Dashboard</strong></div>
          <div className="top-actions"><button className="icon-btn" aria-label="Search"><Search size={19}/></button><button className="icon-btn notification" aria-label="Notifications"><Bell size={19}/><span /></button><button className="icon-btn" aria-label="Help"><CircleHelp size={19}/></button><div className="top-avatar">AS</div></div>
        </header>
        <div className="content">
          <section className="welcome-row"><div><div className="eyebrow"><span className="eyebrow-dot"/> YOUR PERSONAL SERVICE DESK</div><h1>Welcome back, Aarav</h1><p>Your public-service tasks, all in one place.</p></div><button className="outline-btn"><Clock3 size={16}/> View activity</button></section>

          <section className="hero-card">
            <div className="hero-copy"><div className="sparkle"><Sparkles size={17}/></div><div><h2>What can I help you with?</h2><p>Describe a government service you need. I’ll help you understand the requirements and get started.</p></div></div>
            <div className="prompt-box"><input value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => {if(e.key === 'Enter') setSent(true)}} placeholder="Tell CivicFlow what you need help with..." aria-label="Ask CivicFlow"/><button className="attach" aria-label="Attach a file"><Paperclip size={18}/></button><button className="send-btn" onClick={() => setSent(true)} aria-label="Send message"><Send size={17}/></button></div>
            {sent && <div className="sent-note"><Check size={15}/> Got it — I’ll help you explore that service. <button onClick={() => setSent(false)}>Dismiss</button></div>}
            <div className="suggestions"><span>Try asking</span><button onClick={() => setQuery('Find scholarships I may be eligible for')}>Find scholarships</button><button onClick={() => setQuery('I need an income certificate')}>Income certificate</button><button onClick={() => setQuery('Help me renew my driving license')}>Renew a license</button></div>
          </section>

          <section className="section-block"><div className="section-heading"><div><h2>Explore services</h2><p>Start with a popular public-service category</p></div><button className="text-btn" onClick={() => setActive('Explore services')}>View all <ArrowRight size={15}/></button></div><div className="service-grid">{services.map(({title, desc, icon: Icon, tone}) => <button className="service-card" key={title} onClick={() => setActive('Explore services')}><div className={'service-icon '+tone}><Icon size={20}/></div><div className="service-text"><h3>{title}</h3><p>{desc}</p></div><ChevronRight size={17} className="card-arrow"/></button>)}</div></section>

          <section className="stats-grid">{[['Active applications','2','+1 this month',ClipboardCheck,'blue'],['Pending approvals','2','Needs your attention',ShieldCheck,'amber'],['Completed tasks','12','+4 this month',Check,'green'],['Documents uploaded','8','All verified',FileCheck2,'purple']].map(([label, value, meta, Icon, tone]) => <div className="stat-card" key={label as string}><div className={'stat-icon '+tone}><Icon size={18}/></div><div><div className="stat-label">{label as string}</div><div className="stat-value">{value as string}</div><div className="stat-meta">{meta as string}</div></div><ChevronRight size={16} className="stat-arrow"/></div>)}</section>

          <section className="lower-grid"><div className="panel applications"><div className="panel-head"><div><h2>My applications</h2><p>Keep track of your active service requests</p></div><button className="icon-btn small"><Plus size={17}/></button></div><div className="application-list">{applications.map(app => {const Icon = app.icon; return <div className="application-row" key={app.id}><div className="app-icon" style={{background: app.color+'14', color: app.color}}><Icon size={19}/></div><div className="app-main"><div className="app-title-row"><strong>{app.name}</strong><span className={app.status === 'Needs review' ? 'status amber-status' : 'status blue-status'}>{app.status}</span></div><div className="app-id">{app.id} <span>•</span> {app.updated}</div><div className="progress-line"><div><span style={{width: app.progress+'%', background: app.color}}/></div><b>{app.progress}%</b></div></div><ChevronRight size={17} className="muted-icon"/></div>})}</div><button className="panel-footer" onClick={() => setActive('My applications')}>View all applications <ArrowRight size={15}/></button></div>
          <div className="panel activity"><div className="panel-head"><div><h2>Recent activity</h2><p>Your latest CivicFlow updates</p></div><button className="text-btn">See all</button></div><div className="activity-list"><Activity icon={Check} color="green" title="Document verified" detail="Income certificate was verified" time="Today, 10:24 AM"/><Activity icon={MessageSquareText} color="purple" title="AI assistant paused" detail="Waiting for your approval" time="Yesterday, 4:16 PM"/><Activity icon={Upload} color="blue" title="Document uploaded" detail="Aarav_Sharma_Marksheet.pdf" time="Mon, 2:08 PM"/></div></div></section>
          <div className="demo-disclaimer"><ShieldCheck size={15}/><span><strong>Demonstration workspace.</strong> CivicFlow is showing sample data for this prototype. No government portal activity or submission is taking place.</span></div>
        </div>
      </main>
    </div>
  )
}

function Activity({icon: Icon, color, title, detail, time}: {icon: any, color: string, title: string, detail: string, time: string}) { return <div className="activity-row"><div className={'activity-icon '+color}><Icon size={15}/></div><div className="activity-copy"><strong>{title}</strong><span>{detail}</span></div><time>{time}</time></div> }
