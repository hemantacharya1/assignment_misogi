import { useEffect, useState } from "react";
import TicketForm from "../components/TicketForm";
import TicketList from "../components/TicketList";
import { fetchTickets } from "../api/api";

export default function Home() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    fetchTickets().then(setTickets).catch(console.error);
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-4">
      <TicketForm onSubmit={(newTicket) => setTickets([newTicket, ...tickets])} />
      <TicketList tickets={tickets} />
    </div>
  );
}
