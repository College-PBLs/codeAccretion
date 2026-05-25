import { Link, NavLink } from "react-router-dom";

export default function Navbar({ dark, setDark }) {
  const n = ({ isActive }) =>
    `px-3 py-2 rounded-lg ${
      isActive
        ? "bg-cyan-500/20 text-cyan-700 dark:text-cyan-300"
        : "text-slate-700 dark:text-slate-300"
    }`;

  return (
    <nav className="sticky top-0 z-40 border-b border-slate-200 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <Link className="font-bold gradient-text text-xl" to="/">
          CodeAccretion
        </Link>
        <div className="flex items-center gap-2">
          <NavLink className={n} to="/">
            Home
          </NavLink>
          <NavLink className={n} to="/java-to-cpp">
            Java to C++
          </NavLink>
          <NavLink className={n} to="/cpp-to-java">
            C++ to Java
          </NavLink>
          <button
            className="ml-2 rounded-lg border border-slate-300 px-3 py-2 dark:border-slate-700"
            onClick={() => setDark(!dark)}
            aria-label={dark ? "Switch to light theme" : "Switch to dark theme"}
          >
            {!dark ? '🌙':'☀️'}
          </button>
        </div>
      </div>
    </nav>
  );
}
