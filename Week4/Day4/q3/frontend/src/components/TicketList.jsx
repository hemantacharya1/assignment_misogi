export default function TicketList({ tickets }) {
    return (
      <div className="mt-6 space-y-4">
        {tickets.map((t) => (
          <div key={t.id} className="bg-white shadow p-4 rounded border">
            <h3 className="font-bold text-lg">{t.title}</h3>
            <p className="text-gray-700">{t.description}</p>
            <p className="mt-2 text-sm text-gray-500">Category: {t.auto_category} | Priority: {t.priority}</p>
            <p className="text-sm text-gray-500">Tags: {t.tags}</p>
            <div className="mt-2 p-2 bg-gray-100 rounded">
              <p className="text-sm whitespace-pre-wrap">{t.generated_response}</p>
            </div>
          </div>
        ))}
      </div>
    );
  }
  