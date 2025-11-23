"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import { copyToClipboard } from "@/lib/utils";

interface CopyButtonProps {
  text: string;
  variant?: "primary" | "secondary" | "danger" | "outline";
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function CopyButton({
  text,
  variant = "outline",
  size = "sm",
  className = "",
}: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const success = await copyToClipboard(text);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <Button
      variant={variant}
      size={size}
      onClick={handleCopy}
      className={className}
    >
      {copied ? "✓ 복사됨" : "복사"}
    </Button>
  );
}

