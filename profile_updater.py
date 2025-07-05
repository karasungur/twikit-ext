
import json
import asyncio
import time
from tkinter import filedialog
import tkinter as tk
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.client import Client
from models import Profile


async def save_cookies_to_file(client, filename='cookies.json'):
    """Save current cookies to JSON file"""
    try:
        current_cookies = {}
        for cookie in client.http.cookies.jar:
            current_cookies[cookie.name] = cookie.value
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(current_cookies, f, indent=2, ensure_ascii=False)
        print(f"💾 Cookies güncellendi: {filename}")
    except Exception as e:
        print(f"❌ Cookies kaydetme hatası: {e}")


async def load_cookies_and_login():
    """Load cookies from cookies.json and login"""
    try:
        with open('cookies.json', 'r', encoding='utf-8') as f:
            cookies_data = json.load(f)
        
        # Create profile with auth_token from cookies
        profile_data = {
            'auth_token': cookies_data.get('auth_token'),
            'ct0': cookies_data.get('ct0')
        }
        
        profile = Profile(**profile_data)
        client = Client(profile)
        
        # Set all cookies from the file
        client.set_cookies(cookies_data)
        
        # Connect and verify login
        user = await client.connect()
        print(f"✅ Başarıyla giriş yapıldı: @{user.name}")
        
        # Save updated cookies after successful login
        await save_cookies_to_file(client)
        
        return client
        
    except FileNotFoundError:
        print("❌ cookies.json dosyası bulunamadı!")
        return None
    except Exception as e:
        print(f"❌ Giriş hatası: {e}")
        return None


def select_image_file(title="Resim Dosyası Seç"):
    """Open file dialog to select image file"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=[
            ("Resim Dosyaları", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("Tüm Dosyalar", "*.*")
        ]
    )
    
    root.destroy()
    return file_path


async def update_profile_step_by_step(client):
    """Update profile information step by step"""
    
    print("\n🔄 Profil güncelleme işlemi başlıyor...")
    
    # 1. Update name
    print("\n1️⃣ İsim Güncelleme")
    new_name = input("Yeni isim girin (maks 50 karakter): ").strip()
    if new_name:
        try:
            success = await client.change_name(new_name)
            if success:
                print(f"✅ İsim başarıyla güncellendi: {new_name}")
            else:
                print("❌ İsim güncellenemedi")
        except Exception as e:
            print(f"❌ İsim güncelleme hatası: {e}")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    # 2. Update bio
    print("\n2️⃣ Biyografi Güncelleme")
    new_bio = input("Yeni biyografi girin (maks 160 karakter): ").strip()
    try:
        success = await client.change_bio(new_bio)
        if success:
            print(f"✅ Biyografi başarıyla güncellendi: {new_bio}")
        else:
            print("❌ Biyografi güncellenemedi")
    except Exception as e:
        print(f"❌ Biyografi güncelleme hatası: {e}")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    # 3. Update location
    print("\n3️⃣ Lokasyon Güncelleme")
    new_location = input("Yeni lokasyon girin (maks 30 karakter): ").strip()
    try:
        success = await client.change_location(new_location)
        if success:
            print(f"✅ Lokasyon başarıyla güncellendi: {new_location}")
        else:
            print("❌ Lokasyon güncellenemedi")
    except Exception as e:
        print(f"❌ Lokasyon güncelleme hatası: {e}")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    # 4. Update profile photo
    print("\n4️⃣ Profil Resmi Güncelleme")
    print("Profil resmi seçin...")
    profile_image_path = select_image_file("Profil Resmi Seç")
    
    if profile_image_path:
        try:
            success = await client.update_profile_photo(profile_image_path)
            if success:
                print(f"✅ Profil resmi başarıyla güncellendi: {profile_image_path}")
            else:
                print("❌ Profil resmi güncellenemedi")
        except Exception as e:
            print(f"❌ Profil resmi güncelleme hatası: {e}")
    else:
        print("⚠️ Profil resmi seçilmedi, atlanıyor...")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    # 5. Update banner
    print("\n5️⃣ Banner Güncelleme")
    print("Banner resmi seçin...")
    banner_image_path = select_image_file("Banner Resmi Seç")
    
    if banner_image_path:
        try:
            success = await client.update_profile_banner(banner_image_path)
            if success:
                print(f"✅ Banner başarıyla güncellendi: {banner_image_path}")
            else:
                print("❌ Banner güncellenemedi")
        except Exception as e:
            print(f"❌ Banner güncelleme hatası: {e}")
    else:
        print("⚠️ Banner resmi seçilmedi, atlanıyor...")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    # 6. Update username
    print("\n6️⃣ Kullanıcı Adı Güncelleme")
    new_username = input("Yeni kullanıcı adı girin (@ olmadan): ").strip()
    if new_username:
        try:
            success = await client.change_username(new_username)
            if success:
                print(f"✅ Kullanıcı adı başarıyla güncellendi: @{new_username}")
            else:
                print("❌ Kullanıcı adı güncellenemedi")
        except Exception as e:
            print(f"❌ Kullanıcı adı güncelleme hatası: {e}")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    # 7. Update password
    print("\n7️⃣ Şifre Güncelleme")
    current_password = input("Mevcut şifrenizi girin: ").strip()
    if current_password:
        client.profile.password = current_password
        
        new_password = input("Yeni şifre girin: ").strip()
        if new_password:
            try:
                success = await client.change_password(new_password)
                if success:
                    print("✅ Şifre başarıyla güncellendi")
                    print("⚠️ Yeni auth_token otomatik olarak güncellendi")
                else:
                    print("❌ Şifre güncellenemedi")
            except Exception as e:
                print(f"❌ Şifre güncelleme hatası: {e}")
    else:
        print("⚠️ Mevcut şifre girilmedi, şifre güncellemesi atlanıyor...")
    
    print("⏳ 10 saniye bekleniyor...")
    await asyncio.sleep(10)
    
    print("\n🎉 Tüm profil güncelleme işlemleri tamamlandı!")


async def main():
    """Main function"""
    print("🚀 Twitter Profil Güncelleme Aracı")
    print("=" * 40)
    
    # Login with cookies
    client = await load_cookies_and_login()
    if not client:
        return
    
    try:
        # Update profile step by step
        await update_profile_step_by_step(client)
        
        # Save updated cookies
        await save_cookies_to_file(client)
        
        # Save updated profile
        client.profile.save('updated_profile.json')
        print("\n💾 Güncellenmiş profil bilgileri 'updated_profile.json' dosyasına kaydedildi")
        
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
    
    finally:
        # Close client
        await client.close()
        print("\n👋 Bağlantı kapatıldı")


if __name__ == "__main__":
    asyncio.run(main())
