export default function IntermediateViewer({ intermediate = {} }) {
  const lines = intermediate.three_address_code || [];
  
  return (
    <div className="glass max-h-72 overflow-auto font-mono text-sm">
      <div className="flex">
        {/* Line numbers column (SNO) */}
        <div className="flex-shrink-0 border-r border-slate-700/50 bg-slate-800/30">
          {lines.map((_, idx) => (
            <div key={idx} className="px-3 py-1 text-right text-slate-500 select-none">
              {idx + 1}
            </div>
          ))}
        </div>
        
        {/* Code column */}
        <div className="flex-1 overflow-x-auto">
          {lines.map((line, idx) => (
            <div key={idx} className="px-4 py-1 text-emerald-300 whitespace-pre">
              {line}
            </div>
          ))}
        </div>
      </div>
      
      {lines.length === 0 && (
        <div className="p-4 text-slate-400 italic text-center">
          No three address code generated
        </div>
      )}
    </div>
  );
}
