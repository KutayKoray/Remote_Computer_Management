import instaloader
import os
import shutil

profil_kullanıcı_adı = "sand.tagious"

L = instaloader.Instaloader()
profil = instaloader.Profile.from_username(L.context, profil_kullanıcı_adı)

gönderiler = profil.get_posts()

for gönderi in gönderiler:
    L.download_post(gönderi, profil_kullanıcı_adı)



# Dosya dizini
# dizin = "./baddiestr"

# # Klasörleri oluştur
# # os.makedirs(os.path.join(dizin, "0"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "1"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "2"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "3"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "4"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "5"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "6"), exist_ok=True)
# # os.makedirs(os.path.join(dizin, "7"), exist_ok=True)
# os.makedirs(os.path.join(dizin, "8"), exist_ok=True)
# os.makedirs(os.path.join(dizin, "9"), exist_ok=True)
# os.makedirs(os.path.join(dizin, "10"), exist_ok=True)
# os.makedirs(os.path.join(dizin, "mp4"), exist_ok=True)
    

# # Dosyaları taşı
# for dosya in os.listdir(dizin):
#     # if dosya.endswith(".xz"):
#     #     os.remove(os.path.join(dizin, dosya))
#     # if dosya.endswith("UTC.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "0", dosya))
#     # elif dosya.endswith("_1.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "1", dosya))
#     # elif dosya.endswith("_2.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "2", dosya))
#     # elif dosya.endswith("_3.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "3", dosya))
#     # elif dosya.endswith("_4.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "4", dosya))
#     # elif dosya.endswith("_5.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "5", dosya))
#     # elif dosya.endswith("_6.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "6", dosya))
#     # elif dosya.endswith("_7.jpg"):
#     #     shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "7", dosya))    
#     # elif dosya.endswith("_8.jpg"):
#         # shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "8", dosya))
#     if dosya.endswith("_9.jpg"):
#         shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "9", dosya))
#     elif dosya.endswith("_10.jpg"):
#         shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "10", dosya))
#     elif dosya.endswith(".mp4"):
#         shutil.move(os.path.join(dizin, dosya), os.path.join(dizin, "mp4", dosya))


