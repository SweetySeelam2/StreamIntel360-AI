type Props = {
  title: string;
  body: string;
};

export default function AnalysisCard({ title, body }: Props) {
  return (
    <div className="border rounded-md p-4 bg-white shadow-sm">
      <h2 className="text-xl font-semibold mb-2">{title}</h2>
      <div className="prose max-w-none whitespace-pre-wrap">
        {body}
      </div>
    </div>
  );
}