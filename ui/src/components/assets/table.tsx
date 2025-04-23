import { PlusCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import DataTable from "../DataTable";
import CreateAssetDialog from "./create-asset-dialog";

export default function AssetsTable() {
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Assets</h2>
        <CreateAssetDialog>
          <Button>
            <PlusCircle className="mr-2 h-4 w-4" />
            Add Asset
          </Button>
        </CreateAssetDialog>
      </div>

      <DataTable
        url="/assets"
        columns={[
          { name: "id", header: "ID" },
          { name: "name", header: "Name" },
          { name: "symbol", header: "Symbol" },
          {
            name: "asset_type",
            header: "Asset Type",
            getValue(row: any) {
              return row?.asset_type?.name;
            },
          },
          {
            name: "currency",
            header: "Currency",
            getValue(row: any) {
              return row?.currency?.name;
            },
          },
          { name: "created_at", header: "Created At" },
        ]}
      />
    </div>
  );
}
