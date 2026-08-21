# ============================================================
#  services/insta_poster_service.py
#  ATLAS Platformasi — Instagram to Telegram & YouTube AutoPoster Moduli
# ============================================================

import os
import sys
import re
import json
import time
import asyncio
import tempfile
import threading
import subprocess
import requests
import telebot
from datetime import datetime, timezone, timedelta
from services.atlas_db import get_db_connection

UZB_TZ = timezone(timedelta(hours=5))

def get_uzb_now():
    """Toshkent (O'zbekiston, UTC+5) bo'yicha joriy vaqtni olish"""
    return datetime.now(timezone.utc).astimezone(UZB_TZ).replace(tzinfo=None)

DEFAULT_BOT_TOKEN = "8818017813:AAEJTzJ97jCPIYy5exZSjFNHOcSvcHkjDJk"
DEFAULT_TARGET_CHAT_ID = "-1004295470034"
DEFAULT_INSTA_USERNAME = "shahrisabz_t_t_uz"

# Barcha 74 ta Video Reels postlar (DTHudhLiEJT dan keyingi yangi postlar, eskisidan yangisiga qarab)
DEFAULT_SEEDED_POSTS = [
    {
        "shortcode": "DTNEIiLCBPn",
        "post_url": "https://www.instagram.com/reel/DTNEIiLCBPn",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nHammada shunaqami?🤦🏻‍♀️\n\n#top #trendy #rek #top #sh_t_t\nView all 59 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/610781553_17854335450603794_8273537095932445673_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ig_cache_key=MzgwNDcxNTQzODgzMjA5NjIzMTE3ODU0MzM1NDQ3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=-AY9itddX1oQ7kNvwG1W3LN&_nc_oc=AdrP_0q-tYcHdgFs1AljZSlMjfkLVYZW-YPx5zBIfIHI1X_lxpQ3s-CO1EwmMksbCTM&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=nXHdVaV_cdOZrGMpFFKT_w&_nc_ss=7aa8c&oh=00_AQGRuSK2B6tz4xRZAyFQlySo2UKh_2vG50P2f5v7EqJUGw&oe=6A8DF2F6",
        "post_date": ""
    },
    {
        "shortcode": "DTVcl6SCM8c",
        "post_url": "https://www.instagram.com/reel/DTVcl6SCM8c",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBir muhabbat tarixi😂\n\n#top #trendy #rek #sh_t_t\nView all 135 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/612104661_17854780650603794_6009500926953552661_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=111&_nc_map=urlgen_bucketless&ig_cache_key=MzgwNzA3NDgxMDUxNDE2NTUzMjE3ODU0NzgwNjQ0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=UbAVI5nJJssQ7kNvwGdWaFx&_nc_oc=AdoMh5kdv4POh7MQuVTqmAgPrv00oRXWTQ3AtX4xVZWaMXiVAOD-4prjWfbLBRRf4zo&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=HtoIqsWmFshp-GrNPpxJiA&_nc_ss=7aa8c&oh=00_AQHuYIoZHBXuhW5DCOPRjaqmJ7rKbkahF_fdoc1Am_zeuw&oe=6A8DF568",
        "post_date": ""
    },
    {
        "shortcode": "DTZ6oL_iF_9",
        "post_url": "https://www.instagram.com/reel/DTZ6oL_iF_9",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nSiz 1 misz yoki 2😂\n\n#top #trendy #rek #sh_t_t\nView all 52 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/613765717_17855004117603794_4839733021772996227_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=MzgwODMzMjgwODI3MjI0MDYzNzE3ODU1MDA0MTE0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=onDyC4jpJcUQ7kNvwG8s7ne&_nc_oc=Ado91iyzhE13FvPEyx0FD8Pun6dJMLalYD2dVdZ7HTGpXiUQ5aiw2Mao_Hy-bd786js&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=W_ECJq83rwCymTSntnOiMA&_nc_ss=7aa8c&oh=00_AQHcvhuYdwjrwUU21fG8zJQplWZcjXJ27vTBYlakmk7bhg&oe=6A8DFE31",
        "post_date": ""
    },
    {
        "shortcode": "DTfs3bGCEpw",
        "post_url": "https://www.instagram.com/reel/DTfs3bGCEpw",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShifokor — bu nafaqat kasb, balki inson hayotini asrashga bag‘ishlangan buyuk mas’uliyat.🤍\n\n#top #sh_t_t #trendy #rek\nView all 81 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/616818049_17855305548603794_1899069972058223454_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ig_cache_key=MzgwOTk2MTEzMjQ4ODY3MzkwNDE3ODU1MzA1NTQyNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=96Uhg9yhiVEQ7kNvwFvQ7jz&_nc_oc=Adri_EALEKS9zBRrV5qtAFqw9ooP2v2FqYMX9n9FXVKzEW3ou7tXUg3Wgjfb-HATuTM&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=K4uzf4r9HzRTUQyFVJws3A&_nc_ss=7aa8c&oh=00_AQFVFJGNNyN5Ge7aghdCibZrhHUqW1IIby3w_VVwYnuyiw&oe=6A8DDBDD",
        "post_date": ""
    },
    {
        "shortcode": "DTkQ2h0CGiL",
        "post_url": "https://www.instagram.com/reel/DTkQ2h0CGiL",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa do’stlar bormi?😁\n\n#top #trendy #rek #sh_t_t\nView all 70 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/616318553_17855651202603794_5591778728880140138_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=104&_nc_map=urlgen_bucketless&ig_cache_key=MzgxMTI0NTMwMDU2NDY1MDEyMzE3ODU1NjUxMTk2NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=GRNAcqMwVTMQ7kNvwFx2AZ_&_nc_oc=AdquwKil1dnvkKEAnHEFHNU6LT6kzGn3zJWnRM1OU08iXfR1Ek5CgLaBm9v4CG7eVCs&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=XkKLzGs53SZK9GPSQN7bUA&_nc_ss=7aa8c&oh=00_AQFBsWYvGe0YM8iR1BmSlAPmyeuxw_OpHK7EBg4UsGv9ew&oe=6A8DEA71",
        "post_date": ""
    },
    {
        "shortcode": "DTsk6bBiMni",
        "post_url": "https://www.instagram.com/reel/DTsk6bBiMni",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBo’lganmi?😂\n\n#top #trendy #sh_t_t #rek\nView all 57 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/618676351_17856092994603794_5101200529822619216_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=109&_nc_map=urlgen_bucketless&ig_cache_key=MzgxMzU4NTMyODg5Njc4ODk2MjE3ODU2MDkyOTkxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=29x8XaKyeMIQ7kNvwEcf94-&_nc_oc=AdrGVJmWe45czkfDMdrwai9IZhkwxfsa-5FfElslbhpqfdIHTwQ0W6ZtqhJuCEcMaO8&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=SeeseRUZ5K2wNP27iYZjwg&_nc_ss=7aa8c&oh=00_AQFnGrRQOnFar5RPgIsfDcZ5N-yMkjdZwoll1LHoitSl9w&oe=6A8DF431",
        "post_date": ""
    },
    {
        "shortcode": "DT5ZwpSCPP5",
        "post_url": "https://www.instagram.com/reel/DT5ZwpSCPP5",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa do’stlarga yuborib qo’yila😁\n\n#rek #top #shtt\nView all 64 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.71878-15/620908910_4446553802242829_8273568673076963822_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=MzgxNzE5NTQ1MzE5Njg1ODM2MTE3ODU2NzEwODk1NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=2gi8acI9B5sQ7kNvwF_HdrO&_nc_oc=AdrkXaHouUk5TGKuC7nUljeDJW6TLU8-TKDnGvMfukiBtQBVFN4GXociGlFPLZFO9Zg&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=3y_Hg2INFnHsWVUvrBagag&_nc_ss=7aa8c&oh=00_AQHl_GepQvX4DUI3pNL42mfdimu7_F6Nqyb2IxYSCODLdg&oe=6A8DEE5B",
        "post_date": ""
    },
    {
        "shortcode": "DT-zcCLiB8H",
        "post_url": "https://www.instagram.com/reel/DT-zcCLiB8H",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nU bilim olishni tanladi🐧🥹\n\n#top #rek #sh_t_t #trendy #shtt\nView all 35 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.71878-15/622973060_3368883893286916_1155082809039139195_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=MzgxODcxNTc2MDkxNTEyODA3MQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=E5BUbZXAWJIQ7kNvwGs33ul&_nc_oc=Adqoxap8yYd7NfOpFPiRWMMDOw4SS447Lb2jSnZKz3qsn6N_nso9ZjakgG-3Ks0GdRA&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=NL5jh59yfKHZ32RCoXbOiQ&_nc_ss=7aa8c&oh=00_AQF7H2GzUYQFhAOLYKSNRyjP045cQLIBpwMR9ed78TLqNQ&oe=6A8DF717",
        "post_date": ""
    },
    {
        "shortcode": "DUAQjBGCB4A",
        "post_url": "https://www.instagram.com/reel/DUAQjBGCB4A",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nQishki qabullar boshlandi!!!\n\n#rek #top #sh_t_t #trendy #rek\nView all 33 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.71878-15/621684784_919085487263903_1200299497726139712_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=MzgxOTEyNTI1OTExMDk4MTEyMDE3ODU3MDk0NDEyNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=g1XkXKl_Pi4Q7kNvwFX0DmV&_nc_oc=AdrAYWUnwcdDut6lTVan9acjY0HuajpfHFjY4Bk7zx3x52et_BJTRkQCpCFfaVE53nU&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=pEpABnqKM8SDuBach1k32A&_nc_ss=7aa8c&oh=00_AQGGv_Gw3m8LLlYTss5YPXJ5f6r8nU_z8g2gxAQOJ10WWQ&oe=6A8DDAFE",
        "post_date": ""
    },
    {
        "shortcode": "DUFqF5JCCaH",
        "post_url": "https://www.instagram.com/reel/DUFqF5JCCaH",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBuvijonni gaplariga quloq solamiz😁\n\n#rek #top #sh_t_t #trendy #top\nView all 100 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.71878-15/624071038_1610688246924095_8346877269672530139_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=MzgyMDY0NDk4MTc5OTM5Njk5OQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=nMVd93oqK2YQ7kNvwFTlXkE&_nc_oc=Adp9bJkYL_nEFEFUauEMkQtuKEFh--LogqEcaGAx45p3tJV3AlEWXr5wJ-8UPdikLJY&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=w6_c3yyJrj3k_x6FBl0qZQ&_nc_ss=7aa8c&oh=00_AQHpac7WbctWefxOK2A_vNbpNVyU03c4xuRllq2wRuEsJA&oe=6A8DD637",
        "post_date": ""
    },
    {
        "shortcode": "DUNkpDriCCw",
        "post_url": "https://www.instagram.com/reel/DUNkpDriCCw",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBildirsoyda nma bor😁\n\n#top #sh_t_t #rek #trendy\nView all 46 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.71878-15/627039937_740486352452854_6768456279248154060_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=MzgyMjg3MjgwOTgzMTkzMjA4MDE3ODU3ODMxNjA4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=pE2W51IENjIQ7kNvwEDw_w2&_nc_oc=AdowhWcdRW3ESk8SDWlORQ9CH3HXe_Ujm68EMjtWw7v_5UXIUYzekyUzHnJ92dtuY0Y&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=zCOy8obfWFdKf1MyaEspCw&_nc_ss=7aa8c&oh=00_AQHm4u4uKUuu6uzwm_19xuXh5zs7iT0ejecaaFC6NgLbqA&oe=6A8DDE50",
        "post_date": ""
    },
    {
        "shortcode": "DUTJbgRCKCG",
        "post_url": "https://www.instagram.com/reel/DUTJbgRCKCG",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa do’stlaga yuborib qo’yamiz😁\n\n#top #sh_t_t #rek #trendy\nView all 44 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/624871087_17858135610603794_2214074215272740923_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=MzgyNDQ0MTk4MTA1NzY3MTMwMjE3ODU4MTM1NjA0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=otuutcrMR98Q7kNvwEt6yDz&_nc_oc=AdrH-WDI2Y_2Ajp20AjQIkkBWkhghxnXRG8EioB66C_fHs1WTFmLul3iWlFae8NpwFM&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=NcQA13uIK2cn7DyeD7mGOA&_nc_ss=7aa8c&oh=00_AQGLcHv4Rt2eFsht8--viFx1EyTSh-DPzbSjYIGERi_0Tg&oe=6A8DE00C",
        "post_date": ""
    },
    {
        "shortcode": "DUXtJcICKwZ",
        "post_url": "https://www.instagram.com/reel/DUXtJcICKwZ",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa talabalar bormi?😁\n\n#top #sh_t_t #rek #trendy\nView all 40 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/625869900_17858367486603794_4810474513453082532_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=111&_nc_map=urlgen_bucketless&ig_cache_key=MzgyNTcyNDk2OTI0MjM3MzE0NTE3ODU4MzY3NDgzNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=fVLL_HXcLcoQ7kNvwHHcUSb&_nc_oc=Adp7_wVK0bKzPOOLj5tvqYg2XsCYQlN9FPDX7q6NqXayu7Xwomqm_KDVzr-v-SFDjss&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=FOQNzrcoSE9B16V9bgd_Bw&_nc_ss=7aa8c&oh=00_AQFJQCjSylNHpMhteEgwgFA8ucNOtx3ttK8gmunqW94shA&oe=6A8DE617",
        "post_date": ""
    },
    {
        "shortcode": "DUfO8fKiKKO",
        "post_url": "https://www.instagram.com/reel/DUfO8fKiKKO",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nQishki qabullar davom etmoqda\n\n#rek #top #sh_t_t #trendy\nView all 37 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/626279469_17858780973603794_8431793573115617281_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=109&_nc_map=urlgen_bucketless&ig_cache_key=MzgyNzg0MzkzNzU3MDY5Mzc3NDE3ODU4NzgwOTY3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=Fj0GMI-DlS4Q7kNvwEdHnMK&_nc_oc=Adrr3MbRH9iPxUxgMFyFTek9BK1HPn75Hyy6OyxUQe95rohRJSq0MohnJVk9uQ37vlE&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=3OlEqQ48jmYhXClPa081Vg&_nc_ss=7aa8c&oh=00_AQEekTykSLtX2LfKW9RNUOfOOXBSi6rfDCuQmVGhe1p_JA&oe=6A8E0555",
        "post_date": ""
    },
    {
        "shortcode": "DUpmMSWiM6Z",
        "post_url": "https://www.instagram.com/reel/DUpmMSWiM6Z",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa talabalar bormi?😂\n\n#top #sh_t_t #rek #trendy\nView all 25 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/626274292_17859323334603794_1640976625973940690_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=109&_nc_map=urlgen_bucketless&ig_cache_key=MzgzMDc2MDkyODE2MTg3NzY1NzE3ODU5MzIzMzMxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=9NevYvdX4pcQ7kNvwFbYCDx&_nc_oc=AdrJaf-jSmevnrun611cFnRSOlqsy9qLQEOpNmWC6T_x7vkF50C6tFCFafIbeZ2VGAk&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=Dce8qRCTL_oPvKEOpCEMTQ&_nc_ss=7aa8c&oh=00_AQHI228kiqajviuFkhXYjFZyUqK7hgRUeaaudNZ5GlDwUA&oe=6A8DD922",
        "post_date": ""
    },
    {
        "shortcode": "DUtKLNjCMdN",
        "post_url": "https://www.instagram.com/reel/DUtKLNjCMdN",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunchaki trend 😁\n\n#top #rek #sh_t_t #trendy\nView all 38 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/631797373_17859526953603794_8828224679904856768_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=MzgzMTc2MzYwODg4NzkzNjg0NTE3ODU5NTI2OTQ3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=p6jpdDewyAkQ7kNvwHTfiOO&_nc_oc=AdqqkSxuyA762GSaWwezJz6admoyJjLBE4d906dKo-vTDhFFPqSJfbXHSenKMpgy6Z4&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=tyjyJujEB61lqU0h7hPfWg&_nc_ss=7aa8c&oh=00_AQH-CrWJfscWLRlnXOCI3VQ3Hl57BTOzXdfmp5ezVhTuFA&oe=6A8DF0F6",
        "post_date": ""
    },
    {
        "shortcode": "DUx6qpGCHkF",
        "post_url": "https://www.instagram.com/reel/DUx6qpGCHkF",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nAtaylab kechikadiganla bormi?😂\n\n#top #sh_t_t #rek #trendy\nView all 34 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/630198810_17859820209603794_1884983112286867221_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=MzgzMzEwMjc3NDkwOTMwMzA0NTE3ODU5ODIwMjAzNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=eHOfVoCbGvkQ7kNvwGDCtjy&_nc_oc=AdqZYj2cZxmjdThqdCHGDGSOx_yGkR5xlbGH4hmkTXLO6Vt40dV-TER53Qm-kBYBvVE&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=YRt_VH_wOwvl80iQXfLdag&_nc_ss=7aa8c&oh=00_AQHIZUtMgx-JPVwqD4zSEh12bnETlKR_LQBal_xyFnexMw&oe=6A8DF0A0",
        "post_date": ""
    },
    {
        "shortcode": "DU2t0CjCHe3",
        "post_url": "https://www.instagram.com/reel/DU2t0CjCHe3",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa talabalar juda ko’p to’g’rimi?😁\n\n#top #sh_t_t #rek #trendy\nView all 25 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/638309215_17860074819603794_3313066125879698132_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=104&_nc_map=urlgen_bucketless&ig_cache_key=MzgzNDQ1MzYyMDk5MzU4NzEyNzE3ODYwMDc0ODE2NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=8bbF2roDH9wQ7kNvwFIz1lo&_nc_oc=AdpHHqpddwER2mP-gXEGUkhAuB_nVPy3o9CTiwr2oW_x2yt7dYVbwJmyV5_yKvWanJI&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=strl_BY9rY3ZH8DqdxcYsA&_nc_ss=7aa8c&oh=00_AQH5qosZXunxQbR1Hjb3vwrC49VmL-2r5seyvD4jni6_yQ&oe=6A8DDD3E",
        "post_date": ""
    },
    {
        "shortcode": "DU54oq3CO87",
        "post_url": "https://www.instagram.com/reel/DU54oq3CO87",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nAssalomu alaykum!\nKirib kelgan muqaddas Ramadan oyi muborak bo‘lsin! 🤲🌙\n\nAlloh tutgan ro‘zalarimizni, qilgan ibodatlarimizni, duolarimizni qabul aylasin.\nBu oy xonadoningizga tinchlik, qalbingizga xotirjamlik, hayotingizga baraka olib kelsin.\nRamazon oyida qilgan har bir yaxshiligingiz o‘zingizga ming karra qaytsin.\n\n#top #sh_t_t #rek #trendy\nView all comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.71878-15/634591444_1227298869515755_2702214579590344354_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=MzgzNTM0NTY0MzA4Njg2ODI4MzE3ODYwMjQ4NjYwNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=um7UQHubn_EQ7kNvwH0km5_&_nc_oc=Adr1a2UtzvVP59cCi9sQOvPHQ6LflqwoZKUJEJ1GXPLBv5Fld_6xQm5J-9-w4YdqGo0&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=BrccKplziJRS_Xn_qibhdA&_nc_ss=7aa8c&oh=00_AQFQLBYvTdb1cNZcnTsjYsaZQgFfT3xs-Y1RTSgpTkWvRQ&oe=6A8E0AE7",
        "post_date": ""
    },
    {
        "shortcode": "DVIjRREiIrl",
        "post_url": "https://www.instagram.com/reel/DVIjRREiIrl",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBo’lganmi?😂\n\n#top #rek #trendy #sh_t_t\nView all 41 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/640314685_17861052657603794_8126300758667421218_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=111&_nc_map=urlgen_bucketless&ig_cache_key=MzgzOTQ3MzgwMDUyMjAwOTMxNzE3ODYxMDUyNjU0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=aZjDZQHo2jcQ7kNvwE9s55G&_nc_oc=AdouW39K0ol2BxlzzqOlC9zzBFZfr5regOYJqjNA1Zz2_UQ9-2hKZyPru8muMWOJyyc&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=gGTnrxNksky09zJCbX35sw&_nc_ss=7aa8c&oh=00_AQHDZa3yMnOLvD5sJaELtE0_R92RodE5m5-9GW05XCLbrw&oe=6A8DDB08",
        "post_date": ""
    },
    {
        "shortcode": "DVNoH20CPvf",
        "post_url": "https://www.instagram.com/reel/DVNoH20CPvf",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nMedik😌\n\n#top #sh_t_t #rek #trendy\nView all 24 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/640419003_17861341467603794_274728346241980243_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzg0MDkwMjUxODk2ODc0NDkyNzE3ODYxMzQxNDY0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=myHpz_c7wOEQ7kNvwEhZ3lj&_nc_oc=AdoQ_aqQ6GKMBbShred-LngXzcGzxUeCG_3P8FZeZDtiUFe7dAHk5uqfn4DJvPGa9HA&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=DIVnYgbvhGRJCKP3HF4eHA&_nc_ss=7aa8c&oh=00_AQFayzxE9YSSyy3yAXeE_59p_oCfPL3LJs9H7HVVe3cPNA&oe=6A8DD718",
        "post_date": ""
    },
    {
        "shortcode": "DVVe3uRCEFb",
        "post_url": "https://www.instagram.com/reel/DVVe3uRCEFb",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nLo’liga 😂\n\n#top #sh_t_t #rek #trendy\nView all 42 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/641246106_17861839272603794_7967914859451737245_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ig_cache_key=Mzg0MzExMzYyNzY3NTAxNzU2MzE3ODYxODM5MjY5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=J5Qhb91USYYQ7kNvwEZhOnn&_nc_oc=AdrYUi1g9zCi-WGO48LdGlt48ypcw-_N7tPiLwuiMb6EMeDwQBZ45VT3L7oy1700EDw&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=2NcCT5QSotPyBgMCDhxMtg&_nc_ss=7aa8c&oh=00_AQE4Nyg59YxS-FtsETgFZh7eilWjw-6wiU_czbxC-wJykA&oe=6A8E0324",
        "post_date": ""
    },
    {
        "shortcode": "DVdIhEDiNIt",
        "post_url": "https://www.instagram.com/reel/DVdIhEDiNIt",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nQabul hali ham davom etmoqda✅\n\n#top #sh_t_t #rek #trendy\nView all 34 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/642503346_17862662595603794_8868701518946796304_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=109&_nc_map=urlgen_bucketless&ig_cache_key=Mzg0NTI2NzExMzMxMzM1ODM4MTE3ODYyNjYyNTg5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=uMG6-uMLb-MQ7kNvwGqGOCE&_nc_oc=Adqjf0CeN9T1LecF6-QLcmqB7ooQ82xR5DrHjGb1i4mhjIamg7hopm0ifFFZ4i_SoEs&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=z5ahkAim5d-hydxjvqTBpQ&_nc_ss=7aa8c&oh=00_AQHe3Fr5LQ23ORT9GdCEhuoitFlPjTA05rEJghGGD3a1RA&oe=6A8DE587",
        "post_date": ""
    },
    {
        "shortcode": "DVizuydiPhQ",
        "post_url": "https://www.instagram.com/reel/DVizuydiPhQ",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nRuzador talabala qanisila?👀😂\n\n#rek #top #sh_t_t #trendy\nView all 22 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.71878-15/626274080_1245631757035835_6591845505124691298_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=104&_nc_map=urlgen_bucketless&ig_cache_key=Mzg0Njg2NDU0NzM3ODQyNzk4NA%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=ydyO6LhU2bYQ7kNvwH3u98G&_nc_oc=AdolN5k3Bqj3ul6c0ZyzZWsSkekoe4l8wVQNpZmrWw5qqeaSoYle08IKVvuFT5Ib4jk&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=zb99Xu2NJbIs7cx7MuSogg&_nc_ss=7aa8c&oh=00_AQH7CUDelfMehcZrrQBlwDqGuU4eg3QhvlPko-OdhOCHSg&oe=6A8DFE09",
        "post_date": ""
    },
    {
        "shortcode": "DVp7_HiiDbt",
        "post_url": "https://www.instagram.com/reel/DVp7_HiiDbt",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nSHTTdan ajoyib taklif:\n\nTexnikum jamoasi kengaymoqda!\n\nMatematika\nFizika\nOna tili\nKimyo\nBiologiya\nIngliz tili\n\nKeling, yoshlar kelajagini birgalikda quramiz! Bizning ahil jamoamizga qo‘shiling!!!\n\nBatafsil ma’lumot: +998 97 587 46 57\nView all 18 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.71878-15/642975061_969494118946370_7629759141177621588_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzg0ODg3MTE3ODczMTUzNDA2MQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=7qgAYNsabSYQ7kNvwGPD5AU&_nc_oc=Adow5qJiNi_V8JvP0NrWOlyVaD22cQaBf9iCoN3Bw-_nfcpi64hxCRtm946VYqlX8q4&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=xOBABXoDlnTWfRP_ua4UNg&_nc_ss=7aa8c&oh=00_AQHxCQUNTtqP-QJjrKGxslZePegESRP50iTXxcqZYtB2NA&oe=6A8DEC1C",
        "post_date": ""
    },
    {
        "shortcode": "DVvOB48iNtB",
        "post_url": "https://www.instagram.com/reel/DVvOB48iNtB",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n3-paradan keyin hammada shunaqami?😂\n\n#top #sh_t_t #rek #trendy\nView all 28 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/649225540_17863480374603794_7361355992944530199_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzg1MDM1NzkwODk0MDgzOTc0NTE3ODYzNDgwMzcxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=MG5Vy81zvkQQ7kNvwFkF0XY&_nc_oc=AdrXP_HjhrWjZJ7mTzfeIiRs2WgtL-a_lBE7K_Ded8ORDfuC8sr0bpb1zWcWTI3icdw&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=3OHMAqXpluzb2b-rNQHKzg&_nc_ss=7aa8c&oh=00_AQFXwf2sCVcGatdrQqa7u4kBOuE4JCjg43TiT2inM283Xw&oe=6A8E0612",
        "post_date": ""
    },
    {
        "shortcode": "DV0kxwXiOZr",
        "post_url": "https://www.instagram.com/reel/DV0kxwXiOZr",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nXatolarini tushunib yetgan talabalar bormi?😂\n\n#top #sh_t_t #rek #trendy #shtt\nView all 24 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/651237540_17863810629603794_1739866319928772259_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=109&_nc_map=urlgen_bucketless&ig_cache_key=Mzg1MTg2NTMzMDE3MTgzMTkxNTE3ODYzODEwNjIzNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=2qx5Yz0p-cEQ7kNvwE4swol&_nc_oc=AdqQjqMLGrIUrNdlwGMmWYRxxTLC_MyHzD4P_Tkgh9krkl28dKv7Ndch5yrjtDmEa5I&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=3sOZEDx-h-GmsWcSACasxw&_nc_ss=7aa8c&oh=00_AQFHrBnKdm7FR7YfZV8yDUZEqiU0fk7mWgSJxVRx_VbRDg&oe=6A8DD838",
        "post_date": ""
    },
    {
        "shortcode": "DV6NKXpiEir",
        "post_url": "https://www.instagram.com/reel/DV6NKXpiEir",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n1-kurslar shu yerdamisila?😁\n\n#top #sh_t_t #rek #trendy #shtt\nView all 18 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.71878-15/651043924_1459103595674615_4697717673100468782_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=Mzg1MzQ1MDMxODM2MTE1MTY1OTE3ODY0MTcyNzExNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=WzaRGeUx1u0Q7kNvwGbKmNB&_nc_oc=AdpMvNxuvWa9qLw3QBk9j6LK8NG9pkYVfO9kPBE5vAi35z10IpuvHdXkDUQPrLxkq-k&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=FX9wd0JIYLLbF7HygDIv8g&_nc_ss=7aa8c&oh=00_AQGpQYj06x_jvQgEvwEoANV7SmnpLCJv2z42UhX4VscPsQ&oe=6A8E084A",
        "post_date": ""
    },
    {
        "shortcode": "DWBZI4FiOfr",
        "post_url": "https://www.instagram.com/reel/DWBZI4FiOfr",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShahrisabz tibbiyot texnikumi ✅\n\n#top #sh_t_t #rek #trendy\nView all 32 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.71878-15/654488208_1455479886171210_7572868809851804576_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=Mzg1NTQ3MzMxNzE0Njg0NzIxMTE3ODY0NjI1MjYxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=wpjLKqUjAVQQ7kNvwELXFPE&_nc_oc=AdrFenUxgCopKRdeZ4ttKmTREy2d-3b8j-_O9ny4Ej_4O1O8vK_7_ki74srDeoxRHNk&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=xunGzu55QLkxGE_YFR_PDA&_nc_ss=7aa8c&oh=00_AQHgDxG4nuqmqpAYexgf67tuvLhTQxv7TR5mJEYdHtmCyg&oe=6A8E043B",
        "post_date": ""
    },
    {
        "shortcode": "DWTpURNCDlO",
        "post_url": "https://www.instagram.com/reel/DWTpURNCDlO",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nNavro‘z – bu shunchaki bayram emas, bu yangilanish, mehr-oqibat va ezgulik ramzi 🌿\nBu kun qalblarga iliqlik, yuzlarga tabassum va hayotga yangi umidlar olib kiradi.\n\n#top #sh_t_t #rek #navruz\nView all 38 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/655878665_17865988110603794_901993804736612452_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=104&_nc_map=urlgen_bucketless&ig_cache_key=Mzg2MDYxMTAxODM1NTM5MDc5ODE3ODY1OTg4MTA0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcxMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=oEMKwhEbtgQQ7kNvwHYbFwm&_nc_oc=Adpftz9AXV829R4c_rncK9PA_XJ4QeOTad19wEzdJMCIhTd7JJ7WU0fMMW1TZDBdLmU&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=7h8z2i-_iRmj2aPx_6NfmQ&_nc_ss=7aa8c&oh=00_AQHAtyrDDpyr8kUaJajA3QgEdEocIztGH1RPw7HwB4YWDA&oe=6A8DD7FC",
        "post_date": ""
    },
    {
        "shortcode": "DWYYWK5javA",
        "post_url": "https://www.instagram.com/reel/DWYYWK5javA",
        "media_type": "reel",
        "caption": "marvarid__restaurant\n\nShunaqa talabalar bormi😂\nView all 45 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.71878-15/656291290_1260488996187824_1052778148750124439_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=Mzg2MTk0Mzc1NzExNzk1OTEwNDE4MDY0OTExMzU5NDEzNTgw.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=AAkCZqBAIg0Q7kNvwGoYlMC&_nc_oc=Adr730pymWJPC6nbEVw0WySdiG7UFED_-j_xTzhspDPMoW2pQ7YI4dxFCHARzK7yyqQ&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=cCs-JbhqmiF4vgWMl-Rytw&_nc_ss=7aa8c&oh=00_AQFeZl2xoxYZsCRkMRvgY2i27Vv24ZaqKNM5utamSV7AhA&oe=6A8DF9A1",
        "post_date": ""
    },
    {
        "shortcode": "DWgUzd1CFet",
        "post_url": "https://www.instagram.com/reel/DWgUzd1CFet",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nTibbiyot — bu kasb emas, inson hayotini asrash san’atidir✨\nView all 30 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.71878-15/658521459_755775964133867_1324091763709097252_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=105&_nc_map=urlgen_bucketless&ig_cache_key=Mzg2NDE3OTk3NzkzNTY3MzI2MTE3ODY2ODg4MTQwNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=UFYWXYdNzCMQ7kNvwG55Ijg&_nc_oc=AdoJbPzQof5HljiUtcgQTft2zDM3LbDyG2QpdCqJXZHq8f1jpLjasWzpCWdCxwEq3gw&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=pYC7CUka4170BVXkBZ6hnw&_nc_ss=7aa8c&oh=00_AQGzxmo1wkD0fKe8zuVGINVDQHrXWEIJQmpos95Mwu0ffw&oe=6A8E0961",
        "post_date": ""
    },
    {
        "shortcode": "DWlYAA_iMdS",
        "post_url": "https://www.instagram.com/reel/DWlYAA_iMdS",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nCo tam😂\nView all 23 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.71878-15/658796355_2022103078385710_8345370645018191441_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=Mzg2NTYwMTQwOTM0OTYzMzg3NDE3ODY3MjE1ODI0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=iKYk6TedvSYQ7kNvwEH2hXM&_nc_oc=AdqnKUaSI6STxTubLhr29QZ9fIdaqi9OjZK7HBVlIJ4dhnWs0ceaa84pywqf0OAJgHQ&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=PnIBa1koMmO-PhJUGwu5DA&_nc_ss=7aa8c&oh=00_AQHkfidbH_lmcji2ynTeife1nI5zAeiv64LgNiBnvn1esA&oe=6A8DE4ED",
        "post_date": ""
    },
    {
        "shortcode": "DWtGYcHCIDC",
        "post_url": "https://www.instagram.com/reel/DWtGYcHCIDC",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShunaqa talabalarga sekin yuborib qo’yamiz😁\n\n#top #sh_t_t #rek #trendy\nView all 33 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.71878-15/658408063_1481238473509223_7018787942380967889_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=Mzg2Nzc3NTcyMjcxMDQwMTIxODE3ODY3Njk5MzIyNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=idce1LTHgYoQ7kNvwHRoqeg&_nc_oc=Adoox4jcztg2mvmtus_D7gJrp7Q3Rcv0aLTpk46B5yiXes_HNByOk0BQPBjoXHAdoSo&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=HSn2qdLb1N0I7NyM-Yq9ZQ&_nc_ss=7aa8c&oh=00_AQFllCzI4V_NVnyFLXlZl4EcXlQcfPYXX6jiZBKQsSUfEQ&oe=6A8DEB98",
        "post_date": ""
    },
    {
        "shortcode": "DW4B346iBAj",
        "post_url": "https://www.instagram.com/reel/DW4B346iBAj",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nUzur uzur adashib ketdi😂\n\n#top #sh_t_t #rek #trendy #shtt\nView all 37 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.71878-15/669732411_4550562075176908_117289590717516896_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=105&_nc_map=urlgen_bucketless&ig_cache_key=Mzg3MDg1MjExODQ1NDIxMDU5NTE3ODY4Mzk5MjQ5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=GwJQ1T4THPEQ7kNvwFSNFyx&_nc_oc=Adoat5fx1mJLt61Km2as4eMC0e0zSbcBVekRYC5bZmzrKRTqRYx2p5Wya7pLTqF0PnI&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=u9oZR6ieVG2UYxBXBXkfxg&_nc_ss=7aa8c&oh=00_AQEFiCQnS3LjjBJ5ji0vCeT2BseYszdWAqUTI671XY2iKQ&oe=6A8DF242",
        "post_date": ""
    },
    {
        "shortcode": "DXW5UTACBgc",
        "post_url": "https://www.instagram.com/reel/DXW5UTACBgc",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBizning talabalar trendan qolmaydi😅👩‍⚕️💉\n\n#medical #mood #trend #student #doctor\nView all 32 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/660718656_17871788460603794_3911305089397702996_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=Mzg3OTU0MDIxMjQ2ODU1Mzc1NjE3ODcxNzg4NDU3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=2O0CQ1gWtdwQ7kNvwHijLZI&_nc_oc=AdqePnsFYbocefaAG8m00bU6j3lQnHmRj-LTa-Xft5T0vRV6Js7JcGUZ7_8EfBr35eI&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=w8tQtmscRYVhWB_VjbtHrA&_nc_ss=7aa8c&oh=00_AQEO_ViughSwgUQhG2xfgny89CKLzJjr3mKzdnUSMtIeMQ&oe=6A8DFBF9",
        "post_date": ""
    },
    {
        "shortcode": "DXcCaxSiKsd",
        "post_url": "https://www.instagram.com/reel/DXcCaxSiKsd",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nTalabalardan nima uchun oʻqiyotganini soʻradik📚\n\n#study #university #medecine #doctor\nView all 38 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.71878-15/671221156_981771737710390_8174818558836676382_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=Mzg4MDk4NzYxNDYxMDIzODIzNw%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=yUilviBEuPEQ7kNvwHXWBI_&_nc_oc=Adq4hhVrCkLGDgmaya5kkmBnN70EdE8yvrWq_tPR7HFBGUqkcJr-NXuNLXR3nYbr41c&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=630G0yQdljySRjpQw-Lwaw&_nc_ss=7aa8c&oh=00_AQGXWw5PEAAtHmoOlEz_ztGBkIHASw89aU8qGgaWJTbKnA&oe=6A8E0213",
        "post_date": ""
    },
    {
        "shortcode": "DXrm0raiBPy",
        "post_url": "https://www.instagram.com/reel/DXrm0raiBPy",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nSiz bir kunga ustoz boʻlib qolganingizda nima qilgan boʻlardingiz?😅\n\n#medicina #sh_t_t #doctor #study #university\nView all 33 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/682212785_17871788412603794_8574979604826687570_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=Mzg4NTM2OTg0OTMzMzQyMTA0MjE3ODcxNzg4NDA5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEwNzguc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=XLxoSKkKtuAQ7kNvwGzpY0G&_nc_oc=AdoLuQ5T5WwnmumyUwVS-1Z7poonWmhaZpEv4Pmy7EnlfydZ7IvE7cFp-L2mZZrSnCI&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=zJxKZtSv0TIUY3dc7AZvAQ&_nc_ss=7aa8c&oh=00_AQFyhrZMD2pA3ST9qa_721zaudpNdOlegaqrz3T0eEQPGQ&oe=6A8DE004",
        "post_date": ""
    },
    {
        "shortcode": "DXzVIPBIVdy",
        "post_url": "https://www.instagram.com/reel/DXzVIPBIVdy",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShahrisabz tibbiyot texnikumi talabalari @marvarid__restaurant da!⛰️🪁\n\n#picnic #student #team #mountains #sh_t_t\nView all 135 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.71878-15/682740485_2505645349947161_366271079829712014_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=101&_nc_map=urlgen_bucketless&ig_cache_key=Mzg4NzU0MzgyODIwODUwNjczODk2NDIyNzgzNjM0MDk0MQ%3D%3D.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjY0MC5zZHIudmlkZW9fbmZyYW1lX2NvdmVyX2ZyYW1lLkMzIn0%3D&_nc_ohc=eqGSVkx9iWMQ7kNvwF8_hJ0&_nc_oc=Adp3V-hGJgTFWLmN_37OYfwySVwWvKx1bCqetnEdFXIo3lfQgjhVFhffq8_YLd668jk&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=I5MMmWWoAX798RE43zh21A&_nc_ss=7aa8c&oh=00_AQEMI-qi2jRe4kG8sBBqho4BzsncKJybeUd_q6ZEL3Yelg&oe=6A8DE2B0",
        "post_date": ""
    },
    {
        "shortcode": "DX3Qge2IbY7",
        "post_url": "https://www.instagram.com/reel/DX3Qge2IbY7",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎉 Shahrisabz Tibbiyot Texnikumida ajoyib Osh festivali!\nTalabalarimiz nafaqat bilimda, balki an’anada ham yetakchi 🍚🔥\n\n📚 Bizda mavjud yo‘nalishlar:\n— Hamshiralik ishi (2 yil)\n— Hamshiralik ishi (3 yil)\n— Feldsherlik ishi\n— Farmatsiya\n\n👩‍⚕️ Kelajak kasbingni biz bilan boshlagin!\n📞 Batafsil: 97 587 46 57\nView all 67 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/718935547_17878352388603794_3218555404067166555_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=101&_nc_map=urlgen_bucketless&ig_cache_key=Mzg4ODY0OTQwNDE0NTU3OTU3OTE3ODc4MzUyMzgyNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=sDX_R4oPE3YQ7kNvwHlN8n-&_nc_oc=AdounB2Z48ihvL2-a_Va494C5lo2Q7Y70RNTfQhZ_TZg3eM-fRwjOZgYHtPENlhIFCc&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=6NzCEAAklDqQS1Kvyul1oQ&_nc_ss=7aa8c&oh=00_AQE9QaN5WI1zFWCw3bsTfAzIge7xewmAJxD5jwyaxoZ5MA&oe=6A8DD7FE",
        "post_date": ""
    },
    {
        "shortcode": "DYANijgofN1",
        "post_url": "https://www.instagram.com/reel/DYANijgofN1",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🧠 Siz bu faktlarni bilarmidingiz?\n\n🎥 Ko‘ring va hayratda qoling 🤯\n💬 Sizga qaysi biri yoqdi?\n\n#tibbiyot #medicina #doctor #facts #video\nView all 24 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/717930116_17878351779603794_6740780159194765318_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5MTE2OTYyNzI0MzQxMDI5MzE3ODc4MzUxNzc2NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=icybepU7SckQ7kNvwEwrvA1&_nc_oc=Adqmuqi7Vd8RHcYpMI0TSkYK6nu5bT5bJQg4thtJzRmK7Ljp0oNiNxKcbvYDwpLZm8s&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=I9-pVYFceRAaNQDyI90cdQ&_nc_ss=7aa8c&oh=00_AQFpJZ9H7P_J4BM4XjV9zkh4Hs4bW4cfGKoiesC9SiBnVw&oe=6A8DD5FD",
        "post_date": ""
    },
    {
        "shortcode": "DYCqG4_oMnt",
        "post_url": "https://www.instagram.com/reel/DYCqG4_oMnt",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🧑‍🍳Texnikumimizda “Osh festivali”ning 2-bosqichi ham yuqori kayfiyat va milliy an’analar ruhida bo‘lib o‘tdi!\nVideoni tomosha qiling va fikrlaringizni izohlarda yozib qoldiring😉\n\n#palov #festival #celebration #debat #sh_t_t\nView all 66 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/718174620_17878352841603794_8291536620083589526_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5MTg1ODIxOTQ2ODkwMDg0NTE3ODc4MzUyODM4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=cGwux1E8Fy4Q7kNvwEAshlm&_nc_oc=Adpu84ymj8iwN8IVswSUalGTVe7GrXJbtRC9THHXj-Y4sfN8QMA2eOR-T0scaFh20_8&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=LxnJGSPOiMhrsT6fCki2rg&_nc_ss=7aa8c&oh=00_AQG14KJbSdP6wm4ShXMD7mVyU3cpDL4xy556KnmdDgzpWQ&oe=6A8E02C7",
        "post_date": ""
    },
    {
        "shortcode": "DYETpQMIIbU",
        "post_url": "https://www.instagram.com/reel/DYETpQMIIbU",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎉 Talabalik onlariga yana bir chiroyli xotira!\n🎥Marvarid Restoran hamkorligidagi maroqli dam olishdan lavhalar\n\n#picnic #sh_t_t #students #restaurant #mountians\nView all 43 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/718111912_17878352814603794_7946516531210798079_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=107&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5MjMyMjM3NTcyMDUzNTc2NDE3ODc4MzUyODExNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=wKbz9OE26-gQ7kNvwEfQ3Lr&_nc_oc=AdowqnCXlPBX7CCby5rZ6WG3ezReBCmwn0ZPmQNzPlmzhDnjGTHHYC2VyXQa74gAnFc&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=7vo4XynOg1o6PKpPe2YBew&_nc_ss=7aa8c&oh=00_AQHMEz5IBseHemNOXVMgwqen5zj3mvHZOF26tIhN1dBM9Q&oe=6A8DE108",
        "post_date": ""
    },
    {
        "shortcode": "DYKkWqWI7Zv",
        "post_url": "https://www.instagram.com/reel/DYKkWqWI7Zv",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🧑‍🍳 ,,Osh festivali’’ doirasida boʻlib oʻtgan musiqaviy chiqishlardan lavhalar!\nFestivalning eng zo‘r momentlari shu videoda🔥\n\n#festival #sh_t_t #celebrites #show #music\nView all 38 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/718111683_17878352793603794_1114744034797134762_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5NDA4NDcxNDc4NjY5ODg2MzE3ODc4MzUyNzg3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=VFlyU02NVigQ7kNvwGpZdHj&_nc_oc=Adpv4XSkMqGEi4BSJkr37IeSZ_3F3IzFUJKSmTHb9GCGnIH56UT1ghxdlVgeKxq6XCU&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=_oKvQrlMi0lpbpNx75C5RQ&_nc_ss=7aa8c&oh=00_AQGtRR_yK2svnBOqLzqQTEL_QsqRxjBNAt_MDF_Oc2DQiA&oe=6A8E021C",
        "post_date": ""
    },
    {
        "shortcode": "DYPixRjo3pN",
        "post_url": "https://www.instagram.com/reel/DYPixRjo3pN",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nOsh festivalining 2-bosqichidagi musiqaviy chiqishlar kayfiyatni yanada yuqori darajaga olib chiqdi!🎶🔥\n✨Milliy ruh, zamonaviy vibe va unutilmas atmosfera — barchasi bir videoda🤩\n\n#traditional #show #fest #festival #dance\nView all 45 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/718378415_17878353540603794_1086226798043918435_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5NTQ4NTEyMjM4NjAzMzIyOTE3ODc4MzUzNTM3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=P6Q43Z529yYQ7kNvwGf7Xvl&_nc_oc=AdqKMW-BQul4qvDQzINs6PbnfYW_Rc7YI8WhpmNOUcpPK2Ce-2Ev75LmhbuPTYI0ESk&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=_aYGyOEMqy_KecibwKhkGA&_nc_ss=7aa8c&oh=00_AQHN3qbyzoBO61HlTvw0lCTpsFmIIwxV9mlDtQAussYQjw&oe=6A8DF8E3",
        "post_date": ""
    },
    {
        "shortcode": "DYR0e6aov9W",
        "post_url": "https://www.instagram.com/reel/DYR0e6aov9W",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nHayotda eng qimmat narsa — o‘z ustingizda ishlash!📚\nSiz uchun vaqtinchalik hashamatmi yoki kelajakni quradigan ta’limmi? 🎓\n\n#education #video #sh_t_t #trendy #doctor\nView all 61 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/718264668_17878351761603794_7774283313857822610_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5NjEyNTk3NTM3ODk4NDc5MDE3ODc4MzUxNzU1NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=mo4hJ06J2E0Q7kNvwG70nni&_nc_oc=AdrfExUEqTDKE-hZG7BJ5VSZXRxwTDbQwiRvH4XGcP6OGzX3PPHXp5YW8Q1ObH0KIVM&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=Dn11tizkulP40WAyXQ10_A&_nc_ss=7aa8c&oh=00_AQG7Kw1vbjt9lTeYlv__bUxsB_70-8T7lw6r62-67YZsyg&oe=6A8DD8FB",
        "post_date": ""
    },
    {
        "shortcode": "DYTx55nInwT",
        "post_url": "https://www.instagram.com/reel/DYTx55nInwT",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nTalabalarimizning navbatdagi maroqli dam olish kuni — Marvarid Restoran da unutilmas lahzalar ✨\n\n#picnic #day #student #mountain #sh_t_t\nView all 17 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/717273752_17878351737603794_1831646140296794504_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=105&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5NjY3NzU4NTc1NDY4NDQzNTE3ODc4MzUxNzMxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=y5E70XlKmncQ7kNvwEWS3x1&_nc_oc=Adrf3vAasNK3FkHx5J5CzN--i3phbF4aRe-Bxj6h2Gr-atbDfdCsKYC5hn2YyBtEGsA&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=IBHnOcqqYoGwaKZKJFeFJQ&_nc_ss=7aa8c&oh=00_AQGZZ8wpRs9VkzvDON8NDf2KMG4Wp7EkH7e6ExEDRC-4Aw&oe=6A8DD7E0",
        "post_date": ""
    },
    {
        "shortcode": "DYXfbi-IFue",
        "post_url": "https://www.instagram.com/reel/DYXfbi-IFue",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🍚,,Osh festivali’’ning 3-bosqichi yuqori kayfiyat va samimiy muhitda bo‘lib o‘tdi!\n🇺🇿Milliy qadriyatlarimizni aks ettirgan ushbu festival yana bir bor barchani bir dasturxon atrofida jamladi🔥\n\n#festival #traditonal #palov #cooking #show\nView all 30 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/718190175_17878351506603794_3849661819796039514_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5NzcyMjIzNDkyOTY5OTc0MjE3ODc4MzUxNTAzNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=t2PLD-wd1lIQ7kNvwFNS1lQ&_nc_oc=AdpMPXK75F0d_6eTxXdFsm5d1PZJLsuEu2MqQGGaL3E3JMKYf-grnlLIOZz9S6jBP4U&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=e4SFLN2skDdNqz7Ul869Jw&_nc_ss=7aa8c&oh=00_AQE5ggdGdrHrv8fMIhZP65cLZfyta4w5p6XA27wkQ0RbAQ&oe=6A8DD87B",
        "post_date": ""
    },
    {
        "shortcode": "DYchonJI9Dc",
        "post_url": "https://www.instagram.com/reel/DYchonJI9Dc",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nDarslarga kelmay sessiya vaqti koʻrinish bergan talaba😂\nVideoni talabalarga yuborib qoʻyamiz✈️😉\n\n#sh_t_t #student #medicina #doctor\nView all 34 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/718150663_17878350921603794_1403448720840394549_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=Mzg5OTEzOTMwMzczOTIxNjA5MjE3ODc4MzUwOTE4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=P8sOSKBPmnQQ7kNvwHuM0GD&_nc_oc=Adq7zWm-2Z6v8jODEo8ChvjfmHSIxGwRZOhiorPDUqiACKpMxfuQhalNQ3quP-uHCaQ&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=Weuybg9hQ2YvxErVY--6ng&_nc_ss=7aa8c&oh=00_AQFh6Cn1MhkmZ_oqDDbfuwqi-5KLR3uEIBMi33eB5-qMWg&oe=6A8DE626",
        "post_date": ""
    },
    {
        "shortcode": "DYmhGqho5af",
        "post_url": "https://www.instagram.com/reel/DYmhGqho5af",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nBizdan biroz kayfiyat😅\n\n#trendy #kontent #medicina #doctor #student\nView all 21 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/718238077_17878351020603794_1844750789845904180_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=102&_nc_map=urlgen_bucketless&ig_cache_key=MzkwMTk1MTcyMDY3NjM2NTk4MzE3ODc4MzUxMDE3NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=cmYfstMnPMEQ7kNvwG8BHg8&_nc_oc=AdpcSvgy7kRKRzmuNQp-U2Q4HFtJS80XML0Qe4wtWrYLLisweweaTfd3h4BCKCMtw1M&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=mYD84SM5lVhObmO51efYPg&_nc_ss=7aa8c&oh=00_AQGbM6jW6T_Sh48SHJWs62sEntvAjCVwqfNdtdI5Fsnf5g&oe=6A8DF259",
        "post_date": ""
    },
    {
        "shortcode": "DYpe_FHIfXW",
        "post_url": "https://www.instagram.com/reel/DYpe_FHIfXW",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nKontraktingizni kim toʻlaydi?😅\n\n#medicina #student #sh_t_t #doctor\nView all 174 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/718510755_17878349913603794_5117950856878429501_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=MzkwMjc4NjgyODMwMzk4ODE4MjE3ODc4MzQ5OTEwNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=gY8RSTPuvtsQ7kNvwG_NtZV&_nc_oc=AdqubnB9vsY0sUIrIztaW0s7f-ysOl-5_cq2cOTVKWFdludflhGdkDMCJV8u2ZYgMmQ&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=jrxWuIghrdZLvEgsyF7KJA&_nc_ss=7aa8c&oh=00_AQFBH0jhUjgMikGV5ss0siXZrXhpOZs1KwoP3KzgHbkDtg&oe=6A8DE3E0",
        "post_date": ""
    },
    {
        "shortcode": "DZFvYRzoKfF",
        "post_url": "https://www.instagram.com/reel/DZFvYRzoKfF",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n✨ Shahrisabz shahar,tibbiyot texnikumida tashkil etilgan Osh festivalining final bosqichi yuqori kayfiyat va milliy an’analar ruhida bo‘lib o‘tdi!🎉\n\n🍽️ Milliy taomimizga ehtirom, an’analarimizga hurmat va yoshlarning iste’dodi mujassam bo‘lgan ajoyib tadbirdan lavhalar🎥\n\n#national #festival #palov #final\nView all 29 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/717637719_17878347585603794_6783841195261335774_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=MzkxMDc0MDIyODAxNDM4NTA5MzE3ODc4MzQ3NTgyNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjk0MS5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=GVG9j4vKbcMQ7kNvwELKDct&_nc_oc=AdpXNaeYBv8JH4ywSoXrLzXSPkR5NXMCziAXvA--ESvfwpSUiHVp5YYR9ECxkGiOvrc&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=FFlZldzjfNQM19ixxSdTlA&_nc_ss=7aa8c&oh=00_AQGJaAuChMujCgdyWWc_5hSpNmA6tPSVrFmAZaf20vVPlA&oe=6A8DDE57",
        "post_date": ""
    },
    {
        "shortcode": "DZK3Tgloqle",
        "post_url": "https://www.instagram.com/reel/DZK3Tgloqle",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n📚Ta’lim jarayonida bilim olish bilan bir qatorda,talabalik hayotining turli qiziqarli va unutilmas lahzalari ham uchrab turadi\n🎓 Biz bilan talabalik hayotini kuzatishda davom eting!\n\n#student #life #medicina #shtt #doctor\nView all 15 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/717417521_17878354002603794_5108241383307455963_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=MzkxMjE4MjQ1OTU0NDAyMTM0MjE3ODc4MzUzOTk5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=SNQiWDj9uLMQ7kNvwEblUZ9&_nc_oc=Adq9_mgZfF9ua51iPJgFZ5U9s0rRAefW4otV1AsktjKddgCynwT2A3Qd-MVHwCmSFHQ&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=4KcZ9VYvqvAdGerZEwOmCA&_nc_ss=7aa8c&oh=00_AQFov9pOkk-ixYTCL37TPAnKYWQOKxo_ZaGAthDf-aQHwA&oe=6A8DE12F",
        "post_date": ""
    },
    {
        "shortcode": "DZQIF8boF6m",
        "post_url": "https://www.instagram.com/reel/DZQIF8boF6m",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🇺🇿 Bugun millionlab yuraklar bir maqsad uchun uradi — Vatan sharafi uchun!\n\n🧬Shahrisabz tibbiyot texnikumi jamoasi nomidan O‘zbekiston milliy terma jamoasiga omad tilaymiz. Maydonda jasorat, ishonch va g‘alaba ruhi hamrohingiz bo‘lsin!\n\n#football #uzbekistan #team #play\nView all 68 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/718150670_17878353507603794_6926347002369560820_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=110&_nc_map=urlgen_bucketless&ig_cache_key=MzkxMzY2MzY2OTA0MjQzNzc5ODE3ODc4MzUzNTAxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=zHfXuETgj7sQ7kNvwFmn4cT&_nc_oc=AdoJMFzg85Q63n-GNUiZk4jkBlITrkTSPiFzn9yDcakoFrfUV2Bce4-zosxledGDJlc&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=4D91ckY7ee_u9zhXs2CdPA&_nc_ss=7aa8c&oh=00_AQH27iVQt4jhqQ0lZfc6jsNisnqctSiM4cLQ1GFN_IUUKg&oe=6A8DF30A",
        "post_date": ""
    },
    {
        "shortcode": "DZXzq1xobjf",
        "post_url": "https://www.instagram.com/reel/DZXzq1xobjf",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓 Yangi bosqich sari ilk qadam!\n\n💉Shahrisabz tibbiyot texnikumida bitiruvchi talabalarimizga diplomlar tantanali ravishda topshirildi!Yillar davomida olingan bilim, mehnat va intilishlar o‘z samarasini berdi. Endilikda ular sog‘liqni saqlash tizimida xalqimiz salomatligi yo‘lida xizmat qiladigan malakali mutaxassislar sifatida yangi qadam tashlashadi!\n\n⚕️Shahrisabz tibbiyot texnikumi — kelajak tibbiyot xodimlarini tarbiyalaydigan bilim maskani\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#medicina #student #doctor #sh_t_t\nView all 35 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/718510287_17878748637603794_7874820937097469571_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=MzkxNTgyNTY0NTM1MzAyMzcxMTE3ODc4NzQ4NjM0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=5IICn0QVwN4Q7kNvwGXvJaD&_nc_oc=Ado10jBqr2dNZ9uMNG8Wub8JChgNmWLXdQK0cgjTBXh4XuHYdNxrh4BXtFT7MiofeUw&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=N4Y3B-RH55PPhXhacQJACA&_nc_ss=7aa8c&oh=00_AQHCDo9AFMI8NgRU-3irHDbc0wqGNw1Q5SLdSgaLKP5oUQ&oe=6A8DED11",
        "post_date": ""
    },
    {
        "shortcode": "DZiF3OnI20A",
        "post_url": "https://www.instagram.com/reel/DZiF3OnI20A",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓 Kelajagingizni tibbiyot bilan bog‘lashga tayyormisiz?\n📢 Shahrisabz tibbiyot texnikumida qabul jarayonlari boshlandi!\n\n✅ Sifatli ta’lim\n✅ Amaliy mashg‘ulotlar\n✅ Zamonaviy o‘quv muhiti\n✅ Kelajak kasbiga ishonchli yo‘l!\n\nBularning barchasi Shahrisabz tibbiyot texnikumida!😊\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#medicina #qabul #doctor #medical\nView all 221 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/724225856_17879635134603794_6481220129063128652_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ig_cache_key=MzkxODcyMDQxMTI1ODU0NzQ1NjE3ODc5NjM1MTMxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=pByIOoWD1HYQ7kNvwGIybQu&_nc_oc=AdrLCxMkJ9y7V9-YEd0mpaeNP08AQPjZedV8g8WzO64TPjYu0zKcwjaPm3mNFsQUmwQ&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=4_2RFlWtNyQrhsNKn3xCVw&_nc_ss=7aa8c&oh=00_AQGUv5-XzzX_3DfIhH8P0cj-dWgjxUTYXKutm356kq33Kw&oe=6A8DD7C7",
        "post_date": ""
    },
    {
        "shortcode": "DZmsMiGISzz",
        "post_url": "https://www.instagram.com/reel/DZmsMiGISzz",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🏥 Shahrisabz tibbiyot texnikumida 2026–2027 o‘quv yili uchun qabul boshlandi!\n⚕️Tibbiyot sohasida zamonaviy bilim va amaliy ko‘nikmalarga ega bo‘lishni istasangiz, sizni texnikumimiz safiga chorlaymiz. Tajribali ustozlar, qulay ta’lim muhiti va amaliy mashg‘ulotlar sizning muvaffaqiyatli kelajagingiz uchun mustahkam poydevor bo‘ladi!\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#medicine #medical #trend #sh_t_t #student\nView all 9 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/719891395_17879635437603794_1214038757250353905_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=MzkyMDAxNDkwMDk2Mjg2NDM3MTE3ODc5NjM1NDM0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=ebZnveypedYQ7kNvwHbkJSN&_nc_oc=AdpDMoJi4mXbq0XkQWLkOREKu8abIEvXRFzdLgbEj3RkQ6lVUoxJzAUia7uI1-gr8TQ&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=Q6vk-xz0JKImDw57mgEwnA&_nc_ss=7aa8c&oh=00_AQF0n1gjxp5jxn3e-KAAj9h-8le1rBFN4oNNTpuCIDEGCQ&oe=6A8DD7DC",
        "post_date": ""
    },
    {
        "shortcode": "DZ21e-tokIM",
        "post_url": "https://www.instagram.com/reel/DZ21e-tokIM",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\nShahrisabz tibbiyot texnikumi talabalari nazariy bilimlarini amaliyotda mustahkamlab, shifoxonalarda o‘z kasbiy ko‘nikmalarini oshirmoqda!🩺\n⚕️Shahrisabz tibbiyot texnikumi — bilim, tajriba va kelajak sari ishonchli qadam!\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#medicina #student #shtt #medical #practicas\nView all 37 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/726660011_17880687141603794_2297877475627815769_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=105&_nc_map=urlgen_bucketless&ig_cache_key=MzkyNDU1OTM1MDY4Njk1ODA5MjE3ODgwNjg3MTM4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEzMjAuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=VrN28HF4A9sQ7kNvwFd19Wg&_nc_oc=AdohBXbDtnAMsUcenIyZKKBfKF0RIMkWpg_DHvq3VDVqZHlVoYOn_EyQPG613znTyd4&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=nOo0W6m0RfXOH4AarCC5kQ&_nc_ss=7aa8c&oh=00_AQEqnR89RHsguLeU158YXTNpeoULHUo-NEbRFv9ArLKJ-w&oe=6A8E0141",
        "post_date": ""
    },
    {
        "shortcode": "DZ5VIGdo5XW",
        "post_url": "https://www.instagram.com/reel/DZ5VIGdo5XW",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n⚕️Shahrisabz tibbiyot texnikumida talabalar uchun navbatdagi imtihon jarayonlari bo‘lib o‘tdi!\n\nBu sinovlar orqali talabalar o‘z bilim, tayyorgarlik va mas’uliyatini yana bir bor namoyon etishdi!📚🩺\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\nView all 33 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/728951196_17880848865603794_2867727271234174749_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=101&_nc_map=urlgen_bucketless&ig_cache_key=MzkyNTI2MTQ2NTkwMjM1NTkyNjE3ODgwODQ4ODU5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEyMTUuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=ovPoi5cR0NcQ7kNvwFZGDq-&_nc_oc=Ado9b7yNLLDgK9xb_fL6TXMlHrbdOJQT-TvY6gl_3kZlPG2bJEGHH2OKZvodL0KDvr0&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=uYtkVO05oAuc8owntDRqMw&_nc_ss=7aa8c&oh=00_AQEmbtfc_RXFlVy_sesVeElD08YTnC9nTFTSKmdiu2COWg&oe=6A8E0A2E",
        "post_date": ""
    },
    {
        "shortcode": "DaGbAwuIwRP",
        "post_url": "https://www.instagram.com/reel/DaGbAwuIwRP",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓Texnikum bitiruvchilari uchun yana bir katta imkoniyat!\n\n📢 Yangi qarorga muvofiq, texnikum bitiruvchilari bakalavriat ta’lim yo’nalishlarida 2-bosqichdan o’qishni davom ettirish imkoniyatiga ega bo’ladilar!\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#medical #texnikum #education #information #news\nView all 10 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/730348028_17881776780603794_6299544802287217079_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=107&_nc_map=urlgen_bucketless&ig_cache_key=MzkyODk0NjUyNDQ5Njc5MDYwNzE3ODgxNzc2Nzc0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=HpYnuL6GN4oQ7kNvwHbcVs1&_nc_oc=AdqFUC1-PcZqJ1oACJbOYJR7AH9cb1Ajer6NaoaZS_l0aAdJhW8x5YMYbYdfmHBbz0c&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=4U9HPpjO7_4BL2R7zZKSvw&_nc_ss=7aa8c&oh=00_AQGQck3c8oRas3fdl4RyanYJOfdtUK9JgH8BeTs-Lo_iIQ&oe=6A8DEFD1",
        "post_date": ""
    },
    {
        "shortcode": "DaSUrQEIfRp",
        "post_url": "https://www.instagram.com/reel/DaSUrQEIfRp",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🌍 Chet davlatlarda malakali hamshiralar yuqori maosh evaziga faoliyat yuritmoqda.\n\nBugun o‘zingizga beradigan eng muhim savol:\nSiz ham shunday imkoniyatga tayyormisiz?\n\n📚 To‘g‘ri ta’lim va mustahkam bilim — kelajakdagi muvaffaqiyatning birinchi qadami.\nView all 21 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/730304065_17882572359603794_7229176790201590731_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=111&_nc_map=urlgen_bucketless&ig_cache_key=MzkzMjI5NjM1Nzc2NDc4OTM1MzE3ODgyNTcyMzU2NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEzMjAuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=Va4eRObtVpcQ7kNvwHwK6GV&_nc_oc=AdpE5SiJOaep7Rwfew_pNnjoEmm9DvORp77Uly2wdR3jCTgQet4Nf8y8fnvdHkaBAvY&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=2mQiBUvFOeNUQTdt0mXAzA&_nc_ss=7aa8c&oh=00_AQHQnbb6gLTC_uVqKwtz9IQjHwpEr1i5GSncAL8uX8-8aA&oe=6A8E012B",
        "post_date": ""
    },
    {
        "shortcode": "DaUmCM_Ihxp",
        "post_url": "https://www.instagram.com/reel/DaUmCM_Ihxp",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓Davlat namunasidagi diplom - kelajagingiz uchun mustahkam poydevor!\n\nBizning texnikumni tamomlaganingizdan so'ng davlat namunasidagi diplomga ega boʻlasiz. Sifatli ta'lim, amaliy bilim va ishonchli kelajak sari ilk qadamingizni bugun qo'ying!\n\n☎️Murojat uchun:\n+998 88-260-20-73\n+998 97-266-20-73\n\n#medicina #student #sh_t_t #medical\nView all 5 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/731187434_17882720607603794_4706536199031980710_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=105&_nc_map=urlgen_bucketless&ig_cache_key=MzkzMjkzNTY1MTc1MTc2MzA0OTE3ODgyNzIwNjAxNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=9IlDuO8kcqIQ7kNvwEFDzkf&_nc_oc=Adq3aDLsekQLrdVOmi1sxIPsZKOKWVDG54A_eQeqaDrxvdthvazq-lkW0DU8nteOPNU&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=W-G1O6UVxWW6MEMhjtdSzA&_nc_ss=7aa8c&oh=00_AQFD1OeUmF-wNfYU7QWFJZMahiCHWeYIh_sZHjUz0Lgp8Q&oe=6A8DF568",
        "post_date": ""
    },
    {
        "shortcode": "DaVul-HIUpb",
        "post_url": "https://www.instagram.com/reel/DaVul-HIUpb",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🩺Kelajagingizni tibbiyot sohasi bilan bog‘lashni istaysizmi?\n\n⚕️Shahrisabz Tibbiyot Texnikumida 2026/2027-o‘quv yili uchun qabul ochiq! Zamonaviy ta’lim, malakali ustozlar va amaliyotga yo‘naltirilgan darslar sizni kutmoqda!\n\n📚 Bugunoq hujjatlaringizni topshiring va orzuyingizdagi kasb sari ilk qadamni tashlang!\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#medicina #trend #student #doctor\nView all 7 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/734622994_17882803671603794_2025168563615860052_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ig_cache_key=MzkzMzI1NDc2OTAyOTc2MTYyNzE3ODgyODAzNjY4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEzMjAuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=C5FvvIpNWfcQ7kNvwF95Kwt&_nc_oc=AdojEbRfdJRFbub-vuxoZSsxNLpWIZ1GUJmBLCrRKm2EzDcBDqWd8mM-Qk68mzEk2Q8&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=mtusWT-8q0WJkZDJy83k2w&_nc_ss=7aa8c&oh=00_AQF_ReU7D1FNhfUB7xQH3XVedyXbKD3UvAQcjzZb_hUr5A&oe=6A8DF841",
        "post_date": ""
    },
    {
        "shortcode": "Daat-i5o3Vc",
        "post_url": "https://www.instagram.com/reel/Daat-i5o3Vc",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓Kelajagingizni ishonchli ta’lim bilan boshlang!\n\nShahrisabz tibbiyot texnikumida qabul davom etmoqda!\n\n✅ Zamonaviy ta’lim\n✅ Malakali ustozlar\n✅ Amaliyotga yo’naltirilgan darslar\n✅ Kelajak kasbingiz sari mustahkam qadam\n\nBugunoq hujjatlaringizni topshiring va tibbiyot sohasidagi orzularingizni ro’yobga chiqaring!\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#student #medicina #doctor #medical #sh_t_t\nView all comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/735286999_17883157032603794_7698145393653279594_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=101&_nc_map=urlgen_bucketless&ig_cache_key=MzkzNDY1OTQzNDYzNjM0MjYyMDE3ODgzMTU3MDI2NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=PCFZDxa5imIQ7kNvwFep0Ji&_nc_oc=Adp74Pt1-Br6bT6Cg-LyTwgi4-fHKBZqPVdvkNEjuQCeiAQ9uzUfCpjaBTpS0LXEM-I&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=eWjyXxl6XwadGzEdFBtCXg&_nc_ss=7aa8c&oh=00_AQG7ZxSOOS76DriznYaQPgGsC-58fbgLzWB9CiPGH6s6Yg&oe=6A8DD69C",
        "post_date": ""
    },
    {
        "shortcode": "DafkAI3qOnr",
        "post_url": "https://www.instagram.com/reel/DafkAI3qOnr",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n⚕️Shahrisabz tibbiyot texnikumida qabul davom etmoqda!\n\nSifatli ta’lim, malakali ustozlar va amaliyotga yoʻnaltirilgan darslar orqali kelajakdagi kasbingiz sari dadil qadam tashlang!\n\n✨ Nega aynan biz?\n• Zamonaviy ta’lim muhiti\n• Tajribali oʻqituvchilar\n• Amaliy mashgʻulotlarga alohida e’tibor\n• Kelajagingiz uchun mustahkam poydevor\n\nBugun hujjat topshiring va tibbiyot sohasidagi orzularingizni biz bilan amalga oshiring!\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\n\n#doctor #student #medicina #medical\nView all 21 comments",
        "media_url": "https://instagram.fbhk1-4.fna.fbcdn.net/v/t51.82787-15/733676697_17883483765603794_9038112597963596022_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=100&_nc_map=urlgen_bucketless&ig_cache_key=MzkzNjAyMjkzODU0MzI1Mzk5NTE3ODgzNDgzNzU5NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=PwAR66ds8EkQ7kNvwHMrUwg&_nc_oc=Adpb8x2_u4LMgeOdsTjHcExCVFzeckn6De3F1vfWqtsyQ4b_5GYbsfPJoyJMznSJHtQ&_nc_zt=23&_nc_ht=instagram.fbhk1-4.fna&_nc_gid=TElS5hgkb7YazAptO22wsg&_nc_ss=7aa8c&oh=00_AQFgAW4iKU0qlqKFBW_3bPtz7OT2bhsChf5KpfWA1Jdq2A&oe=6A8DFF59",
        "post_date": ""
    },
    {
        "shortcode": "DanRQ0kKsiF",
        "post_url": "https://www.instagram.com/reel/DanRQ0kKsiF",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n⏳ Vaqt o‘tadi, kasblar o‘zgaradi. Ammo tibbiyot sohasi doimo eng barqaror va eng daromadli yo‘nalishlardan biri bo‘lib qoladi.\n\nKelajagingizni ishonchli kasb bilan boshlang. Qabul davom etmoqda!\n\n☎️Murojat uchun:+998 88-260-20-73\n+998 97-266-20-73\nView all 5 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/735776074_17883973863603794_7932890001227399685_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=MzkzODE5MjMyMTkwMjQ2MzEwOTE3ODgzOTczODYwNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=y3BnmBdU9PMQ7kNvwFp3kQq&_nc_oc=AdpsiyMcJInB4KE3z89AhtWsFaekB7j3Xn-bqZ5GBovIvYkVzUADREXvacQrEyszjTw&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=eXepdRCUpAhlu8FfRRMu0Q&_nc_ss=7aa8c&oh=00_AQHAgmwDMvmUxX1y7REpLIdLhQjZWvrA60vB_wIjGuhHDQ&oe=6A8DEE5F",
        "post_date": ""
    },
    {
        "shortcode": "DbsKZ2qICdh",
        "post_url": "https://www.instagram.com/reel/DbsKZ2qICdh",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓 Kelajagingizni bugundan boshlang!\n\n👩‍⚕️ Davlat namunasidagi diplom asosida zamonaviy tibbiy kasbni egallang.\n\n✅ Hamshiralik\n✅ Feldsherlik\n✅ Farmatsiya\n\n📚 Qulay to’lov imkoniyatlari\n👨‍🏫 Tajribali ustozlar\n💼 Bitirgach ish topish imkoniyatini oshiruvchi amaliy ta’lim\n\n📍 Shahrisabz tibbiyot texnikumi\n\n📞 Batafsil ma’lumot va ro’yxatdan o’tish:\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n⏳ Qabul davom etmoqda. Joylar cheklangan — hoziroq murojaat qiling!\nView all 32 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/765059407_17888737608603794_1824720334118703319_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=107&_nc_map=urlgen_bucketless&ig_cache_key=Mzk1NzU4MzkyOTY5MjY2MTYwMTE3ODg4NzM3NjAyNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEzMjAuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=gNh0foWilbEQ7kNvwH2liB9&_nc_oc=Adr3CsndWyMCrl7Fsq7J8n9hVcuN51rdxVYXqQNDRa5JRJi0OrwvoezaaWmRxMUz04s&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=2nAZ8XxfNsPDHA_XqR3pug&_nc_ss=7aa8c&oh=00_AQGHZG_68lRCoToS1vfYIhfy6DUUuAXB8FMHptJJMFgB9Q&oe=6A8DF851",
        "post_date": ""
    },
    {
        "shortcode": "DbyU4H_oLZr",
        "post_url": "https://www.instagram.com/reel/DbyU4H_oLZr",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓 SHAHRISABZ TIBBIYOT TEXNIKUMI\n\n📢 QABUL DAVOM ETMOQDA!\n\nKelajagingizni tibbiyot sohasi bilan bog‘lashni istaysizmi? 🩺\nUnda bizning texnikumimizga hujjat topshirishga shoshiling!\n\n👩🏻‍⚕️Hamshiralik ishi\n\n🩺Davolash ishi\n\n💊Farmatsiya\n\n📞 Murojaat uchun telefon raqamlari:\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n✨ Sifatli ta’lim — yorqin kelajak sari birinchi qadam!\nView all 20 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/763806030_17889193026603794_1270812021053151547_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=103&_nc_map=urlgen_bucketless&ig_cache_key=Mzk1OTMxODg0MDIxNjY5NjQyNzE3ODg5MTkzMDIwNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEzMjAuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=Y-M46mZ6E_AQ7kNvwGuDok6&_nc_oc=Adrz6qN00zaZFskdap7UY-nhluT5vR7uVJk2s50OyHkPTGiLC8EPHHN68yc60Ltn6gQ&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=Q8UYea3GN1_91roQHXrPlg&_nc_ss=7aa8c&oh=00_AQGxgjgxDdYOfJLANAsDxcMcQ8sHc_lUxU6U1TjaanGJpA&oe=6A8E04AE",
        "post_date": ""
    },
    {
        "shortcode": "Db-ssJeIyZh",
        "post_url": "https://www.instagram.com/reel/Db-ssJeIyZh",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🎓 SHAHRISABZ TIBBIYOT TEXNIKUMIDA QABUL DAVOM ETMOQDA! 🩺\n\nKelajakdagi kasbingizni bugundan tanlang! 💙\nSifatli ta’lim, zamonaviy bilim va tibbiyot sohasida mustahkam kelajak sari bir qadam! 👩‍⚕️👨‍⚕️\n\n📞 Murojaat uchun:\n☎️ 77 088 20 73\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n📍 Shahrisabz tibbiyot texnikumi\n✨ Qabul davom etmoqda! Shoshiling, o‘z o‘rningizni band qiling!\nView all 27 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/770235294_17890064757603794_4928756045833025198_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=Mzk2MjgwMTI3MDAwNTM3NjYwOTE3ODkwMDY0NzU0NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjEzMjAuc2RyLnZpZGVvX2RlZmF1bHRfY292ZXJfZnJhbWUuQzMifQ%3D%3D&_nc_ohc=jysSC9tahccQ7kNvwH1N02I&_nc_oc=AdowG-0RfrZ8F19XeqDwhhuluhVesYeb6zYXlaCygQmxZvcgRwKnHu38RoKpGGlrdKU&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=sCvQeB24gZjrqBZLWJm0OA&_nc_ss=7aa8c&oh=00_AQGVcyO6Sr6lvKrBWN7gjOJPNwuK_fCt_niGWHUGIog95Q&oe=6A8DD9C5",
        "post_date": ""
    },
    {
        "shortcode": "DcBekL6Omao",
        "post_url": "https://www.instagram.com/reel/DcBekL6Omao",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n📚 3 OYLIK HAMSHIRALIK KURSI\n\n🩺 Shahrisabz tibbiyot texnikumida 3 oylik hamshiralik kursiga qabul davom etmoqda!\n\n🎓 Zamonaviy bilim va amaliy ko‘nikmalar\n👩‍⚕️ Tajribali mutaxassislardan ta’lim\n📜 Kurs yakunida sertifikat\n\n📞 Murojaat uchun:\n☎️ 77 088 20 73\n☎️ 88 260 20 73\n☎️ 97 266 20 73\n\n📍 Shahrisabz tibbiyot texnikumi\n\nJoylar soni cheklangan! Batafsil ma’lumot uchun bog‘laning.\nView all 36 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/775243993_17890236744603794_3132229336775129250_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=Mzk2MzU4MzU3NTE0NzMwODcxMjE3ODkwMjM2NzM4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=2BxsdU2Kx78Q7kNvwHJ85wx&_nc_oc=AdptnbUJsZuLlWzpKrbS3aUah6A4hf0-can_LUQ_wUoUJ1skZlaNMQXWCKj69h6Kge0&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=cEhYmPb41B3hbu7VuuZzZg&_nc_ss=7aa8c&oh=00_AQH_Xo7gZpquMYIF6B0ll9yWrSrbFaj3cN761PCLzvrgVw&oe=6A8DFD93",
        "post_date": ""
    },
    {
        "shortcode": "DcDX1cOoIoX",
        "post_url": "https://www.instagram.com/reel/DcDX1cOoIoX",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n📚 Shahrisabz tibbiyot texnikumi — kelajagingiz uchun mustahkam qadam! 🩺\n\n🎓 Zamonaviy ta’lim\n👩‍⚕️ Amaliy mashg‘ulotlar\n📚 Sifatli bilim va tajriba\n\n📞 Batafsil ma’lumot uchun:\n+998 77 088 20 73\n+998 97 266 20 73\n+998 88 260 20 73\n\n📍 Shahrisabz tibbiyot texnikumi\n#Shahrisabz #TibbiyotTexnikumi #Qabul2026 #Tibbiyot #Talaba\nView all 20 comments",
        "media_url": "https://instagram.fbhk1-1.fna.fbcdn.net/v/t51.82787-15/772853424_17890427796603794_3810014169498174263_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=Mzk2NDExNjkyNDUyODM2NDA1NTE3ODkwNDI3NzkwNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=F8MP5INj0IUQ7kNvwEda1UZ&_nc_oc=Adq0HdayRy19eJAI3p4oEs6-dxkuE88TlkVmE3j-c1RWoQX4mZ_GqmU3dZZC0U0EsPI&_nc_zt=23&_nc_ht=instagram.fbhk1-1.fna&_nc_gid=DfYEwmmccqttwy14Adf8Aw&_nc_ss=7aa8c&oh=00_AQHurf0rKMJcEnQH27zGPTef0G9iEw7S_SLjz1TxCZA_bg&oe=6A8DE7FF",
        "post_date": ""
    },
    {
        "shortcode": "DcIsWQ5IT8b",
        "post_url": "https://www.instagram.com/reel/DcIsWQ5IT8b",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n📚 Shahrisabz tibbiyot texnikumi — kelajagingiz uchun mustahkam qadam! 🩺\n\n🎓 Zamonaviy ta’lim\n👩‍⚕️ Amaliy mashg‘ulotlar\n📚 Sifatli bilim va tajriba\n\n📞 Batafsil ma’lumot uchun:\n+998 77 088 20 73\n+998 88 260 20 73\n+998 97 266 20 73\n\n📍 Shahrisabz tibbiyot texnikumi\n#Shahrisabz #TibbiyotTexnikumi #Qabul2026 #Tibbiyot #Talaba\nView all 5 comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/774197436_17890832214603794_6962989922684394933_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=109&_nc_map=urlgen_bucketless&ig_cache_key=Mzk2NTYxNDUxNTkxMzA0NzgzNTE3ODkwODMyMjA4NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjQ4MC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=sjws28q2o2EQ7kNvwECHlcY&_nc_oc=AdqZxXPXYTBOwNQpgIKBOb4iT099UmyDtsaK06ZHRuHfaTDluG7JMY_9cYjwkCAGUPk&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=1MRNlyVQTDCpaKss1mpCOA&_nc_ss=7aa8c&oh=00_AQFHTntPHgU54_UptssgBfa5mA2L14IOwBHqEwJDKUhKrg&oe=6A8DFCE4",
        "post_date": ""
    },
    {
        "shortcode": "DcLj3zwqODC",
        "post_url": "https://www.instagram.com/reel/DcLj3zwqODC",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n📚 Tibbiyotda o‘qishni xohlayapsizmi? 🩺\nUnda bu video aynan siz uchun! ❤️\n\n📍 Shahrisabz tibbiyot texnikumi — kelajakdagi kasbingiz sari ishonchli qadam! 🎓\n\n📲 Batafsil ma’lumot uchun:\n☎️ 88 260 20 73\n☎️ 77 088 20 73\n☎️ 97 266 20 73\n\n❤️ Bu videoni tibbiyotda o‘qishni xohlayotgan do‘stingizga yuboring!\nView all comments",
        "media_url": "https://instagram.fbhk1-3.fna.fbcdn.net/v/t51.82787-15/773867678_17891038656603794_2411323614986854335_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=106&_nc_map=urlgen_bucketless&ig_cache_key=Mzk2NjQyMTY2MzYwNjE2OTc5NDE3ODkxMDM4NjUzNjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=lRczLmR4ebAQ7kNvwGoD4Jk&_nc_oc=AdoeCN4TzCr96cIe59UjZmXvwR3KI4ypsrY-xOANlmwEEwc3qeOxsxjq-JwJx0HaNvU&_nc_zt=23&_nc_ht=instagram.fbhk1-3.fna&_nc_gid=bmwhPmqcKt0FHX2B0G_eYg&_nc_ss=7aa8c&oh=00_AQGxQuT1oJIW8wdBZ_34bWcyQU5act2Hbl6GzmacIFMHdw&oe=6A8DFD4F",
        "post_date": ""
    },
    {
        "shortcode": "DcLkGzAqbz9",
        "post_url": "https://www.instagram.com/reel/DcLkGzAqbz9",
        "media_type": "reel",
        "caption": "shahrisabz_t_t_uz\n\n🩺 Bugun kasb tanlaysiz — ertaga shu kasb bilan daromad topasiz! 🎓✨\n\nKelajagingiz uchun to‘g‘ri tanlov qiling!\n🏥 Shahrisabz tibbiyot texnikumi — bilim, kasb va kelajak sari ishonchli qadam! ❤️\n\n📲 Batafsil ma’lumot uchun:\n☎️ 88 260 20 73\n☎️ 77 088 20 73\n☎️ 97 266 20 73\nView all 7 comments",
        "media_url": "https://instagram.fbhk1-2.fna.fbcdn.net/v/t51.82787-15/774744693_17891039091603794_4793673403631759598_n.jpg?stp=dst-jpg_e15_tt6&_nc_cat=108&_nc_map=urlgen_bucketless&ig_cache_key=Mzk2NjQyMjY5MzU5MzA3MDg0NTE3ODkxMDM5MDg1NjAzNzk0.3-ccb7-5&ccb=7-5&_nc_sid=58cdad&efg=eyJ2ZW5jb2RlX3RhZyI6IkNMSVBTLnhwaWRzLjcyMC5zZHIudmlkZW9fZGVmYXVsdF9jb3Zlcl9mcmFtZS5DMyJ9&_nc_ohc=nj0Z85cFMCUQ7kNvwG828N8&_nc_oc=AdrUSs9syFItQTmijha-H-0N6K5JgMQCtkXLWtZmblC5jMKCKggeQtxFlk7ISA74TkQ&_nc_zt=23&_nc_ht=instagram.fbhk1-2.fna&_nc_gid=D9TNLp_1NuJqqEm_9IhPag&_nc_ss=7aa8c&oh=00_AQGGlqqAoC-u-ydHi_6vCwVRdZRBBquy-G7ChE5qxKoQ7A&oe=6A8DF6F6",
        "post_date": ""
    }
]


