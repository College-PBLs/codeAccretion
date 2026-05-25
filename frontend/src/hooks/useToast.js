import { useState } from "react";

export const useToast = () => {
  const [toast, setToast] = useState(null);

  const show = (type, message) => {
    setToast({ type, message });
    setTimeout(() => setToast(null), 2600);
  };

  return { toast, show };
};
