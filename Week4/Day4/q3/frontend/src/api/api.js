const BASE_URL = "http://localhost:8000"; // change if deployed

export async function createTicket(data) {
  const res = await fetch(`${BASE_URL}/tickets`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create ticket");
  return await res.json();
}

export async function fetchTickets() {
  const res = await fetch(`${BASE_URL}/tickets`);
  if (!res.ok) throw new Error("Failed to fetch tickets");
  return await res.json();
}
