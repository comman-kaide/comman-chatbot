"""
初期管理者ユーザーを作成するスクリプト
"""
import sys
from app.database import SessionLocal, User, init_db
from app.auth import get_password_hash

def create_admin_user(username: str, email: str, password: str):
    """管理者ユーザーを作成"""
    # データベース初期化
    init_db()

    db = SessionLocal()

    try:
        # 既存ユーザーのチェック
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            print(f"エラー: ユーザー名 '{username}' またはメールアドレス '{email}' は既に使用されています。")
            return False

        # 管理者ユーザーの作成
        admin_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_admin=True,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print("=" * 50)
        print("✅ 管理者ユーザーを作成しました!")
        print("=" * 50)
        print(f"ユーザー名: {username}")
        print(f"メールアドレス: {email}")
        print(f"パスワード: {password}")
        print("=" * 50)
        print("\n⚠️  このパスワードを安全に保管してください!")
        print("初回ログイン後、パスワードを変更することをお勧めします。\n")

        return True

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # デフォルト値
    default_username = "admin"
    default_email = "admin@comman.co.jp"
    default_password = "comman2024"

    print("=" * 50)
    print("株式会社カンマン チャットボット")
    print("管理者ユーザー作成スクリプト")
    print("=" * 50)
    print()

    # 対話形式での入力
    username = input(f"ユーザー名 (デフォルト: {default_username}): ").strip() or default_username
    email = input(f"メールアドレス (デフォルト: {default_email}): ").strip() or default_email
    password = input(f"パスワード (デフォルト: {default_password}): ").strip() or default_password

    print()

    # ユーザー作成実行
    success = create_admin_user(username, email, password)

    if success:
        print("管理画面にログインできます:")
        print("URL: http://localhost:3000 (開発環境)")
        print("または本番環境の管理画面URL")
        sys.exit(0)
    else:
        sys.exit(1)
