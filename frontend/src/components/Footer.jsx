export default function Footer() {
  return (
    <footer className="border-t border-slate-200 py-6 text-center text-slate-600 dark:border-slate-800 dark:text-slate-400">
      © {new Date().getFullYear()} CodeAccretion. All rights reserved.
    </footer>
  );
}
