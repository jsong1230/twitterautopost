"use client";

import React, { useState, useEffect } from "react";
import { keywordApi } from "@/lib/api";
import type { Keyword } from "@/lib/types";
import { KeywordList } from "@/components/keywords/KeywordList";
import { KeywordForm } from "@/components/keywords/KeywordForm";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function KeywordsPage() {
  const [keywords, setKeywords] = useState<Keyword[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // 키워드 목록 조회
  const fetchKeywords = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await keywordApi.getKeywords();
      setKeywords(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "키워드를 불러오는데 실패했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 키워드 추가
  const handleAddKeyword = async (keyword: string) => {
    try {
      setIsSubmitting(true);
      setError(null);
      setSuccessMessage(null);
      await keywordApi.createKeyword(keyword);
      setSuccessMessage("키워드가 추가되었습니다.");
      await fetchKeywords(); // 목록 새로고침
    } catch (err) {
      throw err; // KeywordForm에서 처리
    } finally {
      setIsSubmitting(false);
    }
  };

  // 키워드 삭제
  const handleDeleteKeyword = async (id: number) => {
    if (!confirm("정말 이 키워드를 삭제하시겠습니까?")) {
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      setSuccessMessage(null);
      await keywordApi.deleteKeyword(id);
      setSuccessMessage("키워드가 삭제되었습니다.");
      await fetchKeywords(); // 목록 새로고침
    } catch (err) {
      setError(err instanceof Error ? err.message : "키워드 삭제에 실패했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // 키워드 활성/비활성 토글
  const handleToggleKeyword = async (id: number) => {
    try {
      setIsSubmitting(true);
      setError(null);
      setSuccessMessage(null);
      await keywordApi.toggleKeyword(id);
      setSuccessMessage("키워드 상태가 변경되었습니다.");
      await fetchKeywords(); // 목록 새로고침
    } catch (err) {
      setError(err instanceof Error ? err.message : "키워드 상태 변경에 실패했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // 초기 로드
  useEffect(() => {
    fetchKeywords();
  }, []);

  // 성공 메시지 자동 제거
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">키워드 관리</h1>
          <p className="text-gray-600">
            트렌드 분석을 위한 키워드를 등록하고 관리하세요.
          </p>
        </div>

        {/* 알림 메시지 */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-800">
            {error}
          </div>
        )}
        {successMessage && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-800">
            {successMessage}
          </div>
        )}

        {/* 키워드 추가 폼 */}
        <Card title="새 키워드 추가" className="mb-6">
          <KeywordForm onSubmit={handleAddKeyword} isLoading={isSubmitting} />
        </Card>

        {/* 키워드 목록 */}
        <Card title="등록된 키워드">
          {isLoading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-500">로딩 중...</p>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-gray-600">
                  총 {keywords.length}개의 키워드
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={fetchKeywords}
                  disabled={isSubmitting}
                >
                  새로고침
                </Button>
              </div>
              <KeywordList
                keywords={keywords}
                onToggle={handleToggleKeyword}
                onDelete={handleDeleteKeyword}
                isLoading={isSubmitting}
              />
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}

