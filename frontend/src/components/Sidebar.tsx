import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Link } from "@tanstack/react-router";
import {
  ChartNoAxesCombined,
  HomeIcon,
  PlusIcon,
  ScrollText,
  Wallet,
} from "lucide-react";
import { useEffect, useState } from "react";

let versionPromise: Promise<string> | null = null;

export function getVersion(): Promise<string> {
  if (!versionPromise) {
    versionPromise = fetch("/api/version")
      .then((res) => res.json())
      .then((data) => data.version);
  }

  return versionPromise;
}

function Sidebar() {
  const [version, setVersion] = useState<string | null>(null);

  useEffect(() => {
    getVersion().then(setVersion);
  }, []);

  return (
    <div className="h-full w-20 bg-[#fff8f6] text-black flex flex-col items-center justify-start gap-3 py-4 shadow-[4px_0_20px_-6px_rgba(0,0,0,0.16)]">
      <div className="flex justify-center items-center">
        <span className="font-bold text-lg">Geld</span>
      </div>
      {/* Sidebar Content */}
      <div className="flex flex-col justify-start items-center h-full w-full gap-8 py-5 px-2">
        <SidebarItem
          icon={<HomeIcon className="w-8 h-8" />}
          label="Home"
          to="/"
        />
        <SidebarItem
          icon={<Wallet className="w-8 h-8" />}
          label="Budgets"
          to="/budgets"
        />
        <SidebarItem
          icon={<ScrollText className="w-8 h-8" />}
          label="Activity"
          to="/activity"
        />
        <SidebarItem
          icon={<ChartNoAxesCombined className="w-8 h-8" />}
          label="Analytics"
          to="/analytics"
        />
        <Button className="rounded-full w-12 h-12 bg-[#ff6f61] text-white shadow-md flex items-center justify-center">
          <PlusIcon />
        </Button>
      </div>
      {/* Sidebar Footer for future elements */}
      <div className="flex flex-col h-1/5 items-center justify-end font-mono text-sm text-gray-500">
        <span className="text-xs">
          {/* checks if version is a semantic version to prefix accordingly otherwise just shows the versio from the backend*/}
          {version && /^\d+\.\d+\.\d+/.test(version) ? `v${version}` : version}
        </span>
      </div>
    </div>
  );
}

export default Sidebar;

interface SidebarItemProps {
  icon: React.ReactNode;
  label: string;
  to: string;
}

function SidebarItem({ icon, label, to }: SidebarItemProps) {
  return (
    <Tooltip>
      <TooltipTrigger
        delay={20}
        render={
          <Link
            className="flex flex-col items-center justify-center gap-1"
            to={to}
          >
            <div className="text-gray-400 w-8 h-8 flex items-center justify-center">
              {icon}
            </div>
          </Link>
        }
      />
      <TooltipContent
        side="right"
        className="bg-neutral-200 fill-neutral-200 text-gray-600"
      >
        <span className="text-lg">{label}</span>
      </TooltipContent>
    </Tooltip>
  );
}
