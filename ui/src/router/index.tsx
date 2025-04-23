import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router";

import useAuth from "@/hooks/useAuth";
import { DashboardLayout } from "@/layouts/dashboard";

import LoginPage from "@/pages/login";
import LoadingPage from "@/pages/loading";
import PortfoliosPage from "@/pages/portfolios";
import PortfolioDetailsPage from "@/pages/portfolio-details";
import NotFound from "@/pages/404";

const Dashboard = lazy(() => import("@/pages/dashboard"));
const Assets = lazy(() => import("@/pages/assets"));
const Users = lazy(() => import("@/pages/users"));

export default function Router() {
  const status = useAuth();

  if (status === "authorized") {
    return (
      <Suspense fallback={<LoadingPage />}>
        <Routes>
          <Route path="/panel" element={<DashboardLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="assets" element={<Assets />} />
            <Route path="users" element={<Users />} />
            <Route path="portfolios" element={<PortfoliosPage />} />
            <Route path="portfolios/:id" element={<PortfolioDetailsPage />} />
            <Route path="users" element={<Users />} />
          </Route>
          <Route path="/" element={<Navigate to="/panel" />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Suspense>
    );
  }

  if (status === "idle" || status === "loading") {
    return <LoadingPage />;
  }

  return (
    <Routes>
      <Route path="*" element={<LoginPage />} />
    </Routes>
  );
}
