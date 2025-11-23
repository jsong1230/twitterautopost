"use client";

import React from "react";
import type { Keyword } from "@/lib/types";
import { Button } from "@/components/ui/Button";
import { formatDate } from "@/lib/utils";

interface KeywordListProps {
  keywords: Keyword[];
  onToggle: (id: number) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  isLoading?: boolean;
}

export function KeywordList({
  keywords,
  onToggle,
  onDelete,
  isLoading = false,
}: KeywordListProps) {
  if (keywords.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        등록된 키워드가 없습니다. 아래에서 키워드를 추가해주세요.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {keywords.map((keyword) => (
        <div
          key={keyword.id}
          className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors"
        >
          <div className="flex-1">
            <div className="flex items-center gap-3">
              <h3 className="text-lg font-semibold text-gray-900">
                {keyword.keyword}
              </h3>
              <span
                className={`px-2 py-1 text-xs font-medium rounded-full ${
                  keyword.is_active
                    ? "bg-green-100 text-green-800"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {keyword.is_active ? "활성" : "비활성"}
              </span>
            </div>
            <p className="text-sm text-gray-500 mt-1">
              등록일: {formatDate(keyword.created_at)}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant={keyword.is_active ? "secondary" : "primary"}
              size="sm"
              onClick={() => onToggle(keyword.id)}
              disabled={isLoading}
            >
              {keyword.is_active ? "비활성화" : "활성화"}
            </Button>
            <Button
              variant="danger"
              size="sm"
              onClick={() => onDelete(keyword.id)}
              disabled={isLoading}
            >
              삭제
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
}

