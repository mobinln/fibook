"use client";

import { FormDescription } from "@/components/ui/form";

import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

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
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";

import { toast } from "sonner";
import { AsyncCombobox } from "../async-combobox";
import { AssetTypeType } from "@/api/asset_type";
import { createAsset } from "@/api/assets";
import { mutate } from "swr";
import { CurrencyType } from "@/api/currency";

const formSchema = z.object({
  name: z.string().min(1, "Name is required"),
  symbol: z.string().min(1, "Symbol is required"),
  description: z.string().optional(),
  is_active: z.boolean().default(true),
  currency_id: z.coerce.number().int().positive("Currency ID must be a positive number"),
  asset_type_id: z.coerce.number().int().positive("Asset Type ID must be a positive number"),
});

export default function CreateAssetDialog({ children }) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      symbol: "",
      description: "",
      is_active: true,
      asset_type_id: null,
      currency_id: null,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      await createAsset(values);

      toast("Asset created.");
      setOpen(false);
      form.reset();
      mutate("/assets");
    } catch (error) {
      console.error("Error creating portfolio:", error);
      toast("Failed to create portfolio. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Asset</DialogTitle>
          <DialogDescription>Create a new assets.</DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="Name" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="symbol"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Symbol</FormLabel>
                  <FormControl>
                    <Input placeholder="Symbol" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description (Optional)</FormLabel>
                  <FormControl>
                    <Textarea placeholder="A brief description of this portfolio" className="resize-none" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="asset_type_id"
              render={({ field }) => (
                <AsyncCombobox<AssetTypeType>
                  placeholder="Asset Type"
                  url="/asset-types"
                  getOptionLabel={(i) => i.name}
                  getOptionValue={(i) => String(i.id)}
                  searchParam="name"
                  value={String(field.value)}
                  onChange={(v) => {
                    form.setValue("asset_type_id", Number(v), {
                      shouldValidate: true,
                    });
                  }}
                />
              )}
            />
            <FormField
              control={form.control}
              name="currency_id"
              render={({ field }) => (
                <AsyncCombobox<CurrencyType>
                  placeholder="Currency"
                  url="/currencies"
                  getOptionLabel={(i) => i.name}
                  getOptionValue={(i) => String(i.id)}
                  searchParam="name"
                  value={String(field.value)}
                  onChange={(v) => {
                    form.setValue("currency_id", Number(v), {
                      shouldValidate: true,
                    });
                  }}
                />
              )}
            />
            <FormField
              control={form.control}
              name="is_active"
              render={({ field }) => (
                <FormItem className="flex flex-row items-center justify-between rounded-lg border p-3">
                  <div className="space-y-0.5">
                    <FormLabel>Active Portfolio</FormLabel>
                    <FormDescription>Set whether this portfolio is active</FormDescription>
                  </div>
                  <FormControl>
                    <Switch checked={field.value} onCheckedChange={field.onChange} />
                  </FormControl>
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Creating..." : "Create"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