def init_insta_tables():
    """Instagram jadvallarini yaratish va 74 ta videoni bazaga sinxronlash"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Navbat jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_posts_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shortcode TEXT UNIQUE,
        post_url TEXT NOT NULL,
        media_type TEXT DEFAULT 'reel',
        caption TEXT,
        media_url TEXT,
        post_date TEXT,
        status TEXT DEFAULT 'PENDING',
        scheduled_at TIMESTAMP,
        sent_at TIMESTAMP,
        error_msg TEXT,
        likes_count INTEGER DEFAULT 0,
        telegram_msg_id INTEGER,
        youtube_uploaded INTEGER DEFAULT 0,
        youtube_url TEXT,
        youtube_uploaded_at TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Migration ustunlar
    cursor.execute("PRAGMA table_info(insta_posts_queue)")
    cols = [row["name"] for row in cursor.fetchall()]
    if "likes_count" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN likes_count INTEGER DEFAULT 0")
        except Exception: pass
    if "telegram_msg_id" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN telegram_msg_id INTEGER")
        except Exception: pass
    if "youtube_uploaded" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN youtube_uploaded INTEGER DEFAULT 0")
        except Exception: pass
    if "youtube_url" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN youtube_url TEXT")
        except Exception: pass
    if "youtube_uploaded_at" not in cols:
        try: cursor.execute("ALTER TABLE insta_posts_queue ADD COLUMN youtube_uploaded_at TEXT")
        except Exception: pass
    
    # 2. Layklar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_post_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(post_id, user_id)
    )
    """)
    
    # 3. Sozlamalar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insta_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)
    
    defaults = {
        "bot_token": DEFAULT_BOT_TOKEN,
        "target_chat_id": DEFAULT_TARGET_CHAT_ID,
        "insta_username": DEFAULT_INSTA_USERNAME,
        "auto_schedule_enabled": "0",
        "interval_minutes": "60",
        "last_post_time": "",
        "is_scanning": "0",
        "last_scan_time": "",
        "last_scan_count": "74",
        "night_mode_enabled": "1",
        "night_mode_start": "00:00",
        "night_mode_end": "07:00",
        "insta_session_id": "61835138797%3AzWTgfIiOPBUkVE%3A13%3AAYiLE6mFSW2M7qmjat3MGNfyqvWPPoaneRmr-c__Gg",
        "youtube_token_json": "",
        "youtube_auto_upload": "1",
        "youtube_schedule_enabled": "1",
        "youtube_schedule_times": "09:00,12:00,15:00,18:30,21:00",
        "youtube_last_posted_slot": ""
    }
    
    for k, v in defaults.items():
        cursor.execute("INSERT OR IGNORE INTO insta_settings (key, value) VALUES (?, ?)", (k, v))
        
    # Eski 18 ta yuklangan postlarni tozalash (DTHudhLiEJT gacha bo'lgan)
    cursor.execute("""
    DELETE FROM insta_posts_queue 
    WHERE shortcode IN (
        'DRjbVIVCKY4', 'DRodxW9iPAr', 'DRtp7ONiAtK', 'DRy5jtWiId5', 'DR6hnfsCFyT',
        'DSE-3rGiKBm', 'DSJ8o_MCK6L', 'DSPNK1QiLHZ', 'DSUShSniPWi', 'DSZZK5-iGaQ',
        'DSem0aaiO5s', 'DSjq4LCCB4l', 'DSo84-gCD7E', 'DSuH3e7iD4N', 'DSzWzXdiB5t',
        'DS4nL3iiIdL', 'DTB-Fz7iJ4A', 'DTHudhLiEJT', 'DTKl4neiIGi', 'DTKl2WlCFbP',
        'DTKlzm8CJ5N', 'Db0U9ivIcwC'
    ) OR media_type = 'post'
    """)
    
    # 4. Agar navbat 70 tadan kam bo'lsa, barcha 74 ta videoni eskisidan yangisiga qarab qayta joylash
    cursor.execute("SELECT COUNT(*) as cnt FROM insta_posts_queue")
    cnt_val = cursor.fetchone()["cnt"]
    if cnt_val < 50:
        cursor.execute("DELETE FROM insta_posts_queue")
        for p in DEFAULT_SEEDED_POSTS:
            cursor.execute("""
            INSERT INTO insta_posts_queue (shortcode, post_url, media_type, caption, media_url, post_date, status)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
            """, (p["shortcode"], p["url"], p.get("media_type") or "reel", p.get("caption") or "", p.get("media_url") or "", p.get("post_date") or ""))
    else:
        for p in DEFAULT_SEEDED_POSTS:
            cursor.execute("""
            UPDATE insta_posts_queue 
            SET caption = CASE WHEN caption IS NULL OR caption = '' THEN ? ELSE caption END,
                post_date = CASE WHEN post_date IS NULL OR post_date = '' THEN ? ELSE post_date END,
                media_type = 'reel',
                media_url = CASE WHEN media_url IS NULL OR media_url = '' THEN ? ELSE media_url END
            WHERE shortcode = ?
            """, (p.get("caption") or "", p.get("post_date") or "", p.get("media_url") or "", p["shortcode"]))

    conn.commit()
    conn.close()


