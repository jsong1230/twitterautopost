"use client";

import React from "react";
import type { Post } from "@/lib/types";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { formatDate, getRelativeTime, parseHashtags, copyToClipboard } from "@/lib/utils";

interface PostListProps {
  posts: Post[];
  onCopy?: (content: string) => void;
}

export function PostList({ posts, onCopy }: PostListProps) {
  if (posts.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        생성된 포스트가 없습니다.
      </div>
    );
  }

  const handleCopy = async (content: string, hashtags?: string | null) => {
    let textToCopy = content;
    if (hashtags) {
      const hashtagList = parseHashtags(hashtags);
      if (hashtagList.length > 0) {
        textToCopy += "\n\n" + hashtagList.map((tag) => `#${tag}`).join(" ");
      }
    }

    const success = await copyToClipboard(textToCopy);
    if (onCopy) {
      onCopy(success ? "복사되었습니다!" : "복사에 실패했습니다.");
    }
  };

  return (
    <div className="space-y-4">
      {posts.map((post) => {
        const hashtags = parseHashtags(post.hashtags);
        const isTweet = post.post_type === "tweet";
        const isInstagram = post.post_type === "instagram";

        return (
          <Card key={post.id} className="hover:shadow-lg transition-shadow">
            <div className="space-y-3">
              {/* 헤더 */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${
                      isTweet
                        ? "bg-blue-100 text-blue-800"
                        : "bg-pink-100 text-pink-800"
                    }`}
                  >
                    {isTweet ? "트윗" : isInstagram ? "인스타그램" : post.post_type}
                  </span>
                  <span className="text-sm text-gray-500">
                    {getRelativeTime(post.created_at)}
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCopy(post.content, post.hashtags)}
                >
                  복사
                </Button>
              </div>

              {/* 내용 */}
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-800 whitespace-pre-wrap">
                  {post.content}
                </p>
              </div>

              {/* 해시태그 */}
              {hashtags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {hashtags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </Card>
        );
      })}
    </div>
  );
}

