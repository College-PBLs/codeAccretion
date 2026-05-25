import { useState, useRef, useEffect } from "react";
import Split from "react-split";
import { Copy, Eraser, Play, Sparkles } from "lucide-react";
import CodeEditor from "../components/CodeEditor";
import OutputConsole from "../components/OutputConsole";
import Loader from "../components/Loader";
import TokenTable from "../components/TokenTable";
import SyntaxTreeViewer from "../components/SyntaxTreeViewer";
import SemanticViewer from "../components/SemanticViewer";
import IntermediateViewer from "../components/IntermediateViewer";
import { SAMPLE } from "../data/constants";
import { prettyCode } from "../utils/format";
import { runCode, transpileCode } from "../services/api";

const tabs = ["Tokens", "Syntax Tree", "Semantic", "Intermediate"];

export default function TranspilePage({
  sourceLanguage = "java",
  targetLanguage = "cpp",
  toast,
  dark,
}) {
  const [src, setSrc] = useState(SAMPLE[sourceLanguage]);
  const [out, setOut] = useState("");
  const [leftRun, setLeftRun] = useState("");
  const [rightRun, setRightRun] = useState("");
  const [data, setData] = useState({});
  const [tab, setTab] = useState("Tokens");

  // Individual loading states for each async action
  const [isTranspiling, setIsTranspiling] = useState(false);
  const [isRunningSource, setIsRunningSource] = useState(false);
  const [isRunningTarget, setIsRunningTarget] = useState(false);

  const targetEditorRef = useRef(null);
  const sourceEditorRef = useRef(null);

  // Reset everything when sourceLanguage or targetLanguage changes (page switch)
  useEffect(() => {
    const sampleCode = SAMPLE[sourceLanguage] || "";
    setSrc(sampleCode);
    if (sourceEditorRef.current) {
      sourceEditorRef.current.setValue(sampleCode);
    }

    setOut("");
    if (targetEditorRef.current) {
      targetEditorRef.current.setValue("");
    }

    setLeftRun("");
    setRightRun("");
    setData({});
    setTab("Tokens");
  }, [sourceLanguage, targetLanguage]);

  // Clear editors when component unmounts (e.g., navigating to home page)
  useEffect(() => {
    return () => {
      setSrc("");
      setOut("");
    };
  }, []);

  const onTranspile = async () => {
    setIsTranspiling(true);
    try {
      const res = await transpileCode({
        source_language: sourceLanguage,
        target_language: targetLanguage,
        code: src,
      });
      const g = res.generated_code || {};
      setData(g);

      const formattedOutput = prettyCode(g.generated_code || "");
      setOut(formattedOutput);
      
      requestAnimationFrame(() => {
        sourceEditorRef.current?.layout();
        targetEditorRef.current?.layout();
      });

      toast("success", "Transpilation successful");
    } catch (e) {
      toast("error", e.message);
    } finally {
      setIsTranspiling(false);
    }
  };

  const onRun = async (lang, code, setter, setLoading) => {
    setLoading(true);
    try {
      const r = await runCode({ language: lang, code });
      setter(r);
    } catch (e) {
      setter({ error: e.message });
    } finally {
      setLoading(false);
    }
  };

  const clearSource = () => {
    setSrc("");
    if (sourceEditorRef.current) {
      sourceEditorRef.current.setValue("");
    }
  };

  const clearTarget = () => {
    setOut("");
    if (targetEditorRef.current) {
      targetEditorRef.current.setValue("");
    }
  };

  const clearAll = () => {
    clearSource();
    clearTarget();
    toast("info", "Both editors cleared");
  };

  const copySource = () => {
    navigator.clipboard.writeText(src);
    toast("info", "Source code copied to clipboard");
  };

  const copyTarget = () => {
    navigator.clipboard.writeText(out);
    toast("info", "Generated code copied to clipboard");
  };

  return (
    <div>
      <div className="mb-4 flex flex-wrap gap-2">
        <button
          className="glass px-3 py-2"
          onClick={() => setSrc(SAMPLE[sourceLanguage])}
        >
          Sample
        </button>
        <button className="glass px-3 py-2" onClick={clearAll}>
          <Eraser className="inline h-4 w-4 mr-1" /> Clear All
        </button>
      </div>

      <div className="grid gap-4 md:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-start w-full">
        {/* Left Panel: Source Input */}
        <div className="min-w-0">
          <div className="mb-2 flex items-center justify-between gap-2 flex-wrap">
            <h2 className="font-semibold">{sourceLanguage.toUpperCase()} Input</h2>
            <div className="flex gap-2">
              <button
                className="glass px-2 py-1 text-xs"
                onClick={copySource}
                title="Copy source code"
              >
                <Copy className="inline h-3.5 w-3.5 mr-1" /> Copy
              </button>
              <button
                className="glass px-2 py-1 text-xs"
                onClick={clearSource}
                title="Clear source code"
              >
                <Eraser className="inline h-3.5 w-3.5 mr-1" /> Clear
              </button>
              <button
                className="glass px-3 py-1 text-sm flex items-center gap-1 disabled:opacity-50"
                onClick={() => onRun(sourceLanguage, src, setLeftRun, setIsRunningSource)}
                disabled={isRunningSource}
              >
                {isRunningSource ? (
                  <Loader />
                ) : (
                  <>
                    <Play className="inline h-4 w-4" /> Run
                  </>
                )}
              </button>
            </div>
          </div>
          <CodeEditor
            darkMode={dark}
            language={sourceLanguage}
            value={src}
            onChange={(v) => setSrc(v || "")}
            formatCode={prettyCode}
            editorRef={sourceEditorRef}
          />
          <OutputConsole title="Source Run Output" output={leftRun} />
        </div>

        {/* Center Column: Transpile Trigger Action */}
        <div className="flex md:flex-col justify-center items-center h-full py-4 md:pt-32">
          <button
            className="glass px-4 py-3 bg-cyan-600/20 hover:bg-cyan-600/40 text-cyan-200 border border-cyan-500/30 flex items-center gap-2 rounded-lg font-medium shadow-lg transition-all disabled:opacity-50"
            onClick={onTranspile}
            disabled={isTranspiling}
          >
            {isTranspiling ? (
              <Loader />
            ) : (
              <>
                <Sparkles className="h-5 w-5" />
                <span className="hidden md:inline">Transpile</span>
              </>
            )}
          </button>
        </div>

        {/* Right Panel: Target Output */}
        <div className="min-w-0">
          <div className="mb-2 flex items-center justify-between gap-2 flex-wrap">
            <h2 className="font-semibold">{targetLanguage.toUpperCase()} Output</h2>
            <div className="flex gap-2">
              <button
                className="glass px-2 py-1 text-xs"
                onClick={copyTarget}
                title="Copy generated code"
              >
                <Copy className="inline h-3.5 w-3.5 mr-1" /> Copy
              </button>
              <button
                className="glass px-2 py-1 text-xs"
                onClick={clearTarget}
                title="Clear generated code"
              >
                <Eraser className="inline h-3.5 w-3.5 mr-1" /> Clear
              </button>
              <button
                className="glass px-3 py-1 text-sm flex items-center gap-1 disabled:opacity-50"
                onClick={() => onRun(targetLanguage, out, setRightRun, setIsRunningTarget)}
                disabled={isRunningTarget}
              >
                {isRunningTarget ? (
                  <Loader />
                ) : (
                  <>
                    <Play className="inline h-4 w-4" /> Run
                  </>
                )}
              </button>
            </div>
          </div>
          <CodeEditor
            darkMode={dark}
            language={targetLanguage}
            value={out}
            onChange={setOut}
            editorRef={targetEditorRef}
            readOnly
          />
          <OutputConsole title="Target Run Output" output={rightRun} />
        </div>
      </div>

      {/* Analysis Tabs */}
      <section className="glass mt-6 p-4">
        <div className="mb-3 flex flex-wrap gap-2">
          {tabs.map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`rounded-lg px-3 py-1 text-sm ${tab === t ? "bg-cyan-500/30" : "bg-slate-200 dark:bg-slate-800"}`}
            >
              {t}
            </button>
          ))}
        </div>
        {tab === "Tokens" && <TokenTable tokens={data.tokens || []} />}
        {tab === "Syntax Tree" && <SyntaxTreeViewer tree={data.syntax_tree} />}
        {tab === "Semantic" && <SemanticViewer semantic={data.semantic_result} />}
        {tab === "Intermediate" && <IntermediateViewer intermediate={data.intermediate_code || {}} />}
      </section>
    </div>
  );
}
