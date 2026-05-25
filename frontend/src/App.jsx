import { Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import MainLayout from "./layouts/MainLayout";
import HomePage from "./pages/HomePage";
import TranspilePage from "./pages/TranspilePage";
import { useToast } from "./hooks/useToast";

export default function App() {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") return true;
    if (saved === "light") return false;
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });
  const { toast, show } = useToast();

  useEffect(() => {
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <MainLayout dark={dark} setDark={setDark} toast={toast}>
      <Routes>
        <Route path="/" element={<HomePage isDark={dark} />} />
        <Route
          path="/java-to-cpp"
          element={
            <TranspilePage
              sourceLanguage="java"
              targetLanguage="cpp"
              toast={show}
              dark={dark}
            />
          }
        />
        <Route
          path="/cpp-to-java"
          element={
            <TranspilePage
              sourceLanguage="cpp"
              targetLanguage="java"
              toast={show}
              dark={dark}
            />
          }
        />
      </Routes>
    </MainLayout>
  );
}
