"""
檢查資料庫同步狀態
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

def main():
    db = SessionLocal()
    
    try:
        # 統計資料
        movie_count = db.query(Movie).count()
        genre_count = db.query(Genre).count()
        person_count = db.query(Person).count()
        credit_count = db.query(MovieCredit).count()
        movie_genre_count = db.query(MovieGenre).count()
        
        print("=" * 60)
        print("📊 CineMood 資料庫統計")
        print("=" * 60)
        print(f"  電影總數: {movie_count}")
        print(f"  類型數量: {genre_count}")
        print(f"  演職人員: {person_count}")
        print(f"  演職關聯: {credit_count}")
        print(f"  類型關聯: {movie_genre_count}")
        print("=" * 60)
        
        # 顯示最近的 10 部電影
        if movie_count > 0:
            print("\n🎬 最近同步的 10 部電影:")
            recent_movies = db.query(Movie).order_by(Movie.created_at.desc()).limit(10).all()
            for i, movie in enumerate(recent_movies, 1):
                print(f"  {i}. {movie.title} ({movie.release_date})")
                print(f"     TMDB ID: {movie.tmdb_id}, 評分: {movie.vote_average}/10")
        
        # 顯示所有類型
        if genre_count > 0:
            print("\n🎭 電影類型列表:")
            genres = db.query(Genre).all()
            genre_names = [g.name for g in genres]
            print(f"  {', '.join(genre_names)}")
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
