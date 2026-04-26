import { Button } from "@/components/ui/button";
import { Link } from "@tanstack/react-router";
import {
  ChartNoAxesCombined,
  Home,
  PlusIcon,
  ScrollText,
  Wallet,
} from "lucide-react";

function MobileNav() {
  // If the height is changed the bottom padding on the main content in __root.tsx muszt be updated to match
  return (
    <div className="h-20 rounded-t-4xl bg-[#fff8f6] px-2 grid grid-cols-5 place-items-center shadow-[0_-5px_15px_-3px_rgba(0,0,0,0.1)]">
      <Link to="/" className="w-full flex justify-center">
        <div className="flex flex-col justify-center items-center gap-0.5">
          <Home className="text-gray-400" />
          <span className="text-gray-400 text-xs">Home</span>
        </div>
      </Link>
      <Link to="/budgets" className="w-full flex justify-center">
        <div className="flex flex-col justify-center items-center gap-0.5">
          <Wallet className="text-gray-400 font-bold" />
          <span className="text-gray-400 text-xs">Budgets</span>
        </div>
      </Link>
      <Button className="rounded-full w-14 h-14 bg-[#ff6f61] text-white shadow-md flex items-center justify-center">
        <PlusIcon />
      </Button>
      <Link to="/activity" className="w-full flex justify-center">
        <div className="flex flex-col justify-center items-center gap-0.5">
          <ScrollText className="text-gray-400 font-bold" />
          <span className="text-gray-400 text-xs">Activity</span>
        </div>
      </Link>
      <Link to="/analytics" className="w-full flex justify-center">
        <div className="flex flex-col justify-center items-center gap-0.5">
          <ChartNoAxesCombined className="text-gray-400 font-bold" />
          <span className="text-gray-400 text-xs">Analytics</span>
        </div>
      </Link>
    </div>
  );
}

export default MobileNav;
