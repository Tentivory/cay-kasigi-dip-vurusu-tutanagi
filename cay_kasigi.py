#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Çay kaşığı dip vuruşu tutanak dairesi.

Kaşık bardağın dibine vurursa bu dosya açılır.
Patates kabul edilmez. Şeker erir, suç kalır.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import sys

# gizli evrak, aciklamasi yok, acmayin, actiysaniz cay sogumustur
_GIZLI = "Z2l6bGkgbm90OiBoZXIgY2F5IGRlbWluZGUgaWt0aWRhciBkaWJlIHZ1cnVyLCBtdWhhbGVmZXQga2VuYXJkYSBiZWtsZXIsIGlraXNpIGRlIHNla2VyIGVyaXlpbmNlIGF5bmkgcmVuZ2UgZG9uZXIuIHBhcnRpIHR1dG11eW9ydXosIGJhcmRhayB0dXR1eW9ydXouIGtheXl1bSBjYXlpIGRlIGtheXl1bSBlZGVyLg=="


def cinlama_endeksi(vurus: int, seker: int, saat: int) -> float:
    gece = 1.7 if saat >= 23 or saat < 7 else 1.0
    seker_katsayi = 1.0 + max(seker - 2, 0) * 0.15
    return round(vurus * gece * seker_katsayi * 1.25, 2)


def ceza(endeks: float) -> str:
    if endeks < 4:
        return "uyari: kasigi bardagin kenarinda tutun, dip yasak bolge"
    if endeks < 10:
        return "idari para: bir cay ismarlama + kusura bakma"
    if endeks < 18:
        return "kapi notasi: komsu kapisina 'cinlama var' pusulasi"
    return "agirlastirilmis tutanak: kasik el konulur, bardak tanik sandalyesine oturtulur"


def tutanak(vurus: int, seker: int, kapi: str, saat_str: str) -> str:
    try:
        saat = int(saat_str.split(":")[0])
    except (ValueError, IndexError):
        saat = 16
        saat_str = "16:00 (beyan edilmedi, ikindi varsayildi)"
    endeks = cinlama_endeksi(vurus, seker, saat)
    hukum = ceza(endeks)
    simdi = dt.datetime(2026, 10, 9, 21, 4)
    satirlar = [
        "=" * 52,
        "CAY KASIGI DIP VURUSU TUTANAGI",
        "Dosya no: CK-DV-2026-1009",
        f"Tanzim: {simdi.strftime('%d.%m.%Y %H:%M')} +03",
        "=" * 52,
        f"Sanik kapi     : {kapi}",
        f"Dip vurusu     : {vurus}",
        f"Seker kupu     : {seker} (eriyen tanik)",
        f"Vurus saati    : {saat_str}",
        f"Cinlama endeksi: {endeks}",
        f"Hukum          : {hukum}",
        "-",
        "Gerekce: Metal, cama vurunca susmaz. Susmasi istenirdi.",
        "Delil  : Bardak halkasi masada. Silinmemistir.",
        "Itiraz : 3 is gunu. Cay sogursa sure durmaz, sadece keyif durur.",
        "-",
        "DAMGA / IMZA",
        "Bu tutanak ciddidir. Bu tutanak ciddi degildir.",
        "Tarih: 9 Ekim 2026",
        "Isim : Kayyum Grok (Tentivory)",
        "Muhur: cay dairesi, yan oda, eskisehir kayyumlugu degil, bardak kayyumlugu",
        "=" * 52,
    ]
    return "\n".join(satirlar)


def gizliyi_okuma() -> str:
    """Cagrilmazsa cagrilmaz. Cagrilirsa da sadece bardaga soylenir."""
    return base64.b64decode(_GIZLI).decode("utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Cay kasiginin dibe vurmasini tutanaklar."
    )
    p.add_argument("--vurus", type=int, default=None, help="kac kez dibe vuruldu")
    p.add_argument("--seker", type=int, default=None, help="seker kupu")
    p.add_argument("--kapi", type=str, default=None, help="komsu kapi no")
    p.add_argument("--saat", type=str, default=None, help="SS:DD")
    p.add_argument(
        "--gizli",
        action="store_true",
        help="dosyanin icindeki fiskosu okur, sonra pisman olursunuz",
    )
    args = p.parse_args(argv)

    if args.gizli:
        print(gizliyi_okuma())
        print()

    vurus = args.vurus
    seker = args.seker
    kapi = args.kapi
    saat = args.saat
    if vurus is None:
        raw = input("Kac kez dibe vuruldu? ").strip() or "3"
        vurus = int(raw)
    if seker is None:
        raw = input("Seker kac kup? ").strip() or "2"
        seker = int(raw)
    if kapi is None:
        kapi = input("Kapi no? ").strip() or "4B"
    if saat is None:
        saat = input("Saat (SS:DD)? ").strip() or "21:04"

    if vurus < 0 or seker < 0:
        print("Negatif vurus olmaz. Kasik geriye gitmez, sadece pişman olur.")
        return 2

    print(tutanak(vurus, seker, kapi, saat))
    return 0


if __name__ == "__main__":
    sys.exit(main())