def get_setting(key, default=""):
    """Sozlamani olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM insta_settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row["value"]
    except Exception as e:
        print(f"[Insta Settings Error]: {e}")
    return default


def set_setting(key, value):
    """Sozlamani yangilash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO insta_settings (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Insta Set Setting Error]: {e}")
        return False


def get_all_settings():
    """Barcha sozlamalarni lug'at ko'rinishida olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM insta_settings")
        rows = cursor.fetchall()
        conn.close()
        return {r["key"]: r["value"] for r in rows}
    except Exception as e:
        print(f"[Insta Get All Settings Error]: {e}")
        return {}

# ------------------------------------------------------------
# 2. Like Boshqaruvi va Inline Tugmalar
# ------------------------------------------------------------

def get_post_inline_keyboard(post_id, post_url, likes_count=0):
    """Post tagidagi Like va Instagramga o'tish inline tugmalari"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn_like = telebot.types.InlineKeyboardButton(f"❤️ {likes_count}", callback_data=f"insta_like_{post_id}")
    btn_link = telebot.types.InlineKeyboardButton("🔗 Instagramda ko‘rish", url=post_url)
    markup.add(btn_like, btn_link)
    return markup


def toggle_post_like(post_id, user_id):
    """Foydalanuvchi like bosganda layklar sonini yangilash (Toggle)"""
    init_insta_tables()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM insta_post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("DELETE FROM insta_post_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        is_liked = False
    else:
        cursor.execute("INSERT OR IGNORE INTO insta_post_likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
        is_liked = True
        
    cursor.execute("SELECT COUNT(*) as cnt FROM insta_post_likes WHERE post_id = ?", (post_id,))
    total_likes = cursor.fetchone()["cnt"]
    
    cursor.execute("UPDATE insta_posts_queue SET likes_count = ? WHERE id = ?", (total_likes, post_id))
    conn.commit()
    
    cursor.execute("SELECT post_url, telegram_msg_id FROM insta_posts_queue WHERE id = ?", (post_id,))
    post_data = cursor.fetchone()
    conn.close()
    
    return {
        "is_liked": is_liked,
        "likes_count": total_likes,
        "post_url": post_data["post_url"] if post_data else "https://instagram.com",
        "telegram_msg_id": post_data["telegram_msg_id"] if post_data else None
    }


def clean_caption_text(raw_caption, username=None):
    """Instagram caption matnini tozalash"""
    if not raw_caption:
        return ""
    text = raw_caption.strip()
    
    if username and text.lower().startswith(username.lower()):
        text = text[len(username):].strip()
        
    patterns = [
        r'View all \d+ comments.*',
        r'View \d+ more comments.*',
        r'View more on Instagram.*',
        r'Add a comment\.\.\..*',
        r'Log in to like or comment.*',
        r'\d+\s+likes\s*$',
        r'View profile.*',
    ]
    for p in patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE | re.DOTALL).strip()
        
    return text

# ------------------------------------------------------------
# 3. YouTube Shorts Jadval Boshqaruvi
# ------------------------------------------------------------

DEFAULT_YOUTUBE_SCHEDULE_TIMES = "09:00,12:00,15:00,18:30,21:00"

def get_youtube_schedule_times():
    """Sozlangan YouTube vaqtlarini ro'yxat ko'rinishida olish"""
    raw = get_setting("youtube_schedule_times", DEFAULT_YOUTUBE_SCHEDULE_TIMES)
    times = [t.strip() for t in raw.split(",") if t.strip()]
    # Normalize times to HH:MM format
    normalized = []
    for t in times:
        m = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", t)
        if m:
            normalized.append(f"{int(m.group(1)):02d}:{int(m.group(2)):02d}")
    return sorted(list(set(normalized)))


def add_youtube_schedule_time(time_str):
    """Yangi vaqt qo'shish (Format: HH:MM)"""
    time_str = str(time_str).strip()
    match = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", time_str)
    if not match:
        return False, "Noto'g'ri format! Vaqtni '14:30' yoki '20:00' formatida kiriting."
    
    hh, mm = match.groups()
    formatted = f"{int(hh):02d}:{int(mm):02d}"
    
    current_times = get_youtube_schedule_times()
    if formatted in current_times:
        return False, f"Ushbu vaqt ({formatted}) allaqachon jadvalda mavjud!"
        
    current_times.append(formatted)
    current_times = sorted(list(set(current_times)))
    set_setting("youtube_schedule_times", ",".join(current_times))
    return True, formatted


def remove_youtube_schedule_time(time_str):
    """Vaqtni jadvaldan o'chirish"""
    current_times = get_youtube_schedule_times()
    time_str = str(time_str).strip()
    
    m = re.match(r"^([01]?\d|2[0-3]):([0-5]\d)$", time_str)
    formatted = f"{int(m.group(1)):02d}:{int(m.group(2)):02d}" if m else time_str
    
    if formatted in current_times:
        current_times.remove(formatted)
        set_setting("youtube_schedule_times", ",".join(current_times))
        return True
    return False


def reset_youtube_schedule_times():
    """Standart 5 ta YouTube vaqtlariga qaytarish (09:00, 12:00, 15:00, 18:30, 21:00)"""
    set_setting("youtube_schedule_times", DEFAULT_YOUTUBE_SCHEDULE_TIMES)
    return ["09:00", "12:00", "15:00", "18:30", "21:00"]

# ------------------------------------------------------------
# 4. Instagram Profile Scraper (Playwright)
# ------------------------------------------------------------

async def _scrape_instagram_profile_async(username, max_posts=150):
    """Playwright orqali profil postlarini skanerlash"""
    try:
        from playwright.async_api import async_playwright
    except ImportError as e:
        raise ImportError("Playwright kutubxonasi o'rnatilmagan.") from e
    
    collected_links = []
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 900}
            )
            page = await context.new_page()
            
            url = f"https://www.instagram.com/{username}/"
            print(f"[Insta Scraper]: Sahifa ochilmoqda: {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)
            
            seen_codes = set()
            scroll_attempts = 0
            max_scrolls = 25
            stagnant_count = 0
            
            while scroll_attempts < max_scrolls and len(seen_codes) < max_posts:
                links = await page.evaluate('''() => {
                    const anchors = Array.from(document.querySelectorAll('a'));
                    return anchors.map(a => a.href).filter(h => h.includes('/reel/'));
                }''')
                
                initial_len = len(seen_codes)
                for l in links:
                    parts = l.split('?')[0].rstrip('/')
                    code = parts.split('/')[-1]
                    if code and code not in seen_codes:
                        seen_codes.add(code)
                        collected_links.append({
                            "shortcode": code,
                            "url": parts,
                            "is_reel": True
                        })
                        
                if len(seen_codes) == initial_len:
                    stagnant_count += 1
                    if stagnant_count >= 4:
                        break
                else:
                    stagnant_count = 0
                    
                await page.evaluate("window.scrollBy(0, 1600)")
                await asyncio.sleep(2)
                scroll_attempts += 1
                
            await browser.close()
    except Exception as be:
        print(f"[Playwright Launch/Scrape Error]: {be}")
        raise be
        
    return collected_links


def add_posts_by_urls(urls_text):
    """Foydalanuvchi kiritgan Instagram havolalari yoki shortcode'larini navbatga qo'shish"""
    init_insta_tables()
    if not urls_text or not str(urls_text).strip():
        return {"success": False, "error": "Havolalar kiritilmadi"}
    
    text = str(urls_text).strip()
    codes = []
    
    # 1. URL pattern orqali topish (masalan: instagram.com/reel/CODE yoki instagram.com/p/CODE)
    url_matches = re.findall(r'instagram\.com/(?:[a-zA-Z0-9_\.]+/)?(?:reel|p)/([A-Za-z0-9_-]+)', text, re.IGNORECASE)
    for c in url_matches:
        c = c.strip('/')
        if c and c not in codes:
            codes.append(c)
            
    # 2. Qatorlar bo'yicha ajratish
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = line.split('?')[0].rstrip('/')
        parts = cleaned.split('/')
        last_part = parts[-1].strip()
        if len(last_part) >= 9 and len(last_part) <= 15 and re.match(r'^[A-Za-z0-9_-]+$', last_part):
            if last_part not in codes:
                codes.append(last_part)
                
    if not codes:
        return {"success": False, "error": "Birorta ham to'g'ri Instagram post/reel havolasi yoki kodi topilmadi"}
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    added_count = 0
    for code in codes:
        is_reel = True
        post_url = f"https://www.instagram.com/reel/{code}"
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO insta_posts_queue (shortcode, post_url, media_type, status)
            VALUES (?, ?, ?, 'PENDING')
            """, (code, post_url, "reel" if is_reel else "post"))
            if cursor.rowcount > 0:
                added_count += 1
        except Exception as e:
            print(f"[Manual Add Error]: {e}")
            
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "total_parsed": len(codes),
        "new_added": added_count,
        "codes": codes,
        "message": f"{len(codes)} ta postdan {added_count} tasi navbatga muvaffaqiyatli qo'shildi."
    }


def scan_and_enqueue_posts(username=None, max_posts=150):
    """Instagram profilini skanerlab, barcha postlarni eskisidan yangisiga tartibda bazaga qo'shish"""
    init_insta_tables()
    if not username:
        username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
        
    set_setting("is_scanning", "1")
    set_setting("last_scan_error", "")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        links = loop.run_until_complete(_scrape_instagram_profile_async(username, max_posts=max_posts))
        loop.close()
        
        links_chronological = list(reversed(links))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        added_count = 0
        for item in links_chronological:
            try:
                cursor.execute("""
                INSERT OR IGNORE INTO insta_posts_queue (shortcode, post_url, media_type, status)
                VALUES (?, ?, ?, 'PENDING')
                """, (item["shortcode"], item["url"], "reel" if item["is_reel"] else "post"))
                if cursor.rowcount > 0:
                    added_count += 1
            except Exception as _e:
                print(f"[Enqueue Error]: {_e}")
                
        conn.commit()
        conn.close()
        
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_setting("last_scan_time", now_str)
        set_setting("last_scan_count", str(len(links)))
        set_setting("is_scanning", "0")
        
        return {
            "success": True,
            "total_found": len(links),
            "new_added": added_count,
            "username": username
        }
    except Exception as e:
        err_msg = str(e)
        set_setting("is_scanning", "0")
        set_setting("last_scan_error", err_msg)
        print(f"[Scan Instagram Error]: {e}")
        return {
            "success": False,
            "error": err_msg
        }


def scan_in_background(username=None, callback_notify=None):
    """Fon rejimida skanerlash"""
    def _task():
        res = scan_and_enqueue_posts(username)
        if callback_notify:
            try:
                callback_notify(res)
            except Exception as e:
                print(f"[Scan Callback Error]: {e}")
                
    th = threading.Thread(target=_task, daemon=True)
    th.start()
    return th

# ------------------------------------------------------------
# 5. HD Video yuklash va Telegram / YouTube ga yuborish
# ------------------------------------------------------------

def _download_hd_video_ytdlp(post_url):
    """yt-dlp Python moduli yordamida videoni to'g'ridan-to'g'ri yuklab olish (Vercel va barcha tizimlarda 100% ishlaydi)"""
    try:
        import yt_dlp
        temp_dir = tempfile.gettempdir()
        out_filename = os.path.join(temp_dir, f"insta_hd_{int(time.time()*1000)}.mp4")
        
        ydl_opts = {
            "outtmpl": out_filename,
            "format": "best[ext=mp4]/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post_url])
            
        if os.path.exists(out_filename) and os.path.getsize(out_filename) > 10000:
            return out_filename
            
        base_prefix = out_filename.replace(".mp4", "")
        for ext in [".mp4", ".mkv", ".webm"]:
            cand = base_prefix + ext
            if os.path.exists(cand) and os.path.getsize(cand) > 10000:
                return cand
    except Exception as e:
        print(f"[yt-dlp Python Module Error]: {e}")
        
    return None


async def _fetch_post_content_async(post_url):
    """Postning to'liq ma'lumotlarini olish (yt-dlp orqali tezkor va xavfsiz)"""
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "socket_timeout": 15
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(post_url, download=False)
            if info:
                desc = info.get("description") or info.get("title") or ""
                v_url = info.get("url")
                t_url = info.get("thumbnail")
                return {
                    "caption": desc,
                    "video_url": v_url,
                    "img_url": t_url,
                    "all_imgs": [t_url] if t_url else []
                }
    except Exception as yte:
        print(f"[yt-dlp info error]: {yte}")

    try:
        from playwright.async_api import async_playwright
        parts = post_url.rstrip('/').split('/')
        code = parts[-1]
        is_reel = "/reel/" in post_url
        embed_url = f"https://www.instagram.com/{'reel' if is_reel else 'p'}/{code}/embed/captioned/"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            )
            page = await context.new_page()
            await page.goto(embed_url, wait_until="domcontentloaded", timeout=15000)
            await asyncio.sleep(1)
            
            data = await page.evaluate('''() => {
                const captionEl = document.querySelector('.Caption') || document.querySelector('.CaptionComments');
                let cap = captionEl ? captionEl.innerText : "";
                const videoEl = document.querySelector('video');
                const imgEl = document.querySelector('.EmbeddedMediaImage') || document.querySelector('img.EmbeddedMedia');
                let allImgs = Array.from(document.querySelectorAll('img')).map(i => i.src).filter(s => s && (s.includes('cdninstagram') || s.includes('fbcdn')));
                return {
                    caption: cap,
                    video_url: videoEl ? videoEl.src : null,
                    img_url: imgEl ? imgEl.src : (allImgs.length > 0 ? allImgs[0] : null),
                    all_imgs: allImgs
                };
            }''')
            await browser.close()
            return data
    except Exception as pe:
        print(f"[Playwright skipped]: {pe}")
        
    return {"caption": "", "video_url": None, "img_url": None, "all_imgs": []}


def post_next_queued_item(chat_id=None, bot_token=None):
    """Navbatdagi eng eski 1 ta postni olib Telegramga yuborish"""
    init_insta_tables()
    
    if not bot_token:
        bot_token = get_setting("bot_token", DEFAULT_BOT_TOKEN)
    if not chat_id:
        chat_id = get_setting("target_chat_id", DEFAULT_TARGET_CHAT_ID)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM insta_posts_queue 
    WHERE status = 'PENDING' 
    ORDER BY id ASC 
    LIMIT 1
    """)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {
            "success": False,
            "empty": True,
            "message": "Navbatda yuborilmagan postlar qolmadi!"
        }
        
    post_id = row["id"]
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    bot = telebot.TeleBot(bot_token)
    
    try:
        username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
        
        raw_caption = row["caption"] or ""
        video_direct_url = None
        
        if not raw_caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            video_direct_url = content.get("video_url")
            
        clean_caption = clean_caption_text(raw_caption, username)
        
        if len(clean_caption) > 1000:
            telegram_caption = clean_caption[:997] + "..."
        else:
            telegram_caption = clean_caption
            
        inline_kb = get_post_inline_keyboard(post_id, post_url, likes_count=0)
        
        media_sent = False
        sent_msg = None
        
        # 1. HD Video yuklash (Reels/Video postlar uchun)
        if row["media_type"] in ("reel", "video") or "/reel/" in post_url:
            hd_video_path = _download_hd_video_ytdlp(post_url)
            if hd_video_path and os.path.exists(hd_video_path):
                try:
                    with open(hd_video_path, 'rb') as v_file:
                        sent_msg = bot.send_video(
                            chat_id,
                            v_file,
                            caption=telegram_caption,
                            parse_mode="HTML" if telegram_caption else None,
                            reply_markup=inline_kb,
                            supports_streaming=True
                        )
                    media_sent = True
                finally:
                    if os.path.exists(hd_video_path):
                        os.remove(hd_video_path)
                        
            if not media_sent and video_direct_url:
                v_res = requests.get(video_direct_url, timeout=40)
                if v_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
                        f.write(v_res.content)
                        temp_v_path = f.name
                    try:
                        with open(temp_v_path, 'rb') as v_file:
                            sent_msg = bot.send_video(
                                chat_id,
                                v_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb,
                                supports_streaming=True
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_v_path):
                            os.remove(temp_v_path)
                            
        # 2. Rasm jo'natish (Statik rasm postlari uchun)
        if not media_sent and (row.get("media_url") or row.get("img_url")):
            img_url = row.get("media_url") or row.get("img_url")
            try:
                p_res = requests.get(img_url, timeout=30)
                if p_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                        f.write(p_res.content)
                        temp_p_path = f.name
                    try:
                        with open(temp_p_path, 'rb') as p_file:
                            sent_msg = bot.send_photo(
                                chat_id,
                                p_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_p_path):
                            os.remove(temp_p_path)
            except Exception as _pe:
                print(f"[Photo Send Err]: {_pe}")
                
        # 3. Matnli xabar orqali jo'natish (oxirgi zaxira)
        if not media_sent:
            sent_msg = bot.send_message(
                chat_id,
                telegram_caption or f"📢 Instagram: {post_url}",
                reply_markup=inline_kb,
                parse_mode="HTML" if telegram_caption else None
            )
            media_sent = True
            
        now_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
        msg_id_val = sent_msg.message_id if sent_msg else None
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'SENT', sent_at = ?, caption = ?, error_msg = NULL, telegram_msg_id = ?
        WHERE id = ?
        """, (now_str, clean_caption, msg_id_val, post_id))
        conn.commit()
        
        set_setting("last_post_time", now_str)
        conn.close()
        
        return {
            "success": True,
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption[:80]
        }
        
    except Exception as e:
        err_msg = str(e)
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'FAILED', error_msg = ?
        WHERE id = ?
        """, (err_msg, post_id))
        conn.commit()
        conn.close()
        print(f"[Post Next Error]: {e}")
        return {
            "success": False,
            "post_id": post_id,
            "error": err_msg
        }


def post_next_youtube_video():
    """Navbatdagi eng eski 1 ta videoni olib YouTube Shorts ga yuklash"""
    init_insta_tables()
    from services.youtube_service import is_youtube_ready, upload_video_to_youtube
    
    if not is_youtube_ready():
        return {
            "success": False,
            "error": "YouTube avtorizatsiyasi mavjud emas! (youtube_token.json)"
        }
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hali YouTubega yuklanmagan eng eski video yoki reelni topish
    cursor.execute("""
    SELECT * FROM insta_posts_queue 
    WHERE (media_type IN ('reel', 'video', 'unknown') OR post_url LIKE '%/reel/%')
      AND youtube_uploaded = 0
    ORDER BY id ASC 
    LIMIT 1
    """)
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {
            "success": False,
            "empty": True,
            "message": "YouTubega yuklash uchun navbatda yangi videolar qolmadi!"
        }
        
    post_id = row["id"]
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
    
    try:
        # 1. Post matnini olish
        caption = row["caption"]
        if not caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            caption = clean_caption_text(raw_caption, username)
            
        # 2. HD Videoni yuklab olish
        vpath = _download_hd_video_ytdlp(post_url)
        if not vpath or not os.path.exists(vpath):
            conn.close()
            return {
                "success": False,
                "error": f"Videoni yuklab bo'lmadi: {post_url}"
            }
            
        # 3. YouTube Shorts ga yuklash
        yt_res = upload_video_to_youtube(
            vpath,
            caption=caption,
            post_url=post_url,
            privacy="public",
            is_shorts=True
        )
        
        if os.path.exists(vpath):
            os.remove(vpath)
            
        if yt_res.get("success"):
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            UPDATE insta_posts_queue 
            SET youtube_uploaded = 1, youtube_url = ?, youtube_uploaded_at = ?, caption = ?
            WHERE id = ?
            """, (yt_res.get("url"), now_str, caption, post_id))
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "post_id": post_id,
                "shortcode": shortcode,
                "url": yt_res.get("url"),
                "title": yt_res.get("title")
            }
        else:
            conn.close()
            return {
                "success": False,
                "error": yt_res.get("error")
            }
    except Exception as e:
        conn.close()
        print(f"[YouTube Upload Queue Error]: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ------------------------------------------------------------
# 6. Statistics & Queue Control
# ------------------------------------------------------------

def get_queue_stats():
    """Navbat holati va hisoboti"""
    init_insta_tables()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM insta_posts_queue")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as pending FROM insta_posts_queue WHERE status = 'PENDING'")
    pending = cursor.fetchone()["pending"]
    
    cursor.execute("SELECT COUNT(*) as sent FROM insta_posts_queue WHERE status = 'SENT'")
    sent = cursor.fetchone()["sent"]
    
    cursor.execute("SELECT COUNT(*) as failed FROM insta_posts_queue WHERE status = 'FAILED'")
    failed = cursor.fetchone()["failed"]
    
    cursor.execute("SELECT COUNT(*) as yt_uploaded FROM insta_posts_queue WHERE youtube_uploaded = 1")
    yt_uploaded = cursor.fetchone()["yt_uploaded"]
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE status = 'PENDING' ORDER BY id ASC LIMIT 1")
    next_post = cursor.fetchone()
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE status = 'SENT' ORDER BY sent_at DESC LIMIT 1")
    last_sent = cursor.fetchone()
    
    conn.close()
    settings = get_all_settings()
    
    next_post_dict = dict(next_post) if next_post else None
    last_sent_dict = dict(last_sent) if last_sent else None
    
    # Calculate next scheduled post time and status
    interval_min = int(settings.get("interval_minutes") or 60)
    last_post_str = settings.get("last_post_time", "")
    
    next_time_str = "Hozir (Navbatdagi siklda)"
    is_night_now = False
    
    now = get_uzb_now()
    now_hm = now.strftime("%H:%M")
    
    night_on = settings.get("night_mode_enabled", "1") == "1"
    night_start = settings.get("night_mode_start", "00:00")
    night_end = settings.get("night_mode_end", "07:00")
    
    if night_on:
        if night_start <= night_end:
            is_night_now = (night_start <= now_hm < night_end)
        else:
            is_night_now = (now_hm >= night_start or now_hm < night_end)
            
    if is_night_now:
        next_time_str = f"Ertalab soat {night_end} da (Tungi rejim faol)"
    elif last_post_str:
        try:
            last_dt = datetime.strptime(last_post_str, "%Y-%m-%d %H:%M:%S")
            target_dt = last_dt + timedelta(minutes=interval_min)
            if target_dt > now:
                next_time_str = target_dt.strftime("%H:%M")
            else:
                next_time_str = "Hozir (Navbatdagi siklda)"
        except Exception:
            next_time_str = "Hozir"
            
    return {
        "total": total,
        "pending": pending,
        "sent": sent,
        "failed": failed,
        "yt_uploaded": yt_uploaded,
        "next_post": next_post_dict,
        "last_sent": last_sent_dict,
        "next_time_estimate": next_time_str,
        "is_night_mode_active": is_night_now,
        "settings": settings
    }


