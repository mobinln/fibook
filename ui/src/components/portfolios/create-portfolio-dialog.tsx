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

import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { useNavigate } from "react-router";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { Check, ChevronsUpDown } from "lucide-react";
import useSWRImmutable from "swr/immutable";
import { ListResponse } from "@/api";
import { CurrencyType } from "@/api/currency";
import { createPortfolio } from "@/api/portfolio";

const formSchema = z.object({
  name: z.string().min(1, "Portfolio name is required"),
  description: z.string().optional(),
  is_active: z.boolean().default(true),
  base_currency_id: z.coerce.number().int().positive("Currency ID must be a positive number"),
});

export default function CreatePortfolioDialog({ children }) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { data: currencies, isLoading: isLoadingCurrencies } =
    useSWRImmutable<ListResponse<CurrencyType>>("/currencies");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
      is_active: true,
      base_currency_id: 1,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      if (!values.name || !values.description || !values.base_currency_id) {
        return;
      }
      const response = await createPortfolio(values as any);

      toast("Portfolio created.");

      setOpen(false);
      form.reset();

      navigate(`/panel/portfolios/${response.id}`);
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
          <DialogTitle>Create New Portfolio</DialogTitle>
          <DialogDescription>Create a new investment portfolio to track your assets.</DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Portfolio Name</FormLabel>
                  <FormControl>
                    <Input placeholder="My Investment Portfolio" {...field} />
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
              name="base_currency_id"
              render={({ field }) => (
                <FormItem className="flex flex-col">
                  <FormLabel>Base Currency</FormLabel>
                  <Popover>
                    <PopoverTrigger asChild>
                      <FormControl>
                        <Button
                          variant="outline"
                          role="combobox"
                          className={cn("w-full justify-between", !field.value && "text-muted-foreground")}
                          disabled={isLoadingCurrencies}
                        >
                          {isLoadingCurrencies
                            ? "Loading currencies..."
                            : field.value
                            ? currencies?.result?.find((currency) => currency.id === field.value)?.name ||
                              `Currency ID: ${field.value}`
                            : "Select currency"}
                          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </FormControl>
                    </PopoverTrigger>
                    <PopoverContent className="w-full p-0">
                      <Command>
                        <CommandInput placeholder="Search currency..." />
                        <CommandList>
                          <CommandEmpty>No currency found.</CommandEmpty>
                          <CommandGroup className="max-h-60 overflow-y-auto">
                            {currencies?.result?.map((currency) => (
                              <CommandItem
                                key={currency.id}
                                value={currency.name}
                                onSelect={() => {
                                  form.setValue("base_currency_id", currency.id, {
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
                                {currency.code && <span className="font-medium mr-2">{currency.code}</span>}
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
                {isLoading ? "Creating..." : "Create Portfolio"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
