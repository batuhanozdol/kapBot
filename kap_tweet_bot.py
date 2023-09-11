#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 10:02:13 2023

@author: batuhanozdol
"""

import tweepy
import requests
from bs4 import BeautifulSoup
import tweepy
import time
import datetime
from selenium import webdriver
from os import environ

API_KEY = environ["API_KEY"]
API_KEY_SECRET = environ["API_SECRET"]
BEARER_TOKEN = environ["BEARER_TOKEN"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = environ["ACCESS_TOKEN_SECRET"]


client = tweepy.Client(consumer_key=API_KEY,
                       consumer_secret=API_KEY_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)


subject = ""
dosya_adi = "sontweet.txt"
baslangic_saat = datetime.time(9, 30)  # Saat 9:30
bitis_saat = datetime.time(17, 0)    # Saat 17:00
# Şu anki tarihi alın
bugun = datetime.date.today()


def get_new_content():
    # Web tarayıcısını başlatın
    driver = webdriver.Chrome()  # Chrome tarayıcı kullanıldı, tarayıcıyı indirmeniz gerekebilir
    
    # Web sitesini ziyaret edin
    driver.get("https://www.kap.org.tr/tr/")
    
    # Sayfanın yüklenmesini bekle
    driver.implicitly_wait(5)  # Örnek olarak 10 saniye bekleyebilirsiniz
    
    # Sayfanın kaynak kodunu alın
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # İçeriği çekmek için gerekli BeautifulSoup işlemlerini yapın
    vcell_spans = soup.find_all('span', class_="vcell")

    return vcell_spans

def write_to_file(text):
    # Dosyaya yazma işlemi
    with open(dosya_adi, "w") as dosya:
        dosya.truncate(0)
        dosya.write(text)

def read_from_file():
    try:
        # Dosyayı okuma işlemi
        with open(dosya_adi, "r") as dosya:
            icerik = dosya.read()
            return icerik
    except FileNotFoundError:
        return ""

def getShortNameForBistCompany(companyName):
    # Dosya adını ve yolu burada belirtin
    dosya_adı = "bist.txt"

    # Şirket bilgilerini tutmak için bir sözlük oluşturun
    sirketler = {}

    # Dosyayı okuyun ve her satırı işleyin
    with open(dosya_adı, 'r', encoding='utf-8') as dosya:
        for satır in dosya:
            # Satırı boşluğa göre böleriz, örneğin "APPL APPLE INC." gibi
            parçalar = satır.strip().split()
            
            # Parçaları kısaltma ve uzun isim olarak ayırın
            if len(parçalar) >= 2:
                kisaltma = parçalar[0]
                uzun_isim = ' '.join(parçalar[1:])
                
                # Şirket bilgilerini sözlüğe ekleyin
                sirketler[kisaltma] = uzun_isim

    # Sonucu görüntüleyin
    for kisaltma, uzun_isim in sirketler.items():
        if (uzun_isim.lower().strip() in companyName.lower().strip()):
            return kisaltma
    return ""

# Haftaiçi günlerini (Pazartesi'den Cuma'ya kadar) kontrol edin
if 0 <= bugun.weekday() <= 4:
    while(True):
        
        su_an = datetime.datetime.now().time()
    
        # Şu anki saat belirtilen saat aralığında ise "Hello, World!" yazdır
        if baslangic_saat <= su_an <= bitis_saat:
        
            # Web sitesinden içeriği alın
            new_content = get_new_content()
            subject = read_from_file()
            
            if (subject != new_content[13].text.strip()):
                sirketKisaltmasi = getShortNameForBistCompany(new_content[11].text.strip())
                
                if (sirketKisaltmasi != ""):
                    content = new_content[11].text.strip() + " #" + sirketKisaltmasi + "\n\n📍" + new_content[13].text.strip()
                else:
                    content = new_content[11].text.strip() + "\n\n📍" + new_content[13].text.strip()
                    
                if (new_content[14].text.strip() != ""):
                    content += "\n\n🔺" + new_content[14].text.strip() + "\n\n #bist100 #bist #bist30 #borsa #xu100"
                else :
                    content += "\n\n #bist100 #bist #bist30 #borsa #xu100"
                    
                subject = new_content[13].text.strip()
            
                # İçeriği tweet atın
                response = client.create_tweet(text=content)
                
                write_to_file(subject)
                
            time.sleep(360)
        else:
            time.sleep(1200)
        




