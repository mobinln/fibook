import { useEffect } from "react";
import { getMe } from "@/api/auth";
import { getToken } from "@/api/token";
import { useUser } from "@/store/user.store";

export default function useAuth() {
  const status = useUser((s) => s.status);
  const setStatus = useUser((s) => s.setStatus);
  const setUser = useUser((s) => s.setUser);
  const logout = useUser((s) => s.logout);

  useEffect(() => {
    const token = getToken();
    if (status === "idle" && token) {
      setStatus("loading");
      getMe()
        .then((r) => {
          setStatus("authorized");
          setUser(r);
        })
        .catch(() => {
          logout();
        });
    } else if (!token) {
      setStatus("unauthorized");
      logout();
    }
  }, [logout, setStatus, setUser, status]);

  return status;
}
