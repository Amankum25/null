export type ServiceStatus = "available" | "coming_soon" | "information_only"
export type ServiceCategory = "education" | "certificates" | "licenses" | "benefits" | "registrations" | "other"

export interface Service {
  id: string
  title: string
  category: ServiceCategory
  description: string
  jurisdiction?: string
  department?: string
  officialUrl?: string
  status: ServiceStatus
  workflowSteps?: string[]
  eligibility?: string[]
  documents?: string[]
  aliases?: string[]
}

export const serviceCatalog: Service[] = [
  { id: "post-matric-scholarship", title: "Post-Matric Scholarship", category: "education", description: "Financial assistance for eligible students studying after Class 10.", jurisdiction: "Maharashtra", department: "Maharashtra Government", officialUrl: "https://mahadbt.maharashtra.gov.in", status: "available", workflowSteps: ["Eligibility", "Profile", "Documents", "Portal Login", "Form", "Review"], eligibility: ["UG and PG students", "Maharashtra domicile", "Family income criteria apply"], documents: ["Aadhaar Card", "Income Certificate", "Previous Marksheet"] },
  { id: "merit-scholarship", title: "Merit Scholarship", category: "education", description: "Support for students with a strong academic record.", jurisdiction: "Maharashtra", department: "State Education Department", status: "coming_soon", eligibility: ["Merit-based eligibility"], documents: ["Marksheet", "Student ID"] },
  { id: "income-certificate", title: "Income Certificate", category: "certificates", description: "Request an official certificate of annual family income.", jurisdiction: "Maharashtra", department: "Revenue Department", status: "information_only", workflowSteps: ["Service Requirements", "Profile", "Documents", "Portal Login", "Form", "Review"], documents: ["Aadhaar Card", "Address Proof", "Income Proof"] },
  { id: "domicile-certificate", title: "Domicile Certificate", category: "certificates", description: "Understand requirements for proving state residence.", jurisdiction: "Maharashtra", department: "Revenue Department", status: "information_only", documents: ["Identity Proof", "Address Proof"] },
  { id: "driving-license-renewal", title: "Driving Licence Renewal", category: "licenses", description: "Renew an existing driving licence through the transport portal.", jurisdiction: "India", department: "Ministry of Road Transport and Highways", status: "coming_soon", workflowSteps: ["Existing Application", "Authentication", "Details", "Documents", "Review"], documents: ["Existing Licence", "Medical Certificate"] },
  { id: "housing-subsidy", title: "Housing Subsidy", category: "benefits", description: "Explore housing support and subsidy eligibility information.", jurisdiction: "India", department: "Housing and Urban Affairs", status: "information_only", documents: ["Identity Proof", "Income Proof"] },
  { id: "public-registration", title: "Public Service Registration", category: "registrations", description: "Discover department-specific registration processes.", jurisdiction: "India", department: "CivicFlow directory", status: "coming_soon" },
]

export const categoryMeta = {
  education: { label: "Education & Scholarships", description: "Scholarships, fee reimbursement, education grants and student benefits." },
  certificates: { label: "Certificates", description: "Income, domicile, caste, birth and other official certificates." },
  licenses: { label: "Licenses & Permits", description: "Driving, learner, trade and business permits." },
  benefits: { label: "Benefits & Subsidies", description: "Government subsidies, welfare benefits, pensions and financial assistance." },
  registrations: { label: "Government Registrations", description: "Public registrations and department-specific applications." },
  other: { label: "Other Services", description: "Search for or describe another government service." },
} as const
