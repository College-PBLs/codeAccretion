import React from "react";

const TreeNode = ({ label, details, children }) => {
  const childrenArray = React.Children.toArray(children);
  const hasChildren = childrenArray.length > 0;

  return (
    <div className="flex flex-col items-start w-max">
      {/* Node Content Card */}
      <div className="bg-slate-800/60 border border-slate-700/80 rounded-lg px-4 py-2.5 text-sm text-cyan-300 inline-block min-w-[200px] shadow-md backdrop-blur-sm">
        <div className="font-bold text-cyan-400 font-mono tracking-wide">{label}</div>
        
        {details && details.length > 0 && (
          <div className="text-xs text-slate-300 mt-2 pt-2 border-t border-slate-700/60 space-y-1 font-mono">
            {details.map((detail, idx) => (
              <div key={idx} className="flex justify-between gap-6">
                <span className="text-slate-500">{detail.key}:</span>{" "}
                <span className="text-emerald-400 font-semibold">{detail.value}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Children Subtree */}
      {hasChildren && (
        <div className="flex flex-col mt-3 w-full">
          {childrenArray.map((child, index) => {
            const isLast = index === childrenArray.length - 1;
            return (
              <div key={index} className="flex items-stretch w-full">
                {/* Visual Branch Connectors */}
                <div className="flex flex-col items-center w-8 relative flex-shrink-0">
                  {/* Vertical Line Anchor */}
                  {!isLast ? (
                    <div className="absolute top-0 bottom-0 left-4 w-px bg-slate-700" />
                  ) : (
                    <div className="absolute top-0 h-5 left-4 w-px bg-slate-700" />
                  )}
                  {/* Horizontal Stub Line */}
                  <div className="absolute top-5 left-4 w-4 h-px bg-slate-700" />
                </div>

                {/* Subtree Node Content wrapper */}
                <div className="flex-1 pb-3">{child}</div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

const RenderAST = ({ node }) => {
  if (node === null || node === undefined) return null;

  // Handle Primitives
  if (typeof node !== "object") {
    return <TreeNode label={String(node)} details={[]} />;
  }

  // Handle Arrays smoothly
  if (Array.isArray(node)) {
    return (
      <div className="space-y-3 w-max">
        {node.map((item, index) => (
          <RenderAST key={index} node={item} />
        ))}
      </div>
    );
  }

  const nodeType = node.type || "Node";
  const details = [];
  const childProps = {};
  const excludedFromDetails = ["type"];

  Object.entries(node).forEach(([key, value]) => {
    if (value === null || value === undefined) return;

    const isPrimitive =
      typeof value === "string" ||
      typeof value === "number" ||
      typeof value === "boolean";

    if (isPrimitive && !excludedFromDetails.includes(key)) {
      let displayValue = value;
      if (typeof value === "boolean") displayValue = value ? "true" : "false";
      details.push({ key, value: String(displayValue) });
    } else if (!isPrimitive) {
      childProps[key] = value;
    }
  });

  // Structural Adjustments for Literals
  if (nodeType === "Literal" && node.value !== undefined) {
    const valueType = node.value_type || typeof node.value;
    if (!details.some((d) => d.key === "value")) {
      details.push({ key: "value", value: String(node.value) });
    }
    if (!details.some((d) => d.key === "value_type" || d.key === "type")) {
      details.push({ key: "value_type", value: valueType });
    }
  }

  // Generate branch blocks matching property keys (BODY, MODIFIERS, etc.)
  const childrenElements = Object.entries(childProps)
    .filter(([_, value]) => value !== null && value !== undefined && (!Array.isArray(value) || value.length > 0))
    .map(([key, value]) => (
      <div key={key} className="flex flex-col items-start w-max">
        {/* Branch Header label */}
        <div className="text-[10px] text-slate-500 font-bold tracking-wider uppercase ml-1 mb-1 font-mono">
          {key}
        </div>
        <RenderAST node={value} />
      </div>
    ));

  return (
    <TreeNode label={nodeType} details={details}>
      {childrenElements}
    </TreeNode>
  );
};

const FunctionTreeNode = ({ functionName, functionData }) => {
  const details = [
    { key: "return_type", value: functionData.return_type },
    { key: "modifiers", value: functionData.modifiers?.join(", ") || "none" },
    { key: "parameters", value: functionData.parameters?.map(p => `${p.type} ${p.name}`).join(", ") || "none" }
  ];

  return (
    <TreeNode label={`${functionName}()`} details={details}>
      {functionData.body && functionData.body.length > 0 && (
        <div className="flex flex-col items-start w-max">
          <div className="text-[10px] text-slate-500 font-bold tracking-wider uppercase ml-1 mb-1 font-mono">
            BODY
          </div>
          <div className="space-y-3 w-max pl-4 relative">
            {/* Vertical line for body container */}
            <div className="absolute left-2 top-0 bottom-0 w-px bg-slate-700/50" />
            {functionData.body.map((stmt, idx) => (
              <div key={idx} className="relative">
                <RenderAST node={stmt} />
              </div>
            ))}
          </div>
        </div>
      )}
    </TreeNode>
  );
};

const SymbolTableViewer = ({ symbolTable }) => {
  if (!symbolTable || Object.keys(symbolTable).length === 0) {
    return <div className="text-slate-400 italic">No symbols defined</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-collapse">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-2 px-3 text-cyan-400 font-mono text-xs uppercase tracking-wider">SNO</th>
            <th className="text-left py-2 px-3 text-cyan-400 font-mono text-xs uppercase tracking-wider">Variable Name</th>
            <th className="text-left py-2 px-3 text-cyan-400 font-mono text-xs uppercase tracking-wider">Data Type</th>
            <th className="text-left py-2 px-3 text-cyan-400 font-mono text-xs uppercase tracking-wider">Scope</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(symbolTable).map(([name, type], idx) => (
            <tr key={name} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
              <td className="py-2 px-3 font-mono text-sm text-slate-400">{idx + 1}</td>
              <td className="py-2 px-3 font-mono text-sm text-emerald-400">{name}</td>
              <td className="py-2 px-3 font-mono text-sm">
                <span className={`px-2 py-0.5 rounded text-xs font-mono ${
                  type === "int" ? "bg-blue-500/20 text-blue-300" :
                  type === "float" ? "bg-green-500/20 text-green-300" :
                  type === "double" ? "bg-purple-500/20 text-purple-300" :
                  type === "boolean" ? "bg-amber-500/20 text-amber-300" :
                  type === "String" ? "bg-rose-500/20 text-rose-300" :
                  type === "String[]" ? "bg-indigo-500/20 text-indigo-300" :
                  "bg-slate-500/20 text-slate-300"
                }`}>
                  {type}
                </span>
              </td>
              <td className="py-2 px-3 font-mono text-sm text-violet-400">local</td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <div className="mt-3 pt-2 text-xs text-slate-500 font-mono">
        Total symbols: {Object.keys(symbolTable).length}
      </div>
    </div>
  );
};

const ErrorListViewer = ({ errors }) => {
  if (!errors || errors.length === 0) {
    return <div className="text-emerald-400 text-sm">✓ No errors detected</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-collapse">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-2 px-3 text-rose-400 font-mono text-xs uppercase tracking-wider">SNO</th>
            <th className="text-left py-2 px-3 text-rose-400 font-mono text-xs uppercase tracking-wider">Error Message</th>
          </tr>
        </thead>
        <tbody>
          {errors.map((error, idx) => (
            <tr key={idx} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
              <td className="py-2 px-3 font-mono text-sm text-slate-400">{idx + 1}</td>
              <td className="py-2 px-3 font-mono text-sm text-rose-300">{error}</td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <div className="mt-3 pt-2 text-xs text-slate-500 font-mono">
        Total errors: {errors.length}
      </div>
    </div>
  );
};

export default function SemanticViewer({ semantic = {} }) {
  const [activeTab, setActiveTab] = React.useState("symbols");

  const tabs = [
    { id: "symbols", label: "Symbol Table", count: Object.keys(semantic.symbol_table || {}).length },
    { id: "functions", label: "Functions", count: Object.keys(semantic.functions || {}).length },
    { id: "errors", label: "Errors", count: semantic.errors?.length || 0 }
  ];

  return (
    <div className="space-y-4">
      {/* Status Header */}
      <div className="flex items-center justify-between p-3 bg-slate-800/40 rounded-lg border border-slate-700/50">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${semantic.status === "Passed" ? "bg-emerald-400 animate-pulse" : "bg-rose-400"}`} />
          <span className="text-slate-300 text-sm">Status:</span>
          <span className={`font-mono font-bold ${semantic.status === "Passed" ? "text-emerald-400" : "text-rose-400"}`}>
            {semantic.status || "N/A"}
          </span>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-1 border-b border-slate-700">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 text-sm font-mono transition-all rounded-t-lg ${
              activeTab === tab.id
                ? "bg-slate-800/80 text-cyan-400 border-t border-x border-slate-700"
                : "text-slate-400 hover:text-slate-300 hover:bg-slate-800/40"
            }`}
          >
            {tab.label}
            {tab.count > 0 && (
              <span className={`ml-2 px-1.5 py-0.5 text-xs rounded ${
                activeTab === tab.id ? "bg-cyan-500/20 text-cyan-300" : "bg-slate-700/50 text-slate-400"
              }`}>
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="glass p-4 rounded-lg border border-slate-700/50 min-h-[400px] max-h-[600px] overflow-auto">
        {activeTab === "symbols" && (
          <div className="space-y-2">
            <h3 className="text-sm font-mono text-cyan-400 mb-3">Symbol Table</h3>
            <SymbolTableViewer symbolTable={semantic.symbol_table} />
          </div>
        )}

        {activeTab === "functions" && (
          <div className="space-y-3">
            <h3 className="text-sm font-mono text-cyan-400 mb-3">Function Definitions</h3>
            <div className="space-y-4">
              {Object.entries(semantic.functions || {}).map(([funcName, funcData]) => (
                <FunctionTreeNode key={funcName} functionName={funcName} functionData={funcData} />
              ))}
              {Object.keys(semantic.functions || {}).length === 0 && (
                <div className="text-slate-400 italic">No functions defined</div>
              )}
            </div>
          </div>
        )}

        {activeTab === "errors" && (
          <div className="space-y-2">
            <h3 className="text-sm font-mono text-rose-400 mb-3">Error List</h3>
            <ErrorListViewer errors={semantic.errors} />
          </div>
        )}
      </div>
    </div>
  );
}
