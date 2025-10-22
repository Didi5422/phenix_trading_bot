import requests
import pandas as pd
import time
from datetime import datetime

# ============================================================
# 🔹 CONFIGURATION TELEGRAM
# ============================================================
TELEGRAM_TOKEN = "8235809690:AAEq9mGSH7GlyHj2mBuarAPMExbBUxtrHJM"  # <-- Mets ici le token que @BotFather t’a donné
CHAT_ID = "1330710292"       # <-- Mets ici ton ID Telegram (avec @userinfobot)

# Fonction d’envoi de message Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Message envoyé sur Telegram !")
    else:
        print(f"❌ Erreur Telegram : {response.text}")

# 🔥 Test immédiat
send_telegram_message("🚀 Test de connexion : le bot Phénix Trading est opérationnel !")

# ============================================================
# 🔹 ANALYSE CRYPTO
# ============================================================
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }
    data = requests.get(url, params=params).json()
    df = pd.DataFrame(data)
    return df[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]

def analyze_crypto(df):
    # Ratio volume/capitalisation
    df['volume_to_cap_ratio'] = df['total_volume'] / df['market_cap']

    # Calcul du RSI (simplifié sur base des variations de prix)
    df['price_change_24h'] = df['price_change_percentage_24h']
    df['RSI'] = 50 + (df['price_change_24h'] * 2)  # estimation grossière (simplifiée)

    # Sélection des cryptos prometteuses
    promising = df[
        (df['RSI'] < 55) &  # Pas trop suracheté
        (df['RSI'] > 45) &  # Pas survendu
        (df['volume_to_cap_ratio'] > 0.05) &  # Volume significatif
        (df['market_cap'] > 1e8)  # Market cap > 100M
    ]

    return promising

# ============================================================
# 🔹 BOUCLE PRINCIPALE
# ============================================================
def main():
    print("🚀 Démarrage du bot d'analyse crypto avancé...")
    while True:
        df = get_crypto_data()
        result = analyze_crypto(df)

        print("\n=== 🔎 Cryptos prometteuses détectées ===")
        print(result)

        if not result.empty:
            message = "🚨 Cryptos prometteuses détectées !\n\n"
            for _, row in result.iterrows():
                message += (
                    f"💎 {row['name']} ({row['symbol'].upper()})\n"
                    f"💰 Prix : ${row['current_price']}\n"
                    f"📊 RSI : {round(row['RSI'], 2)}\n"
                    f"🏦 Cap : {round(row['market_cap']/1e6, 2)}M$\n"
                    f"📈 Variation 24h : {round(row['price_change_24h'], 2)}%\n\n"
                )
            send_telegram_message(message)
        else:
            print("Aucune crypto prometteuse pour le moment.")

        print("\n⏳ Prochaine analyse dans 10 minutes...")
        time.sleep(600)

# ============================================================
# 🔹 EXECUTION
# ============================================================
if __name__ == "__main__":
    main()
