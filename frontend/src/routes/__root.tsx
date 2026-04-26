import MobileNav from "@/components/MobileNav";
import Sidebar from "@/components/Sidebar";
import { TooltipProvider } from "@/components/ui/tooltip";
import { createRootRoute, Outlet } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: () => (
    <div className="flex h-dvh w-full overflow-hidden">
      <div className="md:block hidden z-10">
        <Sidebar />
      </div>
      <main className="flex-1 min-w-0 flex flex-col">
        {/* Bottom padding necessary to account for mobile nav bar with h-20*/}
        <div className="flex-1 min-h-0 flex flex-col bg-[#fef7f5] pb-20 md:pb-0">
          <TooltipProvider>
            <Outlet />
          </TooltipProvider>
          <div className="fixed bottom-0 left-0 right-0 z-20 md:hidden">
            <MobileNav />
          </div>
        </div>
      </main>
    </div>
  ),
});
