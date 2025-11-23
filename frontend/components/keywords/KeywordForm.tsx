"use client";

import React, { useState } from "react";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

interface KeywordFormProps {
  onSubmit: (keyword: string) => Promise<void>;
  isLoading?: boolean;
}

export function KeywordForm({ onSubmit, isLoading = false }: KeywordFormProps) {
  const [keyword, setKeyword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!keyword.trim()) {
      setError("키워드를 입력해주세요.");
      return;
    }

    try {
      await onSubmit(keyword.trim());
      setKeyword("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "키워드 추가에 실패했습니다.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="새 키워드"
        placeholder="예: AI, 마케팅, 트렌드 등"
        value={keyword}
        onChange={(e) => {
          setKeyword(e.target.value);
          setError("");
        }}
        error={error}
        disabled={isLoading}
      />
      <Button type="submit" isLoading={isLoading} className="w-full">
        키워드 추가
      </Button>
    </form>
  );
}

