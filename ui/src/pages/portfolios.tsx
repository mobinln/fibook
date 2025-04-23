import { Suspense } from "react";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import CreatePortfolioDialog from "@/components/portfolios/create-portfolio-dialog";
import { Link } from "react-router";
import useSWR from "swr";
import { ListResponse } from "@/api";
import { PortfolioType } from "@/api/portfolio";

function PortfolioSkeleton() {
  return (
    <Card className="h-[200px]">
      <CardHeader>
        <Skeleton className="h-8 w-3/4" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-4 w-full mb-2" />
        <Skeleton className="h-4 w-2/3" />
      </CardContent>
      <CardFooter>
        <Skeleton className="h-10 w-full" />
      </CardFooter>
    </Card>
  );
}

function PortfolioList({ portfolios }: { portfolios: PortfolioType[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {portfolios.map((portfolio) => (
        <Card key={portfolio.id} className="h-[220px] flex flex-col">
          <CardHeader>
            <CardTitle>{portfolio.name}</CardTitle>
          </CardHeader>
          <CardContent className="flex-grow">
            <p className="text-sm text-muted-foreground line-clamp-3">
              {portfolio.description || "No description provided"}
            </p>
            <p className="text-sm mt-2">
              <span className="font-medium">Currency:</span> {portfolio.base_currency_id}
            </p>
          </CardContent>
          <CardFooter>
            <Link to={`/panel/portfolios/${portfolio.id}`} className="w-full">
              <Button variant="default" className="w-full">
                View Details
              </Button>
            </Link>
          </CardFooter>
        </Card>
      ))}

      <CreatePortfolioDialog>
        <Card className="h-[220px] border-dashed flex flex-col justify-center items-center cursor-pointer hover:bg-accent/50 transition-colors">
          <div className="text-center p-6">
            <div className="mx-auto bg-muted rounded-full w-12 h-12 flex items-center justify-center mb-4">
              <Plus className="h-6 w-6" />
            </div>
            <h3 className="font-medium text-lg mb-1">Create New Portfolio</h3>
            <p className="text-sm text-muted-foreground">Add a new investment portfolio</p>
          </div>
        </Card>
      </CreatePortfolioDialog>
    </div>
  );
}

export default function PortfoliosPage() {
  const { data } = useSWR<ListResponse<PortfolioType>>("/portfolios");

  return (
    <Suspense
      fallback={
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <PortfolioSkeleton key={i} />
          ))}
        </div>
      }
    >
      <PortfolioList portfolios={data?.result || []} />
    </Suspense>
  );
}
