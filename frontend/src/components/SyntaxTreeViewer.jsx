import React from "react";

const TreeNode = ({ label, details, children }) => {
  const childrenArray = React.Children.toArray(children);
  const hasChildren = childrenArray.length > 0;

  return (
    <div className="flex flex-col">
      {/* Node Content Card */}
      <div className="bg-slate-800/60 border border-slate-700/80 rounded-lg px-4 py-2.5 text-sm text-cyan-300 inline-block min-w-[160px] shadow-md backdrop-blur-sm">
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
        <div className="flex flex-col mt-3">
          {childrenArray.map((child, index) => {
            const isLast = index === childrenArray.length - 1;
            return (
              <div key={index} className="flex items-stretch">
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
      <div className="space-y-3 w-full">
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
      <div key={key} className="flex flex-col items-start w-full">
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

export default function SyntaxTreeViewer({ tree }) {
  if (!tree) return null;

  return (
    <div className="bg-slate-900 text-slate-100 p-6 rounded-xl overflow-auto max-h-[850px] shadow-2xl border border-slate-800 selection:bg-cyan-500/20">
      <div className="inline-block p-1">
        <RenderAST node={tree} />
      </div>
    </div>
  );
}