def reset_queue_status():
    """Barcha FAILED postlarni qayta PENDING qilish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE insta_posts_queue SET status = 'PENDING' WHERE status = 'FAILED'")
    count = cursor.rowcount
    conn.commit()
    conn.close()
    return count


def clear_all_queue():
    """Barcha navbatni tozalash"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM insta_posts_queue")
    conn.commit()
    conn.close()
    return True

def delete_queue_item(post_id):
    """Bitta postni navbatdan o'chirish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM insta_posts_queue WHERE id = ?", (post_id,))
        cursor.execute("DELETE FROM insta_post_likes WHERE post_id = ?", (post_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    except Exception as e:
        print(f"[Delete Queue Item Error]: {e}")
        return False


def get_queue_items(page=1, limit=50, status=None, search=None):
    """Navbatdagi postlarni sahifalash, Toshkent vaqti bo'yicha aniq rejalashtirilgan vaqtlar va qidiruv bilan olish"""
    init_insta_tables()
    page = max(1, int(page))
    limit = max(1, min(200, int(limit)))
    offset = (page - 1) * limit
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    where_clauses = []
    params = []
    
    if status and status.upper() not in ("ALL", ""):
        if status.upper() == "YOUTUBE":
            where_clauses.append("youtube_uploaded = 1")
        else:
            where_clauses.append("status = ?")
            params.append(status.upper())
            
    if search:
        s_term = f"%{search.strip()}%"
        where_clauses.append("(shortcode LIKE ? OR caption LIKE ?)")
        params.extend([s_term, s_term])
        
    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    
    # Count total matching
    count_sql = f"SELECT COUNT(*) as cnt FROM insta_posts_queue {where_sql}"
    cursor.execute(count_sql, params)
    total_count = cursor.fetchone()["cnt"]
    
    # Order: If status == 'SENT', sent_at DESC, else id ASC (xronologik eng eskisidan yangisiga)
    order_sql = "ORDER BY sent_at DESC" if status and status.upper() == "SENT" else "ORDER BY id ASC"
    
    query_sql = f"""
    SELECT id, shortcode, post_url, media_type, caption, media_url, post_date,
           status, sent_at, error_msg, likes_count, telegram_msg_id,
           youtube_uploaded, youtube_url, youtube_uploaded_at, created_at
    FROM insta_posts_queue
    {where_sql}
    {order_sql}
    LIMIT ? OFFSET ?
    """
    cursor.execute(query_sql, params + [limit, offset])
    rows = [dict(r) for r in cursor.fetchall()]
    
    # Barcha PENDING postlar uchun rejalashtirilgan kelgusi vaqtlarni hisoblash
    cursor.execute("SELECT id FROM insta_posts_queue WHERE status = 'PENDING' ORDER BY id ASC")
    all_pending_ids = [r["id"] for r in cursor.fetchall()]
    conn.close()
    
    settings = get_all_settings()
    interval_min = int(settings.get("interval_minutes") or 60)
    last_post_str = settings.get("last_post_time", "")
    night_on = settings.get("night_mode_enabled", "1") == "1"
    night_start_str = settings.get("night_mode_start", "00:00")
    night_end_str = settings.get("night_mode_end", "07:00")
    
    now = get_uzb_now()
    
    start_dt = now
    if last_post_str:
        try:
            last_dt = datetime.strptime(last_post_str, "%Y-%m-%d %H:%M:%S")
            cand = last_dt + timedelta(minutes=interval_min)
            if cand > now:
                start_dt = cand
            else:
                start_dt = now
        except Exception:
            start_dt = now
            
    # Har bir kutilayotgan postga Toshkent vaqti bo'yicha sana va soat belgilash
    curr_time = start_dt
    schedule_map = {}
    for pid in all_pending_ids:
        if night_on:
            hm_str = curr_time.strftime("%H:%M")
            if night_start_str <= hm_str < night_end_str:
                end_parts = night_end_str.split(":")
                curr_time = curr_time.replace(hour=int(end_parts[0]), minute=int(end_parts[1]), second=0)
                if curr_time < now:
                    curr_time += timedelta(days=1)
        schedule_map[pid] = curr_time.strftime("%d.%m.%Y %H:%M")
        curr_time += timedelta(minutes=interval_min)
        
    for r in rows:
        r["scheduled_time"] = schedule_map.get(r["id"]) or "—"
        
    return {
        "success": True,
        "items": rows,
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit if limit > 0 else 1
    }


