import { FileQuestion } from "lucide-react";
import { useNavigate } from "react-router";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card className="mx-auto max-w-md shadow-lg">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <FileQuestion className="h-16 w-16 text-muted-foreground" />
          </div>
          <CardTitle className="text-3xl font-bold">404</CardTitle>
          <CardDescription className="text-xl">Page Not Found</CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-muted-foreground">The page you are looking for doesn't exist or has been moved.</p>
        </CardContent>
        <CardFooter className="flex justify-center">
          <Button onClick={() => navigate("/panel")} size="lg">
            Go back home
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
