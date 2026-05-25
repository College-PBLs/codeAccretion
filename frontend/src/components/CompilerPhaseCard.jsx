import { motion } from "framer-motion";
import {
  CircleStackIcon,
  ArrowRightIcon,
  CheckBadgeIcon,
  CpuChipIcon,
} from "@heroicons/react/24/outline";

export default function CompilerPhaseCard({ phase, i }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        delay: i * 0.12,
        duration: 0.45,
      }}
      whileHover={{ y: -6 }}
      className="
        group relative overflow-hidden rounded-3xl border
        border-slate-200 bg-white/90
        dark:border-slate-700/60 dark:bg-gradient-to-br dark:from-slate-900/90 dark:to-slate-950/90
        backdrop-blur-xl shadow-lg
        dark:shadow-[0_10px_40px_rgba(0,0,0,0.35)]
        transition-all duration-500
        hover:border-cyan-400/40 hover:shadow-cyan-500/10
      "
    >
      {/* Animated Glow */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        <div className="absolute -top-24 -right-24 h-56 w-56 rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="absolute -bottom-24 -left-24 h-56 w-56 rounded-full bg-violet-500/10 blur-3xl" />
      </div>

      {/* Top Accent */}
      <div className="absolute inset-x-0 top-0 h-[3px] bg-gradient-to-r from-cyan-400 via-sky-500 to-violet-500" />

      <div className="relative p-7">
        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-6">
          <div className="flex items-start gap-4">
            {/* Icon */}
            <div
              className="
                flex h-14 w-14 items-center justify-center rounded-2xl
                bg-gradient-to-br from-cyan-500/10 to-violet-500/10
                border border-cyan-400/20
              "
            >
              <CpuChipIcon className="w-7 h-7 text-cyan-500 dark:text-cyan-300" />
            </div>

            {/* Title */}
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs uppercase tracking-[0.2em] text-cyan-500 dark:text-cyan-400 font-semibold">
                  Phase {i + 1}
                </span>

                <div className="h-1 w-1 rounded-full bg-slate-400 dark:bg-slate-600" />

                <span className="text-xs text-slate-500 dark:text-slate-500">
                  Compiler Pipeline
                </span>
              </div>

              <h3 className="text-2xl font-bold text-slate-900 dark:text-white leading-tight">
                {phase.title}
              </h3>

              <p className="mt-2 text-sm leading-relaxed text-slate-600 dark:text-slate-400 max-w-xl">
                {phase.desc}
              </p>
            </div>
          </div>

          {/* JSON Badge */}
          <div
            className="
              shrink-0 rounded-xl border
              border-cyan-500/20
              bg-cyan-500/10
              px-3 py-2 text-xs font-mono
              text-cyan-700 dark:text-cyan-300
            "
          >
            {phase.jsonArtifact}
          </div>
        </div>

        {/* Input / Output */}
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 mb-6">
          {/* Input */}
          <div
            className="
              rounded-2xl border p-4 transition-all
              border-slate-200 bg-slate-50
              dark:border-slate-700/70 dark:bg-slate-800/50
              group-hover:border-cyan-500/20
            "
          >
            <div className="mb-3 flex items-center gap-2">
              <CircleStackIcon className="h-4 w-4 text-cyan-500 dark:text-cyan-400" />

              <span className="text-xs font-semibold uppercase tracking-wider text-cyan-500 dark:text-cyan-400">
                Input
              </span>
            </div>

            <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
              {phase.input}
            </p>
          </div>

          {/* Output */}
          <div
            className="
              rounded-2xl border p-4 transition-all
              border-slate-200 bg-slate-50
              dark:border-slate-700/70 dark:bg-slate-800/50
              group-hover:border-violet-500/20
            "
          >
            <div className="mb-3 flex items-center gap-2">
              <ArrowRightIcon className="h-4 w-4 text-violet-500 dark:text-violet-400" />

              <span className="text-xs font-semibold uppercase tracking-wider text-violet-500 dark:text-violet-400">
                Output
              </span>
            </div>

            <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
              {phase.output}
            </p>
          </div>
        </div>

        {/* Operations */}
        <div
          className="
            rounded-2xl border p-5
            border-slate-200 bg-slate-50
            dark:border-slate-700/60 dark:bg-slate-900/40
          "
        >
          <div className="flex items-center gap-2 mb-4">
            <CheckBadgeIcon className="h-5 w-5 text-emerald-500 dark:text-emerald-400" />

            <h4 className="text-sm font-semibold uppercase tracking-wider text-slate-800 dark:text-slate-200">
              Internal Operations
            </h4>
          </div>

          <div className="grid gap-3">
            {phase.details.map((detail, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.04 }}
                className="
                  group/item flex items-start gap-3 rounded-xl border px-4 py-3 transition-all
                  border-slate-200 bg-white
                  dark:border-slate-800 dark:bg-slate-800/40
                  hover:border-cyan-500/20
                  dark:hover:bg-slate-800/70
                "
              >
                <div className="mt-[6px] h-2 w-2 rounded-full bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.9)]" />

                <span
                  className="
                    text-sm leading-relaxed transition-colors
                    text-slate-700
                    dark:text-slate-300
                    group-hover/item:text-slate-900
                    dark:group-hover/item:text-white
                  "
                >
                  {detail}
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}