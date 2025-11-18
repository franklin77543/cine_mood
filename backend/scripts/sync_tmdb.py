"""
TMDB 資料同步腳本
從 TMDB API 獲取電影資料並同步到本地資料庫
"""

import sys
import os

# 將 backend 目錄加入 Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.services.tmdb_client import tmdb_client
from app.models.movie_model import Movie
from app.models.genre_model import Genre
from app.models.person_model import Person
from app.models.movie_genre_model import MovieGenre
from app.models.movie_credit_model import MovieCredit
from typing import List, Dict, Any
import uuid
from datetime import datetime


def init_db():
    """初始化資料庫表"""
    print("📦 初始化資料庫...")
    Base.metadata.create_all(bind=engine)
    print("✅ 資料庫初始化完成")


def sync_genres(db: Session) -> Dict[int, int]:
    """
    同步電影類型
    
    Returns:
        TMDB genre_id 到本地 genre_id 的映射
    """
    print("\n🎬 同步電影類型...")
    
    genres_data = tmdb_client.get_genres()
    if not genres_data:
        print("❌ 獲取類型失敗")
        return {}
    
    genre_map = {}
    
    for genre_data in genres_data:
        tmdb_genre_id = genre_data["id"]
        genre_name = genre_data["name"]
        
        # 檢查類型是否已存在
        existing_genre = db.query(Genre).filter(Genre.name == genre_name).first()
        
        if existing_genre:
            genre_map[tmdb_genre_id] = existing_genre.id
        else:
            new_genre = Genre(name=genre_name)
            db.add(new_genre)
            db.flush()  # 獲取自動生成的 ID
            genre_map[tmdb_genre_id] = new_genre.id
            print(f"  ➕ 新增類型: {genre_name}")
    
    db.commit()
    print(f"✅ 類型同步完成，共 {len(genre_map)} 個類型")
    
    return genre_map


def sync_movie(
    db: Session,
    movie_data: Dict[str, Any],
    genre_map: Dict[int, int]
) -> bool:
    """
    同步單部電影資料
    
    Args:
        db: 資料庫 Session
        movie_data: TMDB 電影資料
        genre_map: 類型 ID 映射
    
    Returns:
        是否成功同步
    """
    tmdb_id = movie_data["id"]
    
    # 檢查電影是否已存在
    existing_movie = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
    if existing_movie:
        return False  # 已存在，跳過
    
    # 獲取電影詳細資料
    details = tmdb_client.get_movie_details(tmdb_id)
    if not details:
        print(f"  ⚠️  無法獲取電影詳情: TMDB ID {tmdb_id}")
        return False
    
    # 獲取演職人員資料
    credits = tmdb_client.get_movie_credits(tmdb_id)
    
    # 處理 release_date (字串 -> date 物件)
    release_date = None
    if details.get("release_date"):
        try:
            release_date = datetime.strptime(details["release_date"], "%Y-%m-%d").date()
        except ValueError:
            pass  # 日期格式錯誤，設為 None
    
    # 建立電影記錄
    movie = Movie(
        id=str(uuid.uuid4()),
        tmdb_id=tmdb_id,
        title=details.get("title", ""),
        original_title=details.get("original_title", ""),
        overview=details.get("overview", ""),
        release_date=release_date,
        runtime=details.get("runtime"),
        vote_average=details.get("vote_average", 0.0),
        vote_count=details.get("vote_count", 0),
        popularity=details.get("popularity", 0.0),
        poster_path=details.get("poster_path"),
        backdrop_path=details.get("backdrop_path"),
    )
    
    db.add(movie)
    db.flush()  # 確保電影已儲存並獲取 ID
    
    # 同步類型關聯（注意：詳情 API 返回的是 genres 陣列，不是 genre_ids）
    for genre in details.get("genres", []):
        genre_id = genre.get("id")
        if genre_id in genre_map:
            movie_genre = MovieGenre(
                movie_id=movie.id,
                genre_id=genre_map[genre_id]
            )
            db.add(movie_genre)
    
    # 同步演職人員
    if credits:
        # 同步演員（前 10 名）
        added_actors = set()  # 追蹤已加入的演員，避免重複
        for i, cast in enumerate(credits.get("cast", [])[:10]):
            person = sync_person(db, cast)
            if person and person.id not in added_actors:
                credit = MovieCredit(
                    movie_id=movie.id,
                    person_id=person.id,
                    role="actor",
                    character=cast.get("character", ""),
                    order_num=i
                )
                db.add(credit)
                added_actors.add(person.id)
        
        # 同步導演
        added_directors = set()  # 追蹤已加入的導演，避免重複
        for crew in credits.get("crew", []):
            if crew.get("job") == "Director":
                person = sync_person(db, crew)
                if person and person.id not in added_directors:
                    credit = MovieCredit(
                        movie_id=movie.id,
                        person_id=person.id,
                        role="director",
                        character="",
                        order_num=0
                    )
                    db.add(credit)
                    added_directors.add(person.id)
    
    print(f"  ✅ {movie.title} ({movie.release_date})")
    
    return True


