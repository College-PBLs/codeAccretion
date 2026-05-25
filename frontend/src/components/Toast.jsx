export default function Toast({ toast }) {
  if (!toast) return null;
  
  return (
    <div
      className={`fixed right-4 top-20 z-50 rounded-xl px-4 py-2 text-sm ${toast.type === "error" ? "bg-rose-500" : "bg-emerald-500"}`}
    >
      {toast.message}
    </div>
  );
}
