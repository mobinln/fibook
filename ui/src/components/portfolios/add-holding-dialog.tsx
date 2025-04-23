import type React from "react";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { toast } from "sonner";
import useSWRImmutable from "swr/immutable";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { ListResponse } from "@/api";
import { AssetType } from "@/api/assets";
import { cn } from "@/lib/utils";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Command, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem } from "../ui/command";
import { ChevronsUpDown, Check } from "lucide-react";
import { createHolding } from "@/api/portfolio";
import { mutate } from "swr";

const formSchema = z.object({
  quantity: z.coerce.number().positive("Quantity must be a positive number"),
  asset_id: z.coerce.number().int().positive("Asset ID must be a positive number"),
});

export default function AddHoldingDialog({
  children,
  portfolioId,
}: {
  children: React.ReactNode;
  portfolioId: string;
}) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { data: assets, isLoading: isAssetsLoading } = useSWRImmutable<ListResponse<AssetType>>("/assets");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      quantity: 0,
      asset_id: 0,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      await createHolding(portfolioId, values as any);

      toast("Holding added.");

      setOpen(false);
      form.reset();
      mutate(`/portfolios/${portfolioId}/holdings`);
    } catch (error) {
      console.error("Error adding holding:", error);
      toast("Failed to add holding. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Holding</DialogTitle>
          <DialogDescription>Add a new asset to your portfolio.</DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="asset_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Asset ID</FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className={cn("w-full justify-between", !field.value && "text-muted-foreground")}
                          disabled={isAssetsLoading}
                        >
                          {isAssetsLoading
                            ? "Loading assets..."
                            : field.value
                            ? assets?.result?.find((currency) => currency.id === field.value)?.name ||
                              `Asset ID: ${field.value}`
                            : "Select Asset"}
                          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-full p-0">
                      <Command>
                        <CommandInput placeholder="Search asset..." />
                        <CommandList>
                          <CommandEmpty>No asset found.</CommandEmpty>
                          <CommandGroup className="max-h-60 overflow-y-auto">
                            {assets?.result?.map((currency) => (
                              <CommandItem
                                key={currency.id}
                                value={currency.name}
                                onSelect={() => {
                                  form.setValue("asset_id", currency.id, {
                                    shouldValidate: true,
                                  });
                                }}
                              >
                                <Check
                                  className={cn(
                                    "mr-2 h-4 w-4",
                                    currency.id === field.value ? "opacity-100" : "opacity-0"
                                  )}
                                />
                                {currency.symbol && <span className="font-medium mr-2">{currency.symbol}</span>}
                                {currency.name}
                                {currency.symbol && (
                                  <span className="ml-2 text-muted-foreground">{currency.symbol}</span>
                                )}
                              </CommandItem>
                            ))}
                          </CommandGroup>
                        </CommandList>
                      </Command>
                    </PopoverContent>
                  </Popover>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="quantity"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Quantity</FormLabel>
                  <FormControl>
                    <Input type="number" step="any" min="0.000001" placeholder="0.00" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Adding..." : "Add Holding"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
