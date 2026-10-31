"""Service registry endpoints — serves the service catalog to the frontend."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from civicflow_contracts.application import CategoryInfo, ServiceDetail, ServiceListItem
from civicflow_contracts.common import ServiceCategory, ServiceStatus

router = APIRouter()

# Static service catalog — mirrors the frontend's serviceCatalog.ts
_SERVICE_CATALOG: list[dict] = [
    {
        "id": "post-matric-scholarship",
        "title": "Post-Matric Scholarship",
        "category": ServiceCategory.education,
        "description": "Financial assistance for eligible students studying after Class 10.",
        "jurisdiction": "Maharashtra",
        "department": "Maharashtra Government",
        "official_url": "https://mahadbt.maharashtra.gov.in",
        "status": ServiceStatus.available,
        "workflow_steps": ["Eligibility", "Profile", "Documents", "Portal Login", "Form", "Review"],
        "eligibility_criteria": ["UG and PG students", "Maharashtra domicile", "Family income criteria apply"],
        "required_documents": ["Aadhaar Card", "Income Certificate", "Previous Marksheet"],
    },
    {
        "id": "merit-scholarship",
        "title": "Merit Scholarship",
        "category": ServiceCategory.education,
        "description": "Support for students with a strong academic record.",
        "jurisdiction": "Maharashtra",
        "department": "State Education Department",
        "status": ServiceStatus.coming_soon,
        "eligibility_criteria": ["Merit-based eligibility"],
        "required_documents": ["Marksheet", "Student ID"],
    },
    {
        "id": "income-certificate",
        "title": "Income Certificate",
        "category": ServiceCategory.certificates,
        "description": "Request an official certificate of annual family income.",
        "jurisdiction": "Maharashtra",
        "department": "Revenue Department",
        "status": ServiceStatus.information_only,
        "workflow_steps": ["Service Requirements", "Profile", "Documents", "Portal Login", "Form", "Review"],
        "required_documents": ["Aadhaar Card", "Address Proof", "Income Proof"],
    },
    {
        "id": "domicile-certificate",
        "title": "Domicile Certificate",
        "category": ServiceCategory.certificates,
        "description": "Understand requirements for proving state residence.",
        "jurisdiction": "Maharashtra",
        "department": "Revenue Department",
        "status": ServiceStatus.information_only,
        "required_documents": ["Identity Proof", "Address Proof"],
    },
    {
        "id": "driving-license-renewal",
        "title": "Driving Licence Renewal",
        "category": ServiceCategory.licenses,
        "description": "Renew an existing driving licence through the transport portal.",
        "jurisdiction": "India",
        "department": "Ministry of Road Transport and Highways",
        "status": ServiceStatus.coming_soon,
        "workflow_steps": ["Existing Application", "Authentication", "Details", "Documents", "Review"],
        "required_documents": ["Existing Licence", "Medical Certificate"],
    },
    {
        "id": "housing-subsidy",
        "title": "Housing Subsidy",
        "category": ServiceCategory.benefits,
        "description": "Explore housing support and subsidy eligibility information.",
        "jurisdiction": "India",
        "department": "Housing and Urban Affairs",
        "status": ServiceStatus.information_only,
        "required_documents": ["Identity Proof", "Income Proof"],
    },
    {
        "id": "public-registration",
        "title": "Public Service Registration",
        "category": ServiceCategory.registrations,
        "description": "Discover department-specific registration processes.",
        "jurisdiction": "India",
        "department": "CivicFlow directory",
        "status": ServiceStatus.coming_soon,
    },
]

_CATEGORY_META = {
    "education": {"label": "Education & Scholarships", "description": "Scholarships, fee reimbursement, education grants and student benefits."},
    "certificates": {"label": "Certificates", "description": "Income, domicile, caste, birth and other official certificates."},
    "licenses": {"label": "Licenses & Permits", "description": "Driving, learner, trade and business permits."},
    "benefits": {"label": "Benefits & Subsidies", "description": "Government subsidies, welfare benefits, pensions and financial assistance."},
    "registrations": {"label": "Government Registrations", "description": "Public registrations and department-specific applications."},
    "other": {"label": "Other Services", "description": "Search for or describe another government service."},
}


@router.get("", response_model=list[ServiceListItem])
async def list_services(category: str | None = None, status: str | None = None):
    results = _SERVICE_CATALOG
    if category:
        results = [s for s in results if s["category"].value == category]
    if status:
        results = [s for s in results if s["status"].value == status]
    return [
        ServiceListItem(
            id=s["id"], title=s["title"], category=s["category"],
            description=s["description"], jurisdiction=s.get("jurisdiction"),
            department=s.get("department"), status=s["status"],
        )
        for s in results
    ]


@router.get("/categories", response_model=list[CategoryInfo])
async def list_categories():
    return [
        CategoryInfo(
            key=key,
            label=meta["label"],
            description=meta["description"],
            service_count=sum(1 for s in _SERVICE_CATALOG if s["category"].value == key),
        )
        for key, meta in _CATEGORY_META.items()
    ]


@router.get("/{service_id}", response_model=ServiceDetail)
async def get_service(service_id: str):
    for s in _SERVICE_CATALOG:
        if s["id"] == service_id:
            return ServiceDetail(
                id=s["id"], title=s["title"], category=s["category"],
                description=s["description"], jurisdiction=s.get("jurisdiction"),
                department=s.get("department"), status=s["status"],
                official_url=s.get("official_url"),
                workflow_steps=s.get("workflow_steps", []),
                eligibility_criteria=s.get("eligibility_criteria", []),
                required_documents=s.get("required_documents", []),
            )
    raise HTTPException(status_code=404, detail=f"Service '{service_id}' not found")
