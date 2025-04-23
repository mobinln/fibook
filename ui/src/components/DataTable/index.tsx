import { ReactNode } from "react";
import useSWR from "swr";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ListResponse } from "@/api";
import { cn } from "@/lib/utils";

export type ColumnType = {
  name: string;
  header?: string;
  getValue?: (row: unknown) => ReactNode;
};

export default function DataTable<T>({
  url,
  columns,
  className,
}: {
  url: string;
  columns: ColumnType[];
  className?: string;
}) {
  const { data } = useSWR<ListResponse<T> | T[]>(url);
  const dataList = Array.isArray(data) ? data : data?.result;

  return (
    <div className={cn("rounded-md border", className)}>
      <Table>
        <TableHeader>
          <TableRow>
            {columns.map((c) => (
              <TableHead key={c.name}>{c.header || c.name}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {dataList && dataList?.length > 0 ? (
            dataList?.map((i, idx) => (
              <TableRow key={idx}>
                {columns.map((c) => (
                  <TableCell key={c.name}>{String(c.getValue ? c.getValue(i) : (i as any)[c.name])}</TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={5} className="text-center py-4">
                No records found
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
