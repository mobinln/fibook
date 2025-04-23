import { useState, useRef, useEffect, useCallback } from "react";
import { Check, ChevronsUpDown, Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { get } from "@/api";

interface AsyncComboboxProps<T> {
  url: string;
  getOptionLabel: (option: T) => string;
  getOptionValue: (option: T) => string;
  placeholder?: string;
  searchPlaceholder?: string;
  emptyMessage?: string;
  value?: string;
  onChange?: (value: string) => void;
  className?: string;
  disabled?: boolean;
  searchParam?: string;
}

export function AsyncCombobox<T>({
  url,
  getOptionLabel,
  getOptionValue,
  placeholder = "Select an option...",
  searchPlaceholder = "Search...",
  emptyMessage = "No results found.",
  value,
  onChange,
  className,
  disabled = false,
  searchParam = "search",
}: AsyncComboboxProps<T>) {
  const [open, setOpen] = useState(false);
  const [options, setOptions] = useState<T[]>([]);
  const [selectedValue, setSelectedValue] = useState<string>(value || "");
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [selectedLabel, setSelectedLabel] = useState<string>("");

  // Debounce search query
  const debouncedSearchQuery = useRef<NodeJS.Timeout | null>(null);

  // Update internal state when external value changes
  useEffect(() => {
    if (value !== undefined) {
      setSelectedValue(value);

      // Find and set the label for the selected value
      const selectedOption = options.find((option) => getOptionValue(option) === value);
      if (selectedOption) {
        setSelectedLabel(getOptionLabel(selectedOption));
      }
    }
  }, [value, options, getOptionValue, getOptionLabel]);

  const fetchOptions = useCallback(
    async (query: string) => {
      setIsLoading(true);
      try {
        const response = await get(url, { params: { [searchParam]: query } });

        const data = JSON.parse(JSON.stringify(response));
        setOptions(Array.isArray(data) ? data : data.items || data.results || data.result || []);

        // If we have a selected value, find its label
        if (selectedValue && data.length > 0) {
          const selectedOption = data.find((option: T) => getOptionValue(option) === selectedValue);
          if (selectedOption) {
            setSelectedLabel(getOptionLabel(selectedOption));
          }
        }
      } catch (error) {
        console.error("Failed to fetch options:", error);
        setOptions([]);
      } finally {
        setIsLoading(false);
      }
    },
    [url, searchParam, selectedValue, getOptionValue, getOptionLabel]
  );

  // Fetch options when the component mounts
  useEffect(() => {
    console.count("fetchOptions");

    fetchOptions("");
  }, [fetchOptions]);

  // Handle search input change with debounce
  const handleSearchChange = useCallback(
    (input: string) => {
      setSearchQuery(input);

      if (debouncedSearchQuery.current) {
        clearTimeout(debouncedSearchQuery.current);
      }

      debouncedSearchQuery.current = setTimeout(() => {
        fetchOptions(input);
      }, 300);
    },
    [fetchOptions]
  );

  // Handle option selection
  const handleSelect = useCallback(
    (currentValue: string) => {
      const newValue = currentValue === selectedValue ? "" : currentValue;
      setSelectedValue(newValue);

      // Find the selected option to get its label
      const selectedOption = options.find((option) => getOptionValue(option) === currentValue);

      if (selectedOption) {
        setSelectedLabel(getOptionLabel(selectedOption));
      } else {
        setSelectedLabel("");
      }

      if (onChange) {
        onChange(newValue);
      }

      setOpen(false);
    },
    [selectedValue, options, getOptionValue, getOptionLabel, onChange]
  );

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn("w-full justify-between", className)}
          disabled={disabled}
        >
          {selectedLabel || placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0" align="start">
        <Command shouldFilter={false}>
          <CommandInput placeholder={searchPlaceholder} value={searchQuery} onValueChange={handleSearchChange} />
          <CommandList className="h-32">
            {isLoading ? (
              <div className="flex items-center justify-center py-6">
                <Loader2 className="h-6 w-6 animate-spin text-primary" />
              </div>
            ) : (
              <>
                <CommandEmpty>{emptyMessage}</CommandEmpty>
                <CommandGroup>
                  {options.map((option, index) => {
                    const value = getOptionValue(option);
                    const label = getOptionLabel(option);
                    return (
                      <CommandItem key={`${value}-${index}`} value={value} onSelect={handleSelect}>
                        <Check className={cn("mr-2 h-4 w-4", selectedValue === value ? "opacity-100" : "opacity-0")} />
                        {label}
                      </CommandItem>
                    );
                  })}
                </CommandGroup>
              </>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
