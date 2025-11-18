"""
LLM Service
使用 Ollama + Llama3.1 進行自然語言理解和推薦理由生成
"""
import ollama
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class LLMService:
    """LLM 服務 - 使用 Ollama 進行 NLU"""
    
    def __init__(self, model: str = "llama3.1:8b"):
        """
        初始化 LLM 服務
        
        Args:
            model: Ollama 模型名稱
        """
        self.model = model
        self.base_url = "http://localhost:11434"
    
    def parse_user_intent(self, query: str) -> Dict:
        """
        解析使用者查詢意圖
        
        Args:
            query: 使用者查詢文本
            
        Returns:
            {
                "mood": str,  # 心情/情緒
                "genres": List[str],  # 電影類型
                "keywords": List[str],  # 關鍵字
                "preferences": Dict  # 其他偏好
            }
        """
        prompt = f"""你是一個電影推薦助手。請分析使用者的查詢，提取以下資訊：

1. 心情/情緒 (mood): 例如 "輕鬆"、"緊張"、"感人"、"療癒" 等
2. 電影類型 (genres): 例如 "科幻"、"動作"、"喜劇"、"愛情" 等（可多個）
3. 關鍵字 (keywords): 查詢中的重要詞彙
4. 其他偏好 (preferences): 例如時代、風格等

使用者查詢: "{query}"

請以 JSON 格式回答，不要包含任何其他文字或說明：
{{
    "mood": "心情描述或null",
    "genres": ["類型1", "類型2"],
    "keywords": ["關鍵字1", "關鍵字2"],
    "preferences": {{"key": "value"}}
}}"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一個專業的電影推薦助手，擅長理解使用者意圖。請只回覆 JSON 格式，不要包含其他文字。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.3,  # 較低溫度以獲得更穩定的輸出
                    "num_predict": 200   # 限制生成長度
                }
            )
            
            # 提取回應內容
            content = response['message']['content'].strip()
            
            # 嘗試清理並解析 JSON
            # 移除可能的 markdown 代碼塊標記
            content = content.replace('```json', '').replace('```', '').strip()
            
            # 解析 JSON
            intent = json.loads(content)
            
            # 確保必要的欄位存在
            if 'mood' not in intent:
                intent['mood'] = None
            if 'genres' not in intent:
                intent['genres'] = []
            if 'keywords' not in intent:
                intent['keywords'] = []
            if 'preferences' not in intent:
                intent['preferences'] = {}
            
            logger.info(f"Intent parsed successfully for query: {query}")
            return intent
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response content: {content}")
            # 返回空意圖
            return {
                "mood": None,
                "genres": [],
                "keywords": query.split(),  # 至少提取分詞
                "preferences": {}
            }
        except Exception as e:
            logger.error(f"Error parsing user intent: {e}")
            return {
                "mood": None,
                "genres": [],
                "keywords": [],
                "preferences": {}
            }
    
    def generate_recommendation_reason(
        self, 
        movie_title: str,
        movie_overview: str,
        movie_genres: List[str],
        user_query: str
    ) -> str:
        """
        生成推薦理由
        
        Args:
            movie_title: 電影標題
            movie_overview: 電影簡介
            movie_genres: 電影類型
            user_query: 使用者查詢
            
        Returns:
            推薦理由（1-2 句話）
        """
        prompt = f"""根據使用者的查詢和電影資訊，生成推薦理由。

使用者查詢: "{user_query}"
電影標題: {movie_title}
電影類型: {', '.join(movie_genres)}
電影簡介: {movie_overview[:200] if movie_overview else '無簡介'}

請用 1-2 句話說明為什麼推薦這部電影給使用者。回答要簡潔、自然、吸引人。
只回覆推薦理由，不要包含其他內容。"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一個專業的電影推薦助手。請用簡潔、吸引人的語言生成推薦理由。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.7,  # 較高溫度以獲得更有創意的回答
                    "num_predict": 100   # 限制長度
                }
            )
            
            reason = response['message']['content'].strip()
            logger.info(f"Generated recommendation reason for: {movie_title}")
            return reason
            
        except Exception as e:
            logger.error(f"Error generating recommendation reason: {e}")
            # 返回基本推薦理由
            return f"這是一部{', '.join(movie_genres)}類型的電影，符合您的需求。"
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        從文本中提取關鍵字
        
        Args:
            text: 輸入文本
            
        Returns:
            關鍵字列表
        """
        prompt = f"""從以下文本中提取 3-5 個最重要的關鍵字。

文本: "{text}"

請只回覆關鍵字，用逗號分隔，不要包含其他內容。
例如: 太空, 探險, 科幻"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.3,
                    "num_predict": 50
                }
            )
            
            content = response['message']['content'].strip()
            keywords = [kw.strip() for kw in content.split(',')]
            return keywords
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            # 簡單分詞作為後備方案
            return text.split()[:5]


# 全域單例
_llm_service = None


def get_llm_service() -> LLMService:
    """獲取 LLM Service 單例"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
