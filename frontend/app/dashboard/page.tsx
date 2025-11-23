"use client";

import React, { useState, useEffect } from "react";
import { insightApi, postApi } from "@/lib/api";
import type { Insight, Post } from "@/lib/types";
import { InsightList } from "@/components/dashboard/InsightList";
import { PostList } from "@/components/dashboard/PostList";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function DashboardPage() {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"insights" | "posts">("insights");

  // 인사이트 목록 조회
  const fetchInsights = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await insightApi.getInsights(0, 50);
      setInsights(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "인사이트를 불러오는데 실패했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 포스트 목록 조회
  const fetchPosts = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await postApi.getPosts(0, 100);
      setPosts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "포스트를 불러오는데 실패했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 인사이트 생성
  const handleGenerateInsight = async (keywordId: number) => {
    try {
      setIsGenerating(true);
      setError(null);
      setSuccessMessage(null);
      await insightApi.generateInsight(keywordId);
      setSuccessMessage("인사이트 생성이 시작되었습니다. 잠시 후 새로고침해주세요.");
      // 3초 후 자동 새로고침
      setTimeout(() => {
        fetchInsights();
        fetchPosts();
      }, 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "인사이트 생성에 실패했습니다.");
    } finally {
      setIsGenerating(false);
    }
  };

  // 복사 성공 메시지
  const handleCopySuccess = (message: string) => {
    setSuccessMessage(message);
    setTimeout(() => setSuccessMessage(null), 2000);
  };

  // 초기 로드
  useEffect(() => {
    fetchInsights();
    fetchPosts();
  }, []);

  // 성공 메시지 자동 제거
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">대시보드</h1>
          <p className="text-gray-600">
            생성된 인사이트와 포스트를 확인하고 관리하세요.
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

        {/* 탭 네비게이션 */}
        <div className="mb-6">
          <div className="flex gap-2 border-b border-gray-200">
            <button
              onClick={() => setActiveTab("insights")}
              className={`px-4 py-2 font-medium transition-colors ${
                activeTab === "insights"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              인사이트 ({insights.length})
            </button>
            <button
              onClick={() => setActiveTab("posts")}
              className={`px-4 py-2 font-medium transition-colors ${
                activeTab === "posts"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              포스트 ({posts.length})
            </button>
          </div>
        </div>

        {/* 인사이트 탭 */}
        {activeTab === "insights" && (
          <Card title="인사이트 목록">
            {isLoading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-gray-500">로딩 중...</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-sm text-gray-600">
                    총 {insights.length}개의 인사이트
                  </p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={fetchInsights}
                    disabled={isGenerating}
                  >
                    새로고침
                  </Button>
                </div>
                <InsightList
                  insights={insights}
                  onGenerateInsight={handleGenerateInsight}
                  isLoading={isGenerating}
                />
              </div>
            )}
          </Card>
        )}

        {/* 포스트 탭 */}
        {activeTab === "posts" && (
          <Card title="포스트 목록">
            {isLoading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-gray-500">로딩 중...</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <p className="text-sm text-gray-600">
                    총 {posts.length}개의 포스트
                  </p>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={fetchPosts}
                    >
                      새로고침
                    </Button>
                  </div>
                </div>
                <PostList posts={posts} onCopy={handleCopySuccess} />
              </div>
            )}
          </Card>
        )}
      </div>
    </div>
  );
}

