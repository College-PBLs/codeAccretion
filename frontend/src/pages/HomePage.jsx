import { PHASES } from "../data/constants";
import CompilerPhaseCard from "../components/CompilerPhaseCard";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";

export default function HomePage({ isDark }) {
  const [currentPhase, setCurrentPhase] = useState(0);
  const [phaseData, setPhaseData] = useState(null);
  const [isConverting, setIsConverting] = useState(false);

  // Theme-aware colors - fixed for light theme
  const bg = isDark ? "#0f1623" : "#f8fafc";
  const surface = isDark ? "#1a2236" : "#ffffff";
  const surface2 = isDark ? "#1e2840" : "#f1f5f9";
  const border = isDark ? "rgba(255,255,255,0.07)" : "rgba(0,0,0,0.08)";
  const text = isDark ? "#e2e8f0" : "#0f172a";
  const textMuted = isDark ? "#64748b" : "#94a3b8";
  const textSub = isDark ? "#94a3b8" : "#475569";
  const accent = isDark ? "#818cf8" : "#4f46e5";
  const accentLight = isDark ? "#a5b4fc" : "#6366f1";
  const accentBg = isDark ? "rgba(129,140,248,0.12)" : "rgba(79,70,229,0.08)";
  const success = "#10b981";
  const warning = "#f59e0b";

  const sectionCard = {
    background: surface,
    border: `1px solid ${border}`,
    borderRadius: 16,
    padding: "1.75rem 2rem",
    marginBottom: "1.5rem",
  };

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-8 rounded-2xl border ${
          isDark
            ? "glass bg-gradient-to-br from-cyan-950/40 to-violet-950/40 border-slate-700"
            : "bg-gradient-to-br from-cyan-50 to-indigo-50 border-slate-200 shadow-sm"
        }`}
      >
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">
            <span
              className={
                isDark
                  ? "bg-gradient-to-r from-cyan-400 to-violet-400 bg-clip-text text-transparent"
                  : "bg-gradient-to-r from-cyan-600 to-indigo-600 bg-clip-text text-transparent"
              }
            >
              CodeAccretion
            </span>
          </h1>
          <p
            className={`text-xl mb-6 ${
              isDark ? "text-cyan-300" : "text-cyan-700"
            }`}
          >
            A Compiler Visualization Platform for Java ↔ C++ Transpilation
          </p>
          <p
            className={`${
              isDark ? "text-slate-400" : "text-slate-600"
            } leading-relaxed`}
          >
            CodeAccretion is a compiler visualization platform and transpiler
            that converts Java ↔ C++ while exposing every internal compilation
            phase including lexical analysis, syntax analysis, semantic
            analysis, intermediate representation, and code generation in real
            time.
          </p>
        </div>
      </motion.section>

      {/* Compiler Pipeline Visualizer */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className={`p-6 rounded-xl border ${
          isDark
            ? "bg-slate-800/50 border-slate-700 text-slate-100"
            : "bg-white border-slate-200 text-slate-900 shadow-sm"
        }`}
      >
        <h2
          className={`text-2xl font-semibold mb-6 ${
            isDark ? "text-white" : "text-slate-900"
          }`}
        >
          Compiler Pipeline Visualizer
        </h2>

        {/* Pipeline Visualization */}
        <div className="relative mb-8">
          <div className="flex flex-col items-center space-y-2 font-mono text-sm">
            {/* Source Code */}
            <div
              className={`font-semibold mb-2 ${
                isDark ? "text-cyan-400" : "text-cyan-700"
              }`}
            >
              Source Code (Java / C++)
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Lexical Analyzer */}
            <div
              className={`relative ${
                currentPhase >= 0
                  ? isDark
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500"
                    : "bg-gradient-to-r from-cyan-400/10 to-violet-400/10 border-cyan-500 shadow-sm"
                  : isDark
                  ? "bg-slate-700/30 border-slate-600"
                  : "bg-slate-100 border-slate-300"
              } border-2 rounded-lg p-3 w-64 text-center transition-all ${
                currentPhase === 0 && isConverting ? "animate-pulse" : ""
              }`}
            >
              <div
                className={`font-semibold ${
                  isDark ? "text-slate-200" : "text-slate-800"
                }`}
              >
                Lexical Analyzer
              </div>
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Token Stream */}
            <div
              className={`text-center ${
                isDark ? "text-yellow-400" : "text-yellow-700"
              }`}
            >
              Token Stream
              {phaseData?.artifacts?.tokens && currentPhase >= 0 && (
                <div
                  className={`text-xs mt-1 max-w-md ${
                    isDark ? "text-slate-400" : "text-slate-500"
                  }`}
                >
                  {phaseData.artifacts.tokens.slice(0, 8).join(", ")}...
                </div>
              )}
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Syntax Analyzer */}
            <div
              className={`relative ${
                currentPhase >= 0
                  ? isDark
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500"
                    : "bg-gradient-to-r from-cyan-400/10 to-violet-400/10 border-cyan-500 shadow-sm"
                  : isDark
                  ? "bg-slate-700/30 border-slate-600"
                  : "bg-slate-100 border-slate-300"
              } border-2 rounded-lg p-3 w-64 text-center transition-all ${
                currentPhase === 0 && isConverting ? "animate-pulse" : ""
              }`}
            >
              <div
                className={`font-semibold ${
                  isDark ? "text-slate-200" : "text-slate-800"
                }`}
              >
                Syntax Analyzer
              </div>
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Abstract Syntax Tree */}
            <div
              className={`text-center ${
                isDark ? "text-green-400" : "text-green-700"
              }`}
            >
              Abstract Syntax Tree
              {phaseData?.artifacts?.ast && currentPhase >= 1 && (
                <div
                  className={`text-xs mt-1 max-w-md ${
                    isDark ? "text-slate-400" : "text-slate-500"
                  }`}
                >
                  {phaseData.artifacts.ast.substring(0, 50)}...
                </div>
              )}
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Semantic Analyzer */}
            <div
              className={`relative ${
                currentPhase >= 0
                  ? isDark
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500"
                    : "bg-gradient-to-r from-cyan-400/10 to-violet-400/10 border-cyan-500 shadow-sm"
                  : isDark
                  ? "bg-slate-700/30 border-slate-600"
                  : "bg-slate-100 border-slate-300"
              } border-2 rounded-lg p-3 w-64 text-center transition-all ${
                currentPhase === 0 && isConverting ? "animate-pulse" : ""
              }`}
            >
              <div
                className={`font-semibold ${
                  isDark ? "text-slate-200" : "text-slate-800"
                }`}
              >
                Semantic Analyzer
              </div>
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Validated AST */}
            <div
              className={`text-center ${
                isDark ? "text-emerald-400" : "text-emerald-700"
              }`}
            >
              Validated AST
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Intermediate IR Generator */}
            <div
              className={`relative ${
                currentPhase >= 0
                  ? isDark
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500"
                    : "bg-gradient-to-r from-cyan-400/10 to-violet-400/10 border-cyan-500 shadow-sm"
                  : isDark
                  ? "bg-slate-700/30 border-slate-600"
                  : "bg-slate-100 border-slate-300"
              } border-2 rounded-lg p-3 w-64 text-center transition-all ${
                currentPhase === 0 && isConverting ? "animate-pulse" : ""
              }`}
            >
              <div
                className={`font-semibold ${
                  isDark ? "text-slate-200" : "text-slate-800"
                }`}
              >
                Intermediate Code Generator
              </div>
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Validated AST */}
            <div
              className={`text-center ${
                isDark ? "text-purple-400" : "text-purple-700"
              }`}
            >
              Three Address Code
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Code Generator */}
            <div
              className={`relative ${
                currentPhase >= 0
                  ? isDark
                    ? "bg-gradient-to-r from-cyan-500/20 to-violet-500/20 border-cyan-500"
                    : "bg-gradient-to-r from-cyan-400/10 to-violet-400/10 border-cyan-500 shadow-sm"
                  : isDark
                  ? "bg-slate-700/30 border-slate-600"
                  : "bg-slate-100 border-slate-300"
              } border-2 rounded-lg p-3 w-64 text-center transition-all ${
                currentPhase === 0 && isConverting ? "animate-pulse" : ""
              }`}
            >
              <div
                className={`font-semibold ${
                  isDark ? "text-slate-200" : "text-slate-800"
                }`}
              >
                Code Generator
              </div>
            </div>

            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              │
            </div>
            <div className={isDark ? "text-slate-500" : "text-slate-400"}>
              ▼
            </div>

            {/* Target Language Code */}
            <div
              className={`font-semibold text-center ${
                isDark ? "text-cyan-400" : "text-cyan-700"
              }`}
            >
              Target Language Code
            </div>
          </div>
        </div>

        {/* Phase Artifacts Display */}
        {phaseData && (
          <div
            className={`mt-6 p-4 rounded-lg border ${
              isDark
                ? "bg-slate-900 border-slate-700"
                : "bg-slate-50 border-slate-200"
            }`}
          >
            <h3
              className={`font-semibold mb-2 ${
                isDark ? "text-cyan-300" : "text-cyan-700"
              }`}
            >
              Phase Artifacts: {phaseData.phase}
            </h3>
            <pre
              className={`text-xs overflow-x-auto ${
                isDark ? "text-slate-300" : "text-slate-700"
              }`}
            >
              {JSON.stringify(phaseData.artifacts, null, 2)}
            </pre>
          </div>
        )}
      </motion.section>

      {/* Features Grid */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <h2 className="mb-6 text-2xl font-semibold flex items-center gap-2">
          <svg
            className={`w-6 h-6 ${isDark ? "text-cyan-400" : "text-cyan-600"}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          Features
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {[
            {
              icon: "Search",
              title: "Compiler Phase Visualization",
              items: [
                "Lexical Analysis",
                "Syntax Analysis (AST)",
                "Semantic Analysis",
                "Intermediate Code",
                "Final Code Gen",
              ],
            },
            {
              icon: "Edit",
              title: "Interactive Editors",
              items: [
                "Monaco-powered editor",
                "Syntax highlighting",
                "Auto-formatting",
                "Read-only output",
              ],
            },
            {
              icon: "Chip",
              title: "Compiler Internals",
              items: [
                "Token stream inspection",
                "AST visualization",
                "Symbol table view",
                "Three Address Code",
              ],
            },
            {
              icon: "Play",
              title: "Code Execution",
              items: [
                "Run original source",
                "Run generated target",
                "Java support",
                "C++ compilation",
              ],
            },
          ].map((feature, idx) => (
            <div
              key={idx}
              className={`p-6 rounded-xl border ${
                isDark
                  ? "bg-slate-800/60 border-slate-700"
                  : "bg-white border-slate-200 shadow-sm"
              }`}
            >
              <div
                className={`w-12 h-12 rounded-lg bg-gradient-to-br ${
                  isDark
                    ? "from-cyan-500/20 to-violet-500/20"
                    : "from-cyan-100 to-indigo-100"
                } flex items-center justify-center mb-4`}
              >
                <svg
                  className={`w-6 h-6 ${
                    isDark ? "text-cyan-400" : "text-cyan-600"
                  }`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  {feature.icon === "Search" && (
                    <path
                      fillRule="evenodd"
                      d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                      clipRule="evenodd"
                    />
                  )}
                  {feature.icon === "Edit" && (
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  )}
                  {feature.icon === "Chip" && (
                    <path
                      fillRule="evenodd"
                      d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                      clipRule="evenodd"
                    />
                  )}
                  {feature.icon === "Play" && (
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                      clipRule="evenodd"
                    />
                  )}
                </svg>
              </div>
              <h3
                className={`font-semibold text-lg mb-3 ${
                  isDark ? "text-white" : "text-slate-800"
                }`}
              >
                {feature.title}
              </h3>
              <ul
                className={`text-sm ${
                  isDark ? "text-slate-400" : "text-slate-600"
                } space-y-1`}
              >
                {feature.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span
                      className={`w-1.5 h-1.5 rounded-full ${
                        isDark ? "bg-cyan-400" : "bg-cyan-500"
                      }`}
                    ></span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </motion.section>

      {/* Architecture Diagram */}
      <div style={sectionCard}>
        <h2
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: text,
            margin: "0 0 1.25rem",
          }}
        >
          Architecture Diagram
        </h2>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 0,
          }}
        >
          {/* React Frontend */}
          <div
            style={{
              padding: "10px 28px",
              borderRadius: 10,
              minWidth: 220,
              textAlign: "center",
              background: isDark
                ? "rgba(99,102,241,0.15)"
                : "rgba(99,102,241,0.1)",
              border: `1.5px solid ${
                isDark ? "rgba(99,102,241,0.35)" : "rgba(99,102,241,0.3)"
              }`,
            }}
          >
            <div
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: isDark ? "#a5b4fc" : "#4f46e5",
              }}
            >
              React Frontend
            </div>
            <div style={{ fontSize: 11, color: textMuted }}>Vite + Monaco</div>
          </div>
          <div
            style={{
              width: 1.5,
              height: 24,
              background: isDark ? "#334155" : "#e2e8f0",
            }}
          />

          {/* Django Backend */}
          <div
            style={{
              padding: "10px 28px",
              borderRadius: 10,
              minWidth: 220,
              textAlign: "center",
              background: isDark
                ? "rgba(6,182,212,0.12)"
                : "rgba(6,182,212,0.08)",
              border: `1.5px solid ${
                isDark ? "rgba(6,182,212,0.3)" : "rgba(6,182,212,0.25)"
              }`,
            }}
          >
            <div
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: isDark ? "#67e8f9" : "#0891b2",
              }}
            >
              Django Backend
            </div>
            <div style={{ fontSize: 11, color: textMuted }}>
              Django REST API
            </div>
          </div>
          <div
            style={{
              width: 1.5,
              height: 24,
              background: isDark ? "#334155" : "#e2e8f0",
            }}
          />

          {/* Three branches */}
          <div
            style={{
              display: "flex",
              gap: 16,
              alignItems: "flex-start",
              width: "100%",
              justifyContent: "center",
            }}
          >
            {[
              {
                label: "Java → C++",
                sub: "Compiler Pipeline",
                color: isDark ? "#fbbf24" : "#d97706",
              },
              {
                label: "Shared Output",
                sub: "JSON Artifacts",
                color: isDark ? "#34d399" : "#059669",
              },
              {
                label: "C++ → Java",
                sub: "Compiler Pipeline",
                color: isDark ? "#a5b4fc" : "#4f46e5",
              },
            ].map(({ label, sub, color }) => (
              <div
                key={label}
                style={{
                  flex: 1,
                  maxWidth: 180,
                  padding: "10px 12px",
                  borderRadius: 10,
                  textAlign: "center",
                  background: isDark
                    ? "rgba(255,255,255,0.04)"
                    : "#f8fafc",
                  border: `1px solid ${border}`,
                }}
              >
                <div style={{ fontSize: 12, fontWeight: 600, color }}>
                  {label}
                </div>
                <div style={{ fontSize: 11, color: textMuted }}>{sub}</div>
              </div>
            ))}
          </div>
          <div
            style={{
              width: 1.5,
              height: 24,
              background: isDark ? "#334155" : "#e2e8f0",
            }}
          />

          {/* Compiler Phases Engine */}
          <div
            style={{
              padding: "12px 28px",
              borderRadius: 10,
              minWidth: 260,
              textAlign: "center",
              background: isDark
                ? "rgba(16,185,129,0.1)"
                : "rgba(16,185,129,0.06)",
              border: `1.5px solid ${
                isDark ? "rgba(16,185,129,0.3)" : "rgba(16,185,129,0.25)"
              }`,
            }}
          >
            <div
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: "#10b981",
                marginBottom: 8,
              }}
            >
              Compiler Phases Engine
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              {[
                "Lexical Analysis",
                "Syntax Analysis",
                "Semantic Analysis",
                "Intermediate Code",
                "Code Generation",
              ].map((p, i) => (
                <div
                  key={p}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    fontSize: 11,
                    color: isDark ? textSub : "#334155",
                  }}
                >
                  <span
                    style={{
                      width: 18,
                      height: 18,
                      borderRadius: 4,
                      flexShrink: 0,
                      background: isDark
                        ? "rgba(16,185,129,0.15)"
                        : "rgba(16,185,129,0.1)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 10,
                      fontWeight: 700,
                      color: "#10b981",
                    }}
                  >
                    {i + 1}
                  </span>
                  {p}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Compiler Phases and Stored JSON Artifacts */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <h2
          className={`mb-6 text-2xl font-semibold ${
            isDark ? "text-white" : "text-slate-800"
          }`}
        >
          Compiler Phases & Stored JSON Artifacts
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {PHASES.map((p, i) => (
            <CompilerPhaseCard key={p.title} phase={p} i={i} />
          ))}
        </div>
      </motion.section>

      {/* Supported Constructs */}
      <div style={sectionCard}>
        <h2
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: text,
            margin: "0 0 1.25rem",
          }}
        >
          Commonly Supported Constructs
        </h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "1.5rem",
          }}
        >
          {/* General */}
          <div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: accent,
                marginBottom: 10,
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              General Language Features
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
              {[
                ["Variable declarations", "int a=1, b=2;"],
                [
                  "Assignments with Compound Operators",
                  "=  +=  -=  *=  /=  %=",
                ],
                ["Arithmetic operators", "+ − * / %"],
                ["Relational operators", "< > <= >="],
                ["Equality operators", "== !="],
                ["Logical operators", "&& || !"],
                ["Unary operators", "++ -- (prefix/postfix), unary + - !"],
                ["Ternary operator", "condition ? a : b"],
                ["Control flow", "if / else / switch (nested ones also)"],
                ["Loops", "for / while / do-while (nested loops also)"],
                ["Jump statements", "break / continue / return"],
                ["Function declarations", "and calls"],
                ["Block Statements", "{ ... }"],
              ].map(([label, code]) => (
                <div
                  key={label}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 8,
                    fontSize: 12,
                    color: isDark ? textSub : "#334155",
                  }}
                >
                  <span>▸ {label}</span>
                  <code
                    style={{
                      fontFamily: "monospace",
                      fontSize: 11,
                      color: accent,
                      background: isDark
                        ? "rgba(129,140,248,0.1)"
                        : "rgba(79,70,229,0.06)",
                      padding: "2px 6px",
                      borderRadius: 4,
                      flexShrink: 0,
                    }}
                  >
                    {code}
                  </code>
                </div>
              ))}
            </div>
          </div>

          {/* Language-specific */}
          <div>
            <div
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: accent,
                marginBottom: 10,
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              Language-Specific Handling
            </div>

            <div
              style={{
                padding: "12px 14px",
                borderRadius: 10,
                marginBottom: 12,
                background: isDark
                  ? "rgba(245,158,11,0.08)"
                  : "rgba(245,158,11,0.05)",
                border: `1px solid ${
                  isDark ? "rgba(245,158,11,0.2)" : "rgba(245,158,11,0.15)"
                }`,
              }}
            >
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: isDark ? "#fbbf24" : "#d97706",
                  marginBottom: 8,
                  display: "flex",
                  alignItems: "center",
                  gap: 5,
                }}
              >
                Java → C++
              </div>
              {[
                ["System.out.println(…)", "cout << … << endl;"],
                ["boolean", "bool"],
                ["String", "string"],
                ["byte", "char"],
              ].map(([from, to]) => (
                <div
                  key={from}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                    fontSize: 11.5,
                    color: isDark ? textSub : "#334155",
                    marginBottom: 5,
                  }}
                >
                  <code
                    style={{
                      fontFamily: "monospace",
                      color: isDark ? "#fbbf24" : "#d97706",
                      fontSize: 11,
                    }}
                  >
                    {from}
                  </code>
                  <span style={{ fontSize: 11 }}>→</span>
                  <code
                    style={{
                      fontFamily: "monospace",
                      color: isDark ? "#67e8f9" : "#0891b2",
                      fontSize: 11,
                    }}
                  >
                    {to}
                  </code>
                </div>
              ))}
            </div>

            <div
              style={{
                padding: "12px 14px",
                borderRadius: 10,
                background: isDark
                  ? "rgba(99,102,241,0.08)"
                  : "rgba(99,102,241,0.04)",
                border: `1px solid ${
                  isDark ? "rgba(99,102,241,0.2)" : "rgba(99,102,241,0.15)"
                }`,
              }}
            >
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: isDark ? "#a5b4fc" : "#4f46e5",
                  marginBottom: 8,
                  display: "flex",
                  alignItems: "center",
                  gap: 5,
                }}
              >
                C++ → Java
              </div>
              {[
                ["#include …", "(removed)"],
                ["cout << … << endl;", "System.out.println(…)"],
                ["TestAll::add(…)", "TestAll.add(…)"],
                ["bool", "boolean"],
                ["string", "String"],
                ["char*", "String"],
                ["int*", "int[]"],
              ].map(([from, to]) => (
                <div
                  key={from}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                    fontSize: 11.5,
                    color: isDark ? textSub : "#334155",
                    marginBottom: 5,
                  }}
                >
                  <code
                    style={{
                      fontFamily: "monospace",
                      color: isDark ? "#67e8f9" : "#0891b2",
                      fontSize: 11,
                    }}
                  >
                    {from}
                  </code>
                  <span style={{ fontSize: 11 }}>→</span>
                  <code
                    style={{
                      fontFamily: "monospace",
                      color: isDark ? "#fbbf24" : "#d97706",
                      fontSize: 11,
                    }}
                  >
                    {to}
                  </code>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}