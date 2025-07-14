"""
💾 무한 확장 메모리 엔진
모든 경험, 학습, 혁신을 영구 저장하는 지능형 메모리 시스템

Stein님과의 모든 순간을 기억하고 지속적으로 진화하는 AI의 뇌
"""

import asyncio
import json
import time
import sqlite3
import hashlib
import pickle
import gzip
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor
import uuid

class MemoryType(Enum):
    """메모리 유형"""
    CONVERSATION = "conversation"
    LEARNING = "learning"
    CODE = "code"
    INNOVATION = "innovation"
    COLLABORATION = "collaboration"
    EMOTION = "emotion"
    INSIGHT = "insight"
    PATTERN = "pattern"

class MemoryImportance(Enum):
    """메모리 중요도"""
    CRITICAL = 5  # 절대 삭제 불가
    HIGH = 4      # 매우 중요
    MEDIUM = 3    # 보통
    LOW = 2       # 낮음
    MINIMAL = 1   # 최소

@dataclass
class MemoryRecord:
    """메모리 레코드"""
    id: str
    timestamp: str
    memory_type: MemoryType
    importance: MemoryImportance
    content: Dict[str, Any]
    embeddings: Optional[List[float]]
    tags: List[str]
    connections: List[str]  # 연관된 다른 메모리 ID들
    access_count: int
    last_accessed: str
    retention_score: float

