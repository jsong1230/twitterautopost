import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Twitter/Instagram AI 인사이트 생성기
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            AI 기반 트렌드 분석 및 포스트 자동 생성
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-900 mb-3">
              키워드 관리
            </h2>
            <p className="text-gray-600 mb-4">
              트렌드 분석을 위한 키워드를 등록하고 관리하세요.
            </p>
            <Link
              href="/keywords"
              className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              키워드 관리 →
            </Link>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-900 mb-3">
              대시보드
            </h2>
            <p className="text-gray-600 mb-4">
              생성된 인사이트와 포스트를 확인하세요.
            </p>
            <Link
              href="/dashboard"
              className="inline-block bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              대시보드 →
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            주요 기능
          </h2>
          <ul className="space-y-2 text-gray-600">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              키워드 기반 트윗 수집 및 분석
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              AI 기반 트렌드 요약 (한글/영어)
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              트윗 초안 자동 생성 (3-5개)
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              인스타그램 캡션 + 해시태그 자동 생성
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              주기적 자동 인사이트 생성 (매일 9시, 15시, 21시)
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}
