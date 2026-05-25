import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
});

const safe = async (cb) => {
  try {
    return await cb();
  } catch (e) {
    throw new Error(
      e?.response?.data?.message || e.message || "Request failed",
    );
  }
};

export const transpileCode = (payload) => safe(async () => (await api.post("/transpile/", payload)).data);
export const runCode = (payload) => safe(async () => (await api.post("/run/", payload)).data);
