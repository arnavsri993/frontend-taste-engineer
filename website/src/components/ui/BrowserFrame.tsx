import { cn } from "@/lib/utils";

interface BrowserFrameProps {
  url?: string;
  children: React.ReactNode;
  className?: string;
}

export function BrowserFrame({ url = "preview.local", children, className }: BrowserFrameProps) {
  return (
    <div className={cn("browser-frame", className)}>
      <div className="browser-chrome" aria-hidden="true">
        <span className="browser-dot" />
        <span className="browser-dot" />
        <span className="browser-dot" />
        <span className="ml-2 text-xs font-mono text-gray-400 truncate flex-1">{url}</span>
      </div>
      <div className="relative">{children}</div>
    </div>
  );
}
