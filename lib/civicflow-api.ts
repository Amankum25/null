"use client";

const baseUrl = process.env.NEXT_PUBLIC_CORE_API_URL?.replace(/\/$/, "");

export const isCoreApiConfigured = Boolean(baseUrl);

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!baseUrl) throw new Error("Core API is not configured");
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
  });
  if (!response.ok) throw new Error(`Core API request failed (${response.status})`);
  return response.json() as Promise<T>;
}

export type CustomApplicationInput = {
  request_text: string;
  state_code: string;
  district?: string;
  department_id?: string;
  additional_context?: Record<string, unknown>;
};

export function createCoreCustomApplication(input: CustomApplicationInput) {
  return request<{ application_id: string; status: string; message: string }>("/api/v1/applications/custom", {
    method: "POST", body: JSON.stringify(input),
  });
}

export function listCoreServices(params: Record<string, string | undefined> = {}) {
  const query = new URLSearchParams(Object.entries(params).filter(([, value]) => Boolean(value)) as string[][]);
  return request<Array<Record<string, unknown>>>(`/api/v1/services${query.size ? `?${query}` : ""}`);
}
