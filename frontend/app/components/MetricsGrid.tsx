type Metric = {
  label: string;
  value: string | number;
  hint?: string;
};

type Props = {
  metrics: Metric[];
};

export default function MetricsGrid({ metrics }: Props) {
  if (!metrics || metrics.length === 0) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
      {metrics.map((m, idx) => (
        <div
          key={idx}
          className="border rounded-md p-3 bg-black/5 flex flex-col"
        >
          <span className="text-xs uppercase text-gray-500 mb-1">
            {m.label}
          </span>
          <span className="text-lg font-semibold">{m.value}</span>
          {m.hint && (
            <span className="text-xs text-gray-500 mt-1">{m.hint}</span>
          )}
        </div>
      ))}
    </div>
  );
}