def sync_person(db: Session, person_data: Dict[str, Any]) -> Person:
    """
    同步演員/導演資料
    
    Args:
        db: 資料庫 Session
        person_data: TMDB 人員資料
    
    Returns:
        Person 實例
    """
    tmdb_id = person_data["id"]
    
    # 檢查是否已存在
    existing_person = db.query(Person).filter(Person.tmdb_id == tmdb_id).first()
    if existing_person:
        return existing_person
    
    # 建立新人員記錄
    person = Person(
        id=str(uuid.uuid4()),
        tmdb_id=tmdb_id,
        name=person_data.get("name", ""),
        profile_path=person_data.get("profile_path")
    )
    
    db.add(person)
    db.flush()
    
    return person


def sync_movies_from_endpoint(
    db: Session,
    endpoint_name: str,
    endpoint_func,
    genre_map: Dict[int, int],
    max_pages: int = 5
) -> int:
    """
    從指定的 TMDB 端點同步電影
    
    Args:
        db: 資料庫 Session
        endpoint_name: 端點名稱（用於顯示）
        endpoint_func: TMDB Client 的方法
        genre_map: 類型 ID 映射
        max_pages: 最多獲取幾頁
    
    Returns:
        成功同步的電影數量
    """
    print(f"\n🎥 同步 {endpoint_name}...")
    
    synced_count = 0
    
    for page in range(1, max_pages + 1):
        print(f"\n  📄 第 {page}/{max_pages} 頁")
        
        data = endpoint_func(page=page)
        if not data or "results" not in data:
            print(f"  ⚠️  獲取第 {page} 頁失敗")
            break
        
        movies = data["results"]
        
        for movie_data in movies:
            if sync_movie(db, movie_data, genre_map):
                synced_count += 1
        
        db.commit()  # 每頁提交一次
    
    print(f"\n✅ {endpoint_name} 同步完成，新增 {synced_count} 部電影")
    
    return synced_count


def main():
    """主同步流程"""
    print("=" * 60)
    print("🚀 CineMood - TMDB 資料同步")
    print("=" * 60)
    
    # 初始化資料庫
    init_db()
    
    # 建立資料庫 Session
    db = SessionLocal()
    
    try:
        # 1. 同步類型
        genre_map = sync_genres(db)
        
        if not genre_map:
            print("❌ 類型同步失敗，中止同步")
            return
        
        # 2. 同步熱門電影（前 5 頁 = ~100 部，約 200 requests）
        popular_count = sync_movies_from_endpoint(
            db,
            "熱門電影",
            tmdb_client.get_popular_movies,
            genre_map,
            max_pages=5
        )
        
        # 3. 同步高評分電影（前 5 頁 = ~100 部，約 200 requests）
        top_rated_count = sync_movies_from_endpoint(
            db,
            "高評分電影",
            tmdb_client.get_top_rated_movies,
            genre_map,
            max_pages=5
        )
        
        # 4. 同步正在上映（前 3 頁 = ~60 部，約 120 requests）
        now_playing_count = sync_movies_from_endpoint(
            db,
            "正在上映",
            tmdb_client.get_now_playing_movies,
            genre_map,
            max_pages=3
        )
        
        # 統計資料
        total_movies = db.query(Movie).count()
        total_people = db.query(Person).count()
        total_genres = db.query(Genre).count()
        
        print("\n" + "=" * 60)
        print("📊 同步統計")
        print("=" * 60)
        print(f"  電影總數: {total_movies}")
        print(f"  演職人員: {total_people}")
        print(f"  電影類型: {total_genres}")
        print(f"  本次新增: {popular_count + top_rated_count + now_playing_count} 部")
        print("=" * 60)
        print("✅ 同步完成！")
        
    except Exception as e:
        print(f"\n❌ 同步過程發生錯誤: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
