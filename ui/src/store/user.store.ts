import { create } from "zustand";
import { UserType } from "@/api/auth";

type UserStatus = "idle" | "authorized" | "unauthorized" | "loading";

type UserState = {
  status: UserStatus;
  user: UserType | null;
  setUser: (v: UserType) => void;
  setStatus: (v: UserStatus) => void;
  logout: () => void;
};

export const useUser = create<UserState>((set) => ({
  status: "idle" as UserStatus,
  user: null,
  setUser: (newUser) => set({ user: newUser }),
  setStatus: (newStatus) => set({ status: newStatus }),
  logout: () => set({ user: null, status: "unauthorized" }),
}));
