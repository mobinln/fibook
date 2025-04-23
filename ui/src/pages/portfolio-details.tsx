import { Suspense } from "react";
import { ArrowLeft } from "lucide-react";
import { Link, useParams } from "react-router";
import useSWRImmutable from "swr/immutable";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import AddHoldingDialog from "@/components/portfolios/add-holding-dialog";
import { PortfolioHoldingType, PortfolioType } from "@/api/portfolio";
import DataTable from "@/components/DataTable";

function PortfolioSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-10 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-2/3" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
      </div>
    </div>
  );
}

function HoldingsSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-10 w-1/4" />
      <Skeleton className="h-64 w-full" />
    </div>
  );
}

export default function PortfolioDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const { data: portfolio } = useSWRImmutable<PortfolioType>(id ? `/portfolios/${id}` : null);
  const { data: holdings } = useSWRImmutable<PortfolioHoldingType[]>(id ? `/portfolios/${id}/holdings` : null);

  if (!portfolio || !holdings) {
    return <></>;
  }

  return (
    <div className="container">
      <div className="mb-6">
        <Link to="/panel/portfolios">
          <Button variant="ghost" className="pl-0">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Portfolios
          </Button>
        </Link>
      </div>

      <Suspense fallback={<PortfolioSkeleton />}>
        {portfolio ? (
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold">{portfolio.name}</h1>
              <p className="text-muted-foreground mt-2">{portfolio.description || "No description provided"}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {portfolio.is_active ? (
                      <span className="text-green-500">Active</span>
                    ) : (
                      <span className="text-red-500">Inactive</span>
                    )}
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Base Currency</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{portfolio.base_currency_id}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-muted-foreground">Holdings</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{holdings.length}</div>
                </CardContent>
              </Card>
            </div>
          </div>
        ) : (
          <div className="text-center py-10">
            <h2 className="text-2xl font-bold">Portfolio not found</h2>
            <p className="text-muted-foreground mt-2">
              The portfolio you're looking for doesn't exist or you don't have access to it.
            </p>
            <Link to="/" className="mt-4 inline-block">
              <Button>Go back to portfolios</Button>
            </Link>
          </div>
        )}
      </Suspense>

      {portfolio && (
        <Suspense fallback={<HoldingsSkeleton />}>
          <div className="mt-10">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Holdings</h2>
              <AddHoldingDialog portfolioId={id}>
                <Button>Add Holding</Button>
              </AddHoldingDialog>
            </div>

            <DataTable
              url={`/portfolios/${id}/holdings`}
              columns={[
                {
                  name: "asset",
                  header: "Asset",
                  getValue(row: any) {
                    return row?.asset?.name;
                  },
                },
                { name: "quantity", header: "Quantity" },
              ]}
            />
          </div>
        </Suspense>
      )}
    </div>
  );
}
