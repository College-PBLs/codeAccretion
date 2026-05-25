export const prettyCode = (code = "") => {
  if (!code) return "";

  const expandedCode = code
    .replace(/;(?!(?:[^\(]*\)))/g, ";\n")
    .replace(/\{\s*/g, " {\n")
    .replace(/\}\s*/g, "\n}\n");

  const lines = expandedCode.split("\n");
  let indentLevel = 0;
  const formattedLines = [];

  for (let line of lines) {
    line = line.trim();
    if (!line) continue; // Skip empty structural gaps

    const openBraces = (line.match(/\{/g) || []).length;
    const closeBraces = (line.match(/\}/g) || []).length;

    if (line.startsWith("}")) {
      indentLevel = Math.max(0, indentLevel - 1);
    }

    const padding = " ".repeat(indentLevel * 4);
    formattedLines.push(padding + line);

    if (!line.startsWith("}")) {
      indentLevel += openBraces - closeBraces;
    } else {
      indentLevel += openBraces - (closeBraces - 1);
    }
    
    if (indentLevel < 0) indentLevel = 0;
  }

  return formattedLines.join("\n");
};
