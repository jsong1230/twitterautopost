"use client";

import React from "react";
import type { Insight } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { formatDate, getRelativeTime } from "@/lib/utils";

interface InsightListProps {
  insights: Insight[];
  onGenerateInsight?: (keywordId: number) => Promise<void>;
  isLoading?: boolean;
}

export function InsightList({
  insights,
  onGenerateInsight,
  isLoading = false,
}: InsightListProps) {
  if (insights.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        생성된 인사이트가 없습니다. 키워드를 등록하고 인사이트를 생성해보세요.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {insights.map((insight) => (
        <Card key={insight.id} className="hover:shadow-lg transition-shadow">
          <div className="space-y-4">
            {/* 헤더 */}
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {insight.keyword}
                  </h3>
                  <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                    {insight.tweets_analyzed}개 트윗 분석
                  </span>
                </div>
                <p className="text-sm text-gray-500">
                  {getRelativeTime(insight.created_at)}
                </p>
              </div>
              {onGenerateInsight && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onGenerateInsight(insight.keyword_id)}
                  disabled={isLoading}
                >
                  재생성
                </Button>
              )}
            </div>

            {/* 한글 요약 */}
            {insight.summary_kr && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  한글 요약
                </h4>
                <p className="text-gray-600 whitespace-pre-wrap">
                  {insight.summary_kr}
                </p>
              </div>
            )}

            {/* 영문 요약 */}
            {insight.summary_en && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  영문 요약
                </h4>
                <p className="text-gray-600 whitespace-pre-wrap">
                  {insight.summary_en}
                </p>
              </div>
            )}

            {/* 포스트 개수 */}
            {insight.posts && insight.posts.length > 0 && (
              <div className="pt-2 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  생성된 포스트: {insight.posts.length}개
                </p>
              </div>
            )}
          </div>
        </Card>
      ))}
    </div>
  );
}

