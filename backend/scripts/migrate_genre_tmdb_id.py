"""
為現有資料庫添加 tmdb_id 欄位到 genres 表
"""
import sqlite3
import sys

def add_tmdb_id_to_genres():
    try:
        conn = sqlite3.connect('cinemood.db')
        cursor = conn.cursor()
        
        # 檢查 tmdb_id 是否已存在
        cursor.execute('PRAGMA table_info(genres)')
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'tmdb_id' in columns:
            print("✅ tmdb_id 欄位已存在")
        else:
            print("📝 添加 tmdb_id 欄位...")
            cursor.execute('ALTER TABLE genres ADD COLUMN tmdb_id INTEGER')
            
            # 為現有資料設置 tmdb_id（使用 id 作為臨時值）
            cursor.execute('UPDATE genres SET tmdb_id = id WHERE tmdb_id IS NULL')
            
            conn.commit()
            print("✅ 成功添加 tmdb_id 欄位")
        
        # 顯示更新後的結構
        cursor.execute('PRAGMA table_info(genres)')
        print("\n更新後的 genres 表結構:")
        for row in cursor.fetchall():
            print(f"  {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_tmdb_id_to_genres()
