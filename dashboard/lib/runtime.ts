import { headers } from "next/headers";

export function runtimeOrigin() {
  const origin = new URL(process.env.BUSINESSOS_API_URL ?? "http://127.0.0.1:8790");
  if (!(origin.protocol === "https:" || (origin.protocol === "http:" && ["127.0.0.1", "localhost", "[::1]"].includes(origin.hostname)))) throw new Error("Runtime must use HTTPS or loopback");
  if (origin.username || origin.password || origin.pathname !== "/" || origin.search || origin.hash) throw new Error("Invalid runtime origin");
  return origin.origin;
}

export async function runtimeFetch(path: string, init?: RequestInit) {
  const role = (await headers()).get("x-businessos-role");
  if (role !== "owner" && role !== "reviewer") throw new Error("Authentication required");
  const token = role === "reviewer" ? process.env.BUSINESSOS_REVIEWER_TOKEN : process.env.BUSINESSOS_OWNER_TOKEN;
  if (!token) throw new Error("Runtime authentication missing");
  return fetch(`${runtimeOrigin()}${path}`, { ...init, cache: "no-store", signal: AbortSignal.timeout(30000), headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` } });
}
