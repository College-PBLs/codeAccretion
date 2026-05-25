export default function TokenTable({ tokens = [] }) {
  return (
    <div className="overflow-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-slate-400 border-b border-slate-700">
            <th className="py-2 px-3">SNO</th>
            <th className="py-2 px-3">TYPE</th>
            <th className="py-2 px-3">VALUE</th>
            <th className="py-2 px-3">POSITION</th>
           </tr>
        </thead>
        <tbody>
          {tokens.map((t, i) => (
            <tr key={i} className="border-t border-slate-800 hover:bg-slate-800/30 transition-colors">
              <td className="py-2 px-3 text-slate-400 font-mono text-xs">{i + 1}</td>
              <td className="py-2 px-3">
                <span className={`px-2 py-0.5 rounded text-xs font-mono ${
                  t.type === "KEYWORD" ? "bg-purple-500/20 text-purple-300" :
                  t.type === "IDENTIFIER" ? "bg-emerald-500/20 text-emerald-300" :
                  t.type === "LITERAL" ? "bg-amber-500/20 text-amber-300" :
                  t.type === "OPERATOR" ? "bg-blue-500/20 text-blue-300" :
                  t.type === "PUNCTUATION" ? "bg-rose-500/20 text-rose-300" :
                  "bg-slate-500/20 text-slate-300"
                }`}>
                  {t.type}
                </span>
              </td>
              <td className="py-2 px-3 font-mono text-sm text-cyan-300">{t.value}</td>
              <td className="py-2 px-3 font-mono text-xs text-slate-400">{t.position}</td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {tokens.length === 0 && (
        <div className="p-8 text-center text-slate-400 italic">
          No tokens generated yet
        </div>
      )}
      
      {tokens.length > 0 && (
        <div className="mt-3 pt-2 text-xs text-slate-500 font-mono">
          Total tokens: {tokens.length}
        </div>
      )}
    </div>
  );
}