def post_single_item(post_id, chat_id=None, bot_token=None):
    """Bitta aniq tanlangan postni Telegramga yuborish"""
    init_insta_tables()
    
    if not bot_token:
        bot_token = get_setting("bot_token", DEFAULT_BOT_TOKEN)
    if not chat_id:
        chat_id = get_setting("target_chat_id", DEFAULT_TARGET_CHAT_ID)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM insta_posts_queue WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"success": False, "error": f"Post topilmadi (ID: {post_id})"}
        
    shortcode = row["shortcode"]
    post_url = row["post_url"]
    
    bot = telebot.TeleBot(bot_token)
    
    try:
        username = get_setting("insta_username", DEFAULT_INSTA_USERNAME)
        
        raw_caption = row["caption"] or ""
        video_direct_url = None
        if not raw_caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(_fetch_post_content_async(post_url))
            loop.close()
            raw_caption = content.get("caption") or ""
            video_direct_url = content.get("video_url")
            
        clean_caption = clean_caption_text(raw_caption, username)
        
        if len(clean_caption) > 1000:
            telegram_caption = clean_caption[:997] + "..."
        else:
            telegram_caption = clean_caption
            
        inline_kb = get_post_inline_keyboard(post_id, post_url, likes_count=row["likes_count"] or 0)
        
        media_sent = False
        sent_msg = None
        
        # 1. HD Video yuklash (Reels/Video postlar uchun)
        if row["media_type"] in ("reel", "video") or "/reel/" in post_url:
            hd_video_path = _download_hd_video_ytdlp(post_url)
            if hd_video_path and os.path.exists(hd_video_path):
                try:
                    with open(hd_video_path, 'rb') as v_file:
                        sent_msg = bot.send_video(
                            chat_id,
                            v_file,
                            caption=telegram_caption,
                            parse_mode="HTML" if telegram_caption else None,
                            reply_markup=inline_kb,
                            supports_streaming=True
                        )
                    media_sent = True
                finally:
                    if os.path.exists(hd_video_path):
                        os.remove(hd_video_path)
                        
            if not media_sent and video_direct_url:
                v_res = requests.get(video_direct_url, timeout=40)
                if v_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
                        f.write(v_res.content)
                        temp_v_path = f.name
                    try:
                        with open(temp_v_path, 'rb') as v_file:
                            sent_msg = bot.send_video(
                                chat_id,
                                v_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb,
                                supports_streaming=True
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_v_path):
                            os.remove(temp_v_path)
                            
        # 2. Rasm jo'natish (Statik rasm postlari uchun)
        if not media_sent and (row.get("media_url") or row.get("img_url")):
            img_url = row.get("media_url") or row.get("img_url")
            try:
                p_res = requests.get(img_url, timeout=30)
                if p_res.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                        f.write(p_res.content)
                        temp_p_path = f.name
                    try:
                        with open(temp_p_path, 'rb') as p_file:
                            sent_msg = bot.send_photo(
                                chat_id,
                                p_file,
                                caption=telegram_caption,
                                parse_mode="HTML" if telegram_caption else None,
                                reply_markup=inline_kb
                            )
                        media_sent = True
                    finally:
                        if os.path.exists(temp_p_path):
                            os.remove(temp_p_path)
            except Exception as _pe:
                print(f"[Photo Send Err]: {_pe}")
                
        # 3. Matnli xabar orqali jo'natish (oxirgi zaxira)
        if not media_sent:
            sent_msg = bot.send_message(
                chat_id,
                telegram_caption or f"📢 Instagram: {post_url}",
                reply_markup=inline_kb,
                parse_mode="HTML" if telegram_caption else None
            )
            media_sent = True
            
        now_str = get_uzb_now().strftime("%Y-%m-%d %H:%M:%S")
        msg_id_val = sent_msg.message_id if sent_msg else None
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'SENT', sent_at = ?, caption = ?, error_msg = NULL, telegram_msg_id = ?
        WHERE id = ?
        """, (now_str, clean_caption, msg_id_val, post_id))
        conn.commit()
        
        set_setting("last_post_time", now_str)
        conn.close()
        
        return {
            "success": True,
            "post_id": post_id,
            "shortcode": shortcode,
            "post_url": post_url,
            "caption": clean_caption[:80]
        }
    except Exception as e:
        err_msg = str(e)
        cursor.execute("""
        UPDATE insta_posts_queue 
        SET status = 'FAILED', error_msg = ?
        WHERE id = ?
        """, (err_msg, post_id))
        conn.commit()
        conn.close()
        print(f"[Post Single Error]: {e}")
        return {
            "success": False,
            "post_id": post_id,
            "error": err_msg
        }