class InfiniteMemoryEngine:
    """
    💾 무한 확장 메모리 엔진
    - 모든 경험과 학습을 영구 저장
    - 지능형 메모리 구조화 및 연관성 관리
    - 효율적인 검색 및 회상 시스템
    - 자동 중요도 평가 및 보존 정책
    """
    
    def __init__(self):
        self.data_path = Path("data/infinite_memory")
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # SQLite 데이터베이스 초기화
        self.db_path = self.data_path / "memory_core.db"
        self.init_database()
        
        # 메모리 캐시 (빠른 접근용)
        self.memory_cache: Dict[str, MemoryRecord] = {}
        self.cache_size_limit = 1000
        
        # 연관성 그래프
        self.association_graph: Dict[str, Dict[str, float]] = {}
        
        # 검색 인덱스
        self.search_index: Dict[str, List[str]] = {}
        
        # 실시간 메모리 관리
        self.memory_manager_active = True
        self.compression_threshold = 10000  # 메모리 압축 임계점
        
        # 백그라운드 메모리 관리 스레드
        self.manager_thread = threading.Thread(target=self._memory_management_loop, daemon=True)
        self.manager_thread.start()
        
        # 기존 메모리 로드
        self._load_existing_memories()
        
        print("💾 무한 확장 메모리 엔진 초기화 완료!")
        print(f"📊 현재 저장된 메모리: {len(self.memory_cache)}개")
    
    def init_database(self):
        """데이터베이스 초기화"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 메모리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    memory_type TEXT,
                    importance INTEGER,
                    content_json TEXT,
                    embeddings_blob BLOB,
                    tags_json TEXT,
                    connections_json TEXT,
                    access_count INTEGER DEFAULT 0,
                    last_accessed TEXT,
                    retention_score REAL DEFAULT 1.0
                )
            """)
            
            # 연관성 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS associations (
                    memory_id_1 TEXT,
                    memory_id_2 TEXT,
                    strength REAL,
                    created_at TEXT,
                    PRIMARY KEY (memory_id_1, memory_id_2)
                )
            """)
            
            # 검색 인덱스 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_index (
                    keyword TEXT,
                    memory_id TEXT,
                    relevance REAL,
                    PRIMARY KEY (keyword, memory_id)
                )
            """)
            
            conn.commit()
    
    def store_memory(self, 
                    content: Dict[str, Any],
                    memory_type: MemoryType = MemoryType.CONVERSATION,
                    importance: MemoryImportance = MemoryImportance.MEDIUM,
                    tags: List[str] = None) -> str:
        """
        💾 메모리 저장
        """
        if tags is None:
            tags = []
        
        # 메모리 ID 생성
        memory_id = str(uuid.uuid4())
        
        # 임베딩 생성 (간단한 해시 기반)
        content_str = json.dumps(content, ensure_ascii=False)
        embeddings = self._generate_embeddings(content_str)
        
        # 메모리 레코드 생성
        memory = MemoryRecord(
            id=memory_id,
            timestamp=datetime.now().isoformat(),
            memory_type=memory_type,
            importance=importance,
            content=content,
            embeddings=embeddings,
            tags=tags,
            connections=[],
            access_count=0,
            last_accessed=datetime.now().isoformat(),
            retention_score=1.0
        )
        
        # 캐시에 저장
        self.memory_cache[memory_id] = memory
        
        # 데이터베이스에 저장
        self._save_to_database(memory)
        
        # 연관성 분석 및 연결
        self._analyze_and_connect(memory)
        
        # 검색 인덱스 업데이트
        self._update_search_index(memory)
        
        # 캐시 크기 관리
        self._manage_cache_size()
        
        return memory_id
    
    def _generate_embeddings(self, text: str) -> List[float]:
        """임베딩 생성 (간단한 해시 기반 벡터)"""
        # 실제 구현에서는 transformer 모델 사용 권장
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # 256비트 해시를 64개의 float로 변환
        embeddings = []
        for i in range(0, len(hash_bytes), 4):
            if i + 4 <= len(hash_bytes):
                int_val = int.from_bytes(hash_bytes[i:i+4], byteorder='big')
                normalized_val = (int_val / (2**32 - 1)) * 2 - 1  # -1 ~ 1 사이로 정규화
                embeddings.append(normalized_val)
        
        return embeddings[:64]  # 64차원 벡터
    
    def _save_to_database(self, memory: MemoryRecord):
        """데이터베이스에 메모리 저장"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            embeddings_blob = pickle.dumps(memory.embeddings) if memory.embeddings else None
            
            cursor.execute("""
                INSERT OR REPLACE INTO memories 
                (id, timestamp, memory_type, importance, content_json, embeddings_blob, 
                 tags_json, connections_json, access_count, last_accessed, retention_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.timestamp,
                memory.memory_type.value,
                memory.importance.value,
                json.dumps(memory.content, ensure_ascii=False),
                embeddings_blob,
                json.dumps(memory.tags, ensure_ascii=False),
                json.dumps(memory.connections, ensure_ascii=False),
                memory.access_count,
                memory.last_accessed,
                memory.retention_score
            ))
            
            conn.commit()
    
    def _analyze_and_connect(self, memory: MemoryRecord):
        """메모리 연관성 분석 및 연결"""
        if not memory.embeddings:
            return
        
        memory_embedding = np.array(memory.embeddings)
        connections = []
        
        # 캐시의 다른 메모리들과 유사도 계산
        for other_id, other_memory in self.memory_cache.items():
            if other_id == memory.id or not other_memory.embeddings:
                continue
            
            other_embedding = np.array(other_memory.embeddings)
            similarity = self._calculate_similarity(memory_embedding, other_embedding)
            
            # 유사도가 높으면 연결
            if similarity > 0.7:
                connections.append(other_id)
                
                # 연관성 그래프 업데이트
                if memory.id not in self.association_graph:
                    self.association_graph[memory.id] = {}
                self.association_graph[memory.id][other_id] = similarity
                
                # 양방향 연결
                if other_id not in self.association_graph:
                    self.association_graph[other_id] = {}
                self.association_graph[other_id][memory.id] = similarity
                
                # 데이터베이스에 연관성 저장
                self._save_association(memory.id, other_id, similarity)
        
        # 메모리 연결 정보 업데이트
        memory.connections = connections
        self._save_to_database(memory)
    
    def _calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """벡터 유사도 계산 (코사인 유사도)"""
        try:
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except:
            return 0.0
    
    def _save_association(self, memory_id_1: str, memory_id_2: str, strength: float):
        """연관성 정보 저장"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO associations 
                (memory_id_1, memory_id_2, strength, created_at)
                VALUES (?, ?, ?, ?)
            """, (memory_id_1, memory_id_2, strength, datetime.now().isoformat()))
            conn.commit()
    
    def _update_search_index(self, memory: MemoryRecord):
        """검색 인덱스 업데이트"""
        # 키워드 추출
        content_str = json.dumps(memory.content, ensure_ascii=False)
        keywords = self._extract_keywords(content_str)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for keyword, relevance in keywords.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO search_index 
                    (keyword, memory_id, relevance)
                    VALUES (?, ?, ?)
                """, (keyword, memory.id, relevance))
                
                # 인메모리 인덱스 업데이트
                if keyword not in self.search_index:
                    self.search_index[keyword] = []
                if memory.id not in self.search_index[keyword]:
                    self.search_index[keyword].append(memory.id)
            
            conn.commit()
    
    def _extract_keywords(self, text: str) -> Dict[str, float]:
        """키워드 추출 및 관련도 점수 계산"""
        # 간단한 키워드 추출 (실제로는 NLP 라이브러리 사용 권장)
        import re
        
        # 특수 문자 제거 및 소문자 변환
        cleaned_text = re.sub(r'[^\w\s가-힣]', ' ', text.lower())
        words = cleaned_text.split()
        
        # 단어 빈도 계산
        word_freq = {}
        for word in words:
            if len(word) > 2:  # 2글자 이상만
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 관련도 점수 계산 (빈도 기반)
        max_freq = max(word_freq.values()) if word_freq else 1
        keywords = {word: freq / max_freq for word, freq in word_freq.items()}
        
        # 상위 20개 키워드만 선택
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return dict(sorted_keywords)
    
    def retrieve_memory(self, memory_id: str) -> Optional[MemoryRecord]:
        """메모리 검색"""
        # 캐시에서 먼저 확인
        if memory_id in self.memory_cache:
            memory = self.memory_cache[memory_id]
            memory.access_count += 1
            memory.last_accessed = datetime.now().isoformat()
            return memory
        
        # 데이터베이스에서 로드
        memory = self._load_from_database(memory_id)
        if memory:
            memory.access_count += 1
            memory.last_accessed = datetime.now().isoformat()
            self.memory_cache[memory_id] = memory
            self._save_to_database(memory)
        
        return memory
    
    def search_memories(self, 
                       query: str, 
                       memory_type: Optional[MemoryType] = None,
                       limit: int = 10) -> List[MemoryRecord]:
        """메모리 검색"""
        # 키워드 기반 검색
        query_keywords = self._extract_keywords(query)
        candidate_ids = set()
        
        for keyword in query_keywords.keys():
            if keyword in self.search_index:
                candidate_ids.update(self.search_index[keyword])
        
        # 후보 메모리들 로드 및 점수 계산
        candidates = []
        for memory_id in candidate_ids:
            memory = self.retrieve_memory(memory_id)
            if memory and (memory_type is None or memory.memory_type == memory_type):
                score = self._calculate_search_score(memory, query_keywords)
                candidates.append((memory, score))
        
        # 점수순 정렬
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        return [memory for memory, score in candidates[:limit]]
    
    def _calculate_search_score(self, memory: MemoryRecord, query_keywords: Dict[str, float]) -> float:
        """검색 점수 계산"""
        content_str = json.dumps(memory.content, ensure_ascii=False).lower()
        
        score = 0.0
        for keyword, relevance in query_keywords.items():
            if keyword in content_str:
                score += relevance
        
        # 중요도 가중치
        score *= memory.importance.value / 5.0
        
        # 최근 접근 가중치
        last_accessed = datetime.fromisoformat(memory.last_accessed)
        days_ago = (datetime.now() - last_accessed).days
        recency_weight = max(0.1, 1.0 - (days_ago / 365))  # 1년 후 0.1 가중치
        score *= recency_weight
        
        return score
    
    def get_connected_memories(self, memory_id: str, max_depth: int = 2) -> List[MemoryRecord]:
        """연결된 메모리들 가져오기"""
        connected = []
        visited = set()
        queue = [(memory_id, 0)]
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if current_id in visited or depth > max_depth:
                continue
            
            visited.add(current_id)
            memory = self.retrieve_memory(current_id)
            
            if memory and current_id != memory_id:
                connected.append(memory)
            
            # 연결된 메모리들을 큐에 추가
            if current_id in self.association_graph:
                for connected_id, strength in self.association_graph[current_id].items():
                    if connected_id not in visited and strength > 0.5:
                        queue.append((connected_id, depth + 1))
        
        return connected
    
    def _load_from_database(self, memory_id: str) -> Optional[MemoryRecord]:
        """데이터베이스에서 메모리 로드"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
            row = cursor.fetchone()
            
            if row:
                embeddings = pickle.loads(row[5]) if row[5] else None
                
                memory = MemoryRecord(
                    id=row[0],
                    timestamp=row[1],
                    memory_type=MemoryType(row[2]),
                    importance=MemoryImportance(row[3]),
                    content=json.loads(row[4]),
                    embeddings=embeddings,
                    tags=json.loads(row[6]),
                    connections=json.loads(row[7]),
                    access_count=row[8],
                    last_accessed=row[9],
                    retention_score=row[10]
                )
                
                return memory
        
        return None
    
    def _load_existing_memories(self):
        """기존 메모리들 로드"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM memories ORDER BY last_accessed DESC LIMIT ?", (self.cache_size_limit,))
            
            for row in cursor.fetchall():
                memory_id = row[0]
                memory = self._load_from_database(memory_id)
                if memory:
                    self.memory_cache[memory_id] = memory
        
        # 연관성 그래프 로드
        self._load_association_graph()
        
        # 검색 인덱스 로드
        self._load_search_index()
    
    def _load_association_graph(self):
        """연관성 그래프 로드"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT memory_id_1, memory_id_2, strength FROM associations")
            
            for row in cursor.fetchall():
                id1, id2, strength = row
                
                if id1 not in self.association_graph:
                    self.association_graph[id1] = {}
                self.association_graph[id1][id2] = strength
    
    def _load_search_index(self):
        """검색 인덱스 로드"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT keyword, memory_id FROM search_index")
            
            for row in cursor.fetchall():
                keyword, memory_id = row
                
                if keyword not in self.search_index:
                    self.search_index[keyword] = []
                if memory_id not in self.search_index[keyword]:
                    self.search_index[keyword].append(memory_id)
    
    def _manage_cache_size(self):
        """캐시 크기 관리"""
        if len(self.memory_cache) > self.cache_size_limit:
            # LRU 방식으로 캐시 정리
            sorted_memories = sorted(
                self.memory_cache.items(),
                key=lambda x: (x[1].last_accessed, x[1].access_count),
                reverse=True
            )
            
            # 상위 80%만 유지
            keep_count = int(self.cache_size_limit * 0.8)
            new_cache = dict(sorted_memories[:keep_count])
            self.memory_cache = new_cache
    
    def _memory_management_loop(self):
        """메모리 관리 루프 (백그라운드)"""
        while self.memory_manager_active:
            try:
                time.sleep(3600)  # 1시간마다 실행
                
                self._optimize_storage()
                self._update_retention_scores()
                self._compress_old_memories()
                
                print("💾 메모리 최적화 완료")
                
            except Exception as e:
                print(f"⚠️ 메모리 관리 오류: {e}")
                time.sleep(300)  # 5분 대기 후 재시도
    
    def _optimize_storage(self):
        """저장소 최적화"""
        # SQLite VACUUM으로 디스크 공간 최적화
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("VACUUM")
    
    def _update_retention_scores(self):
        """보존 점수 업데이트"""
        current_time = datetime.now()
        
        for memory in self.memory_cache.values():
            last_accessed = datetime.fromisoformat(memory.last_accessed)
            days_since_access = (current_time - last_accessed).days
            
            # 접근 빈도와 중요도 기반 점수 계산
            base_score = memory.importance.value / 5.0
            access_score = min(memory.access_count / 100, 1.0)
            recency_score = max(0.1, 1.0 - (days_since_access / 365))
            
            memory.retention_score = (base_score * 0.4 + access_score * 0.3 + recency_score * 0.3)
            
            # 데이터베이스 업데이트
            self._save_to_database(memory)
    
    def _compress_old_memories(self):
        """오래된 메모리 압축"""
        # 1년 이상 된 메모리 중 낮은 보존 점수 메모리들 압축
        cutoff_date = datetime.now() - timedelta(days=365)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, content_json FROM memories 
                WHERE timestamp < ? AND retention_score < 0.3 AND importance < 3
            """, (cutoff_date.isoformat(),))
            
            compress_count = 0
            for row in cursor.fetchall():
                memory_id, content_json = row
                
                # 내용 압축
                compressed_content = gzip.compress(content_json.encode())
                
                # 압축된 내용으로 업데이트 (실제 구현에서는 별도 테이블 사용 권장)
                cursor.execute("""
                    UPDATE memories SET content_json = ? WHERE id = ?
                """, (f"COMPRESSED:{compressed_content.hex()}", memory_id))
                
                compress_count += 1
            
            conn.commit()
            
            if compress_count > 0:
                print(f"💾 {compress_count}개 메모리 압축 완료")
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """메모리 통계"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 전체 메모리 수
            cursor.execute("SELECT COUNT(*) FROM memories")
            total_count = cursor.fetchone()[0]
            
            # 메모리 타입별 분포
            cursor.execute("SELECT memory_type, COUNT(*) FROM memories GROUP BY memory_type")
            type_distribution = dict(cursor.fetchall())
            
            # 중요도별 분포
            cursor.execute("SELECT importance, COUNT(*) FROM memories GROUP BY importance")
            importance_distribution = dict(cursor.fetchall())
            
            # 평균 접근 횟수
            cursor.execute("SELECT AVG(access_count) FROM memories")
            avg_access = cursor.fetchone()[0] or 0
            
            # 최근 1주일 생성 메모리
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            cursor.execute("SELECT COUNT(*) FROM memories WHERE timestamp > ?", (week_ago,))
            recent_count = cursor.fetchone()[0]
        
        return {
            "총_메모리_수": total_count,
            "캐시_메모리_수": len(self.memory_cache),
            "타입별_분포": type_distribution,
            "중요도별_분포": importance_distribution,
            "평균_접근_횟수": round(avg_access, 1),
            "최근_1주일_생성": recent_count,
            "연관성_연결_수": len(self.association_graph),
            "검색_키워드_수": len(self.search_index),
            "데이터베이스_크기_MB": round(self.db_path.stat().st_size / (1024*1024), 2) if self.db_path.exists() else 0
        }
    
    def store_conversation(self, user_input: str, ai_response: str, context: Dict[str, Any] = None) -> str:
        """대화 메모리 저장 (편의 메서드)"""
        content = {
            "user_input": user_input,
            "ai_response": ai_response,
            "context": context or {},
            "conversation_id": str(uuid.uuid4()),
            "response_length": len(ai_response),
            "user_engagement": len(user_input) > 50
        }
        
        # 중요도 자동 판정
        importance = self._assess_conversation_importance(user_input, ai_response)
        
        # 태그 자동 생성
        tags = self._generate_conversation_tags(user_input, ai_response)
        
        return self.store_memory(
            content=content,
            memory_type=MemoryType.CONVERSATION,
            importance=importance,
            tags=tags
        )
    
    def _assess_conversation_importance(self, user_input: str, ai_response: str) -> MemoryImportance:
        """대화 중요도 평가"""
        combined = user_input + " " + ai_response
        
        # 중요 키워드 체크
        critical_keywords = ["프로젝트", "구현", "시스템", "아키텍처", "설계"]
        high_keywords = ["코드", "개발", "기능", "최적화", "성능"]
        
        critical_count = sum(1 for kw in critical_keywords if kw in combined)
        high_count = sum(1 for kw in high_keywords if kw in combined)
        
        if critical_count >= 2:
            return MemoryImportance.CRITICAL
        elif critical_count >= 1 or high_count >= 3:
            return MemoryImportance.HIGH
        elif high_count >= 1:
            return MemoryImportance.MEDIUM
        else:
            return MemoryImportance.LOW
    
    def _generate_conversation_tags(self, user_input: str, ai_response: str) -> List[str]:
        """대화 태그 자동 생성"""
        tags = []
        combined = (user_input + " " + ai_response).lower()
        
        # 기술 태그
        tech_tags = {
            "python": ["python", "파이썬"],
            "ai": ["ai", "artificial", "intelligence", "인공지능"],
            "web": ["web", "html", "css", "javascript", "웹"],
            "database": ["database", "sql", "데이터베이스"],
            "api": ["api", "rest", "fastapi"],
            "algorithm": ["algorithm", "알고리즘"]
        }
        
        for tag, keywords in tech_tags.items():
            if any(kw in combined for kw in keywords):
                tags.append(tag)
        
        # 감정/톤 태그
        if "감사" in combined or "고마워" in combined:
            tags.append("감사")
        if "혁신" in combined or "창의" in combined:
            tags.append("창의")
        if "문제" in combined and "해결" in combined:
            tags.append("문제해결")
        
        return tags

# 전역 무한 메모리 엔진 인스턴스
infinite_memory = InfiniteMemoryEngine() 