import { format } from "date-fns";

export function formatDate(v: Date | string) {
  return format(v, "yyyy-MM-dd HH:mm");
}
