"use client";

import { useCallback, useState } from "react";
import { Check, Copy } from "lucide-react";
import { copyToClipboard, cn } from "@/lib/utils";

interface CopyButtonProps {
  text: string;
  label?: string;
  className?: string;
  variant?: "default" | "inverse";
}

export function CopyButton({ text, label = "Copy", className, variant = "default" }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    const success = await copyToClipboard(text);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  }, [text]);

  return (
    <button
      type="button"
      onClick={handleCopy}
      aria-label={copied ? "Copied to clipboard" : `${label} to clipboard`}
      className={cn(
        "inline-flex items-center justify-center gap-1.5 min-h-[44px] min-w-[44px] px-3 text-sm rounded transition-colors",
        variant === "inverse"
          ? "text-white/90 hover:text-white hover:bg-white/10 border border-white/30"
          : "text-gray-600 hover:text-ink hover:bg-gray-100",
        className
      )}
    >
      {copied ? (
        <>
          <Check className="w-4 h-4 text-teal" aria-hidden="true" />
          <span>Copied</span>
        </>
      ) : (
        <>
          <Copy className="w-4 h-4" aria-hidden="true" />
          <span>{label}</span>
        </>
      )}
    </button>
  );
}
