export default function OutputConsole({ title, output }) {
  const consoleText = output?.output?.output || "No output yet";

  return (
    <div className="glass mt-3 p-3">
      <p className="text-xs text-slate-400">{title}</p>

      <pre className="mt-2 overflow-auto text-sm text-emerald-300 whitespace-pre-wrap">
        {consoleText}
      </pre>
    </div>
  );
}
