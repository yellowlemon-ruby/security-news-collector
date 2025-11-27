"""
Vercel Serverless API for Security News Collector
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# 加入父目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from news_collector import SecurityNewsCollector, load_demo_data, NewsItem
from dataclasses import asdict
import pandas as pd


# 全域狀態（注意：Serverless 每次請求可能是新實例）
collector_cache = {
    'data': None,
    'last_update': None
}


def collect_news():
    """收集新聞"""
    collector = SecurityNewsCollector()
    df = collector.collect()
    
    # 如果無法連線，使用展示資料
    if df.empty:
        demo_data = load_demo_data()
        for item in demo_data:
            news_item = NewsItem(
                title=item['title'],
                link=item['link'],
                date=item['date'],
                summary=item['summary'],
                source=item['source'],
                category=item['category'],
                keywords=item['keywords'],
                content_hash=collector._generate_hash(item['title'] + item['link'])
            )
            collector.news_items.append(news_item)
        
        collector.df = pd.DataFrame([asdict(item) for item in collector.news_items])
        collector.df['keywords_str'] = collector.df['keywords'].apply(
            lambda x: ', '.join(x) if x else ''
        )
        collector.df = collector.df.sort_values('date', ascending=False).reset_index(drop=True)
    
    return collector


def get_news_data():
    """取得新聞資料"""
    collector = collect_news()
    
    if collector.df is None or collector.df.empty:
        return {'news': [], 'total_count': 0}
    
    from datetime import datetime
    
    return {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_count': len(collector.df),
        'sources': list(collector.df['source'].unique()),
        'categories': list(collector.df['category'].unique()),
        'news': collector.df.to_dict(orient='records')
    }


class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Handler"""
    
    def do_GET(self):
        """處理 GET 請求"""
        path = self.path.split('?')[0]
        
        if path == '/api/news' or path == '/api/news/':
            self._handle_news()
        elif path == '/api/status' or path == '/api/status/':
            self._handle_status()
        elif path == '/api/sources' or path == '/api/sources/':
            self._handle_sources()
        else:
            self._send_json({'error': 'Not Found', 'path': path}, 404)
    
    def do_POST(self):
        """處理 POST 請求"""
        path = self.path.split('?')[0]
        
        if path == '/api/collect' or path == '/api/collect/':
            self._handle_collect()
        else:
            self._send_json({'error': 'Not Found'}, 404)
    
    def _send_json(self, data, status=200):
        """發送 JSON 回應"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _handle_news(self):
        """處理新聞 API"""
        try:
            data = get_news_data()
            self._send_json(data)
        except Exception as e:
            self._send_json({'error': str(e)}, 500)
    
    def _handle_status(self):
        """處理狀態 API"""
        self._send_json({
            'is_running': False,
            'last_update': collector_cache.get('last_update'),
            'total_news': 0,
            'message': '就緒',
            'progress': 100
        })
    
    def _handle_sources(self):
        """處理來源 API"""
        sources = SecurityNewsCollector.DEFAULT_SOURCES
        result = [
            {'name': name, 'url': url, 'is_default': True}
            for name, url in sources.items()
        ]
        self._send_json({'sources': result, 'total': len(result)})
    
    def _handle_collect(self):
        """處理收集請求"""
        try:
            data = get_news_data()
            from datetime import datetime
            collector_cache['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            collector_cache['data'] = data
            
            self._send_json({
                'success': True,
                'message': f"收集完成！共 {data['total_count']} 則新聞",
                'data': data
            })
        except Exception as e:
            self._send_json({
                'success': False,
                'message': str(e)
            }, 500)
    
    def do_OPTIONS(self):
        """處理 CORS 預檢請求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
