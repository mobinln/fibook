import {
  BarChart3,
  Users,
  Settings,
  LayoutDashboard,
  GalleryVerticalEnd,
  BadgeDollarSign,
  Captions,
  DollarSign,
  ChartBarStacked,
  GalleryVertical,
} from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";
import { useUser } from "@/store/user.store";
import { useLocation } from "react-router";

const navigationItems = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    href: "/panel",
  },
  {
    title: "Analytics",
    icon: BarChart3,
    href: "/panel/analytics",
  },
  {
    title: "Portfolios",
    icon: GalleryVertical,
    href: "/panel/portfolios",
  },
  {
    title: "Users",
    icon: Users,
    href: "/panel/users",
    admin: true,
  },
  {
    title: "Currencies",
    icon: DollarSign,
    href: "/panel/currencies",
    admin: true,
  },
  {
    title: "Asset Types",
    icon: ChartBarStacked,
    href: "/panel/asset-types",
    admin: true,
  },
  {
    title: "Assets",
    icon: BadgeDollarSign,
    href: "/panel/assets",
  },
  {
    title: "Asset Transactions",
    icon: Captions,
    href: "/panel/asset-transactions",
  },
  {
    title: "Settings",
    icon: Settings,
    href: "/panel/settings",
  },
];

export function DashboardSidebar() {
  const location = useLocation();
  const user = useUser((s) => s.user);

  return (
    <Sidebar>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg">
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                <GalleryVerticalEnd className="size-4" />
              </div>
              <div className="flex flex-col gap-0.5 leading-none">
                <span className="font-semibold">{user?.email}</span>
                <span className="text-xs text-muted-foreground">{user?.full_name}</span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Main Menu</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems
                .filter((i) => (user?.is_superuser ? i : !i.admin))
                .map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild isActive={location.pathname === item.href}>
                      <a href={item.href}>
                        <item.icon className="h-4 w-4" />
                        <span>{item.title}</span>
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}
