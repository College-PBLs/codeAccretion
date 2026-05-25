import { useRef } from "react";
import Editor from "@monaco-editor/react";

export default function CodeEditor({
  darkMode,
  language,
  value,
  onChange,
  readOnly = false,
  formatCode,
  editorRef,
}) {
  const internalEditorRef = useRef(null);

  const handleChange = (newValue) => {
    onChange?.(newValue || "");
  };

  const handleEditorDidMount = (editor, monaco) => {
    // Keep reference tracking clean
    internalEditorRef.current = editor;
    if (editorRef) {
      editorRef.current = editor;
    }

    // Auto format on paste
    editor.onDidPaste(() => {
      if (formatCode) {
        const formatted = formatCode(editor.getValue());
        onChange?.(formatted);
      }
    });

    // Keyboard shortcut for saving/formatting
    editor.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS,
      () => {
        if (formatCode) {
          const formatted = formatCode(editor.getValue());
          const position = editor.getPosition();
          editor.setValue(formatted);
          if (position) editor.setPosition(position);
          onChange?.(formatted);
        }
      }
    );
  };

  return (
    <div className="glass overflow-hidden rounded-xl border border-slate-700">
      <Editor
        height="360px"
        theme={darkMode ? "vs-dark" : "light"}
        language={language}
        value={value}
        onChange={handleChange}
        onMount={handleEditorDidMount}
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: "Fira Code, monospace",
          wordWrap: "on",
          automaticLayout: true,
          scrollBeyondLastLine: false,
          tabSize: 4,
          insertSpaces: true,
          detectIndentation: false,
          autoIndent: "full",
          formatOnPaste: true,
          formatOnType: false,
          smoothScrolling: true,
          cursorBlinking: "smooth",
          padding: { top: 12 },
        }}
      />
    </div>
  );
}
