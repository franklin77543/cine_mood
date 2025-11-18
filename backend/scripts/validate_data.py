"""
資料驗證腳本 - Phase 1 Step 3
檢查資料完整性、中文支援、關聯關係
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.movie_model import Movie
from app.models.genre_model import Genre
from app.models.person_model import Person
from app.models.movie_credit_model import MovieCredit
from app.models.movie_genre_model import MovieGenre
from sqlalchemy import func


def validate_chinese_support(db):
    """驗證中文支援"""
    print("\n📝 驗證中文支援...")
    
    # 檢查有中文標題的電影
    chinese_movies = db.query(Movie).filter(
        Movie.title.like('%中%') |
        Movie.title.like('%的%') |
        Movie.title.like('%人%')
    ).limit(5).all()
    
    if chinese_movies:
        print(f"  ✅ 找到 {len(chinese_movies)} 部中文標題電影:")
        for movie in chinese_movies:
            print(f"     • {movie.title}")
    else:
        print("  ⚠️  未找到中文標題電影（可能都是外語片）")
    
    # 檢查有中文簡介的電影
    movies_with_overview = db.query(Movie).filter(
        Movie.overview.isnot(None),
        Movie.overview != ""
    ).limit(3).all()
    
    print(f"\n  ✅ 簡介範例（前 3 部）:")
    for movie in movies_with_overview:
        overview = movie.overview[:50] + "..." if len(movie.overview) > 50 else movie.overview
        print(f"     • {movie.title}: {overview}")


def validate_genres(db):
    """驗證類型資料"""
    print("\n🎭 驗證電影類型...")
    
    # 每個類型的電影數量
    genre_counts = db.query(
        Genre.name,
        func.count(MovieGenre.movie_id).label('count')
    ).join(MovieGenre, Genre.id == MovieGenre.genre_id)\
     .group_by(Genre.name)\
     .order_by(func.count(MovieGenre.movie_id).desc())\
     .all()
    
    print(f"  ✅ 類型分布（前 10）:")
    for genre_name, count in genre_counts[:10]:
        print(f"     • {genre_name}: {count} 部電影")
    
    # 檢查沒有類型的電影
    movies_without_genre = db.query(Movie).outerjoin(MovieGenre).filter(
        MovieGenre.movie_id.is_(None)
    ).count()
    
    if movies_without_genre > 0:
        print(f"\n  ⚠️  {movies_without_genre} 部電影沒有類型標籤")
    else:
        print(f"\n  ✅ 所有電影都有類型標籤")


def validate_credits(db):
    """驗證演職人員資料"""
    print("\n🎬 驗證演職人員...")
    
    # 演員數量 vs 導演數量
    actor_count = db.query(MovieCredit).filter(MovieCredit.role == 'actor').count()
    director_count = db.query(MovieCredit).filter(MovieCredit.role == 'director').count()
    
    print(f"  ✅ 演員記錄: {actor_count}")
    print(f"  ✅ 導演記錄: {director_count}")
    
    # 找出參演最多電影的演員
    top_actors = db.query(
        Person.name,
        func.count(MovieCredit.movie_id).label('movie_count')
    ).join(MovieCredit, Person.id == MovieCredit.person_id)\
     .filter(MovieCredit.role == 'actor')\
     .group_by(Person.name)\
     .order_by(func.count(MovieCredit.movie_id).desc())\
     .limit(5).all()
    
    print(f"\n  ✅ 參演最多的演員（前 5）:")
    for name, count in top_actors:
        print(f"     • {name}: {count} 部電影")
    
    # 檢查沒有演職人員的電影
    movies_without_credits = db.query(Movie).outerjoin(MovieCredit).filter(
        MovieCredit.movie_id.is_(None)
    ).count()
    
    if movies_without_credits > 0:
        print(f"\n  ⚠️  {movies_without_credits} 部電影沒有演職人員資料")
    else:
        print(f"\n  ✅ 所有電影都有演職人員資料")


def validate_movie_data(db):
    """驗證電影基本資料"""
    print("\n🎥 驗證電影資料完整性...")
    
    total_movies = db.query(Movie).count()
    
    # 檢查各欄位完整性
    movies_with_title = db.query(Movie).filter(Movie.title.isnot(None)).count()
    movies_with_overview = db.query(Movie).filter(
        Movie.overview.isnot(None),
        Movie.overview != ""
    ).count()
    movies_with_release_date = db.query(Movie).filter(Movie.release_date.isnot(None)).count()
    movies_with_poster = db.query(Movie).filter(Movie.poster_path.isnot(None)).count()
    movies_with_rating = db.query(Movie).filter(Movie.vote_average > 0).count()
    
    print(f"  ✅ 標題完整性: {movies_with_title}/{total_movies} ({movies_with_title/total_movies*100:.1f}%)")
    print(f"  ✅ 簡介完整性: {movies_with_overview}/{total_movies} ({movies_with_overview/total_movies*100:.1f}%)")
    print(f"  ✅ 上映日期: {movies_with_release_date}/{total_movies} ({movies_with_release_date/total_movies*100:.1f}%)")
    print(f"  ✅ 海報圖片: {movies_with_poster}/{total_movies} ({movies_with_poster/total_movies*100:.1f}%)")
    print(f"  ✅ 評分資料: {movies_with_rating}/{total_movies} ({movies_with_rating/total_movies*100:.1f}%)")
    
    # 評分分布
    rating_ranges = [
        (0, 4, "低分"),
        (4, 6, "中下"),
        (6, 7, "中等"),
        (7, 8, "優良"),
        (8, 10, "優秀")
    ]
    
    print(f"\n  📊 評分分布:")
    for min_rating, max_rating, label in rating_ranges:
        count = db.query(Movie).filter(
            Movie.vote_average >= min_rating,
            Movie.vote_average < max_rating
        ).count()
        if count > 0:
            print(f"     • {label} ({min_rating}-{max_rating}): {count} 部")


def sample_movie_with_details(db):
    """隨機抽取電影顯示完整資訊"""
    print("\n🎬 隨機電影範例:")
    
    # 抽取一部有完整資料的電影
    movie = db.query(Movie).filter(
        Movie.overview.isnot(None),
        Movie.overview != ""
    ).first()
    
    if movie:
        print(f"\n  標題: {movie.title}")
        print(f"  原始標題: {movie.original_title}")
        print(f"  上映日期: {movie.release_date}")
        print(f"  評分: {movie.vote_average}/10 ({movie.vote_count} 票)")
        print(f"  人氣度: {movie.popularity}")
        
        # 類型
        genres = db.query(Genre.name).join(MovieGenre).filter(
            MovieGenre.movie_id == movie.id
        ).all()
        if genres:
            genre_names = [g.name for g in genres]
            print(f"  類型: {', '.join(genre_names)}")
        
        # 導演
        directors = db.query(Person.name).join(MovieCredit).filter(
            MovieCredit.movie_id == movie.id,
            MovieCredit.role == 'director'
        ).all()
        if directors:
            director_names = [d.name for d in directors]
            print(f"  導演: {', '.join(director_names)}")
        
        # 主要演員（前 5）
        actors = db.query(Person.name, MovieCredit.character).join(MovieCredit).filter(
            MovieCredit.movie_id == movie.id,
            MovieCredit.role == 'actor'
        ).order_by(MovieCredit.order_num).limit(5).all()
        
        if actors:
            print(f"  主要演員:")
            for name, character in actors:
                char_info = f" 飾演 {character}" if character else ""
                print(f"     • {name}{char_info}")
        
        # 簡介
        overview = movie.overview[:100] + "..." if len(movie.overview) > 100 else movie.overview
        print(f"  簡介: {overview}")


def main():
    print("=" * 60)
    print("🔍 CineMood 資料驗證 - Phase 1 Step 3")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. 基本統計
        total_movies = db.query(Movie).count()
        total_genres = db.query(Genre).count()
        total_people = db.query(Person).count()
        total_credits = db.query(MovieCredit).count()
        total_movie_genres = db.query(MovieGenre).count()
        
        print(f"\n📊 資料庫統計:")
        print(f"  • 電影: {total_movies} 部")
        print(f"  • 類型: {total_genres} 種")
        print(f"  • 演職人員: {total_people} 位")
        print(f"  • 演職關聯: {total_credits} 筆")
        print(f"  • 類型關聯: {total_movie_genres} 筆")
        
        # 2. 中文支援驗證
        validate_chinese_support(db)
        
        # 3. 類型驗證
        validate_genres(db)
        
        # 4. 演職人員驗證
        validate_credits(db)
        
        # 5. 電影資料驗證
        validate_movie_data(db)
        
        # 6. 範例電影
        sample_movie_with_details(db)
        
        print("\n" + "=" * 60)
        print("✅ 資料驗證完成！")
        print("=" * 60)
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
