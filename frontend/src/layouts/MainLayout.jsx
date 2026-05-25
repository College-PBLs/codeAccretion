import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Toast from "../components/Toast";

export default function MainLayout({ children, dark, setDark, toast }) {
  return (
    <div className={dark?'dark':'light'}>
      <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
        <Navbar dark={dark} setDark={setDark} />
        <main className="mx-auto max-w-7xl px-4 py-8">{children}</main>
        <Footer />
        <Toast toast={toast} />
      </div>
    </div>
  );
}