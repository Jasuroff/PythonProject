from flask import Flask, render_template_string, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# HTML SHA BLON - To'liq dizayn bilan
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇺🇿 Valyuta va Kripto Kurslari</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            padding: 30px 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 30px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 20px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo i {
            font-size: 2.5rem;
            color: #2a5298;
        }

        .logo h1 {
            font-size: 2rem;
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .date-box {
            background: linear-gradient(135deg, #667eea20, #764ba220);
            padding: 12px 25px;
            border-radius: 50px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #2a5298;
            font-weight: 600;
        }

        .update-status {
            background: linear-gradient(135deg, #1e3c720d, #2a52980d);
            padding: 15px 25px;
            border-radius: 15px;
            margin-bottom: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .refresh-btn {
            background: #2a5298;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: 0.3s;
        }

        .refresh-btn:hover {
            background: #1e3c72;
            transform: translateY(-2px);
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 25px;
        }

        .section-title i {
            font-size: 1.8rem;
            color: #2a5298;
            background: rgba(42, 82, 152, 0.1);
            padding: 10px;
            border-radius: 15px;
        }

        .section-title h2 {
            font-size: 1.6rem;
            color: #333;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .card {
            background: white;
            border-radius: 25px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: 0.3s;
            border: 1px solid rgba(0,0,0,0.05);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(42, 82, 152, 0.15);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        .card-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .card-icon i {
            font-size: 2rem;
        }

        .usd i { color: #27ae60; }
        .eur i { color: #2980b9; }
        .rub i { color: #e67e22; }
        .btc i { color: #f7931a; }
        .eth i { color: #627eea; }
        .gold i { color: #ffd700; }

        .card-info h3 {
            font-size: 1.2rem;
            color: #333;
            margin-bottom: 5px;
        }

        .card-code {
            font-size: 0.8rem;
            color: #666;
            background: #f0f0f0;
            padding: 3px 12px;
            border-radius: 50px;
        }

        .rate {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1e3c72;
            margin-bottom: 10px;
        }

        .rate small {
            font-size: 1rem;
            color: #666;
            font-weight: normal;
        }

        .change {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 5px 12px;
            border-radius: 50px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .positive { background: rgba(39, 174, 96, 0.1); color: #27ae60; }
        .negative { background: rgba(231, 76, 60, 0.1); color: #e74c3c; }

        .card-footer {
            margin-top: 20px;
            color: #888;
            font-size: 0.85rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .converter {
            background: linear-gradient(135deg, #667eea0d, #764ba20d);
            border-radius: 30px;
            padding: 30px;
            margin-top: 30px;
        }

        .converter-box {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .converter-item {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .converter-item label {
            font-weight: 600;
            color: #555;
        }

        .converter-item input,
        .converter-item select {
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            font-size: 1rem;
        }

        .convert-btn {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 15px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: 0.3s;
        }

        .convert-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(42, 82, 152, 0.4);
        }

        .result {
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.3rem;
            font-weight: 700;
            color: #2a5298;
            border: 2px dashed #2a5298;
            margin-top: 20px;
        }

        footer {
            margin-top: 40px;
            text-align: center;
            color: #666;
            padding-top: 30px;
            border-top: 2px solid #f0f0f0;
        }

        @media (max-width: 768px) {
            .container { padding: 20px; }
            .logo h1 { font-size: 1.5rem; }
            .section-title h2 { font-size: 1.3rem; }
            .rate { font-size: 1.8rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <i class="fas fa-chart-line"></i>
                <h1>🇺🇿 Kurslar.uz</h1>
            </div>
            <div class="date-box">
                <i class="far fa-calendar-alt"></i>
                {{ time }}
            </div>
        </header>

        <div class="update-status">
            <span><i class="fas fa-sync-alt"></i> So'nggi yangilanish: {{ time }}</span>
            <button onclick="location.reload()" class="refresh-btn">
                <i class="fas fa-redo-alt"></i> Yangilash
            </button>
        </div>

        <!-- MARKAZIY BANK VALYUTALARI -->
        <div class="section-title">
            <i class="fas fa-university"></i>
            <h2>🏦 Markaziy Bank kurslari</h2>
        </div>

        <div class="grid">
            <!-- USD -->
            <div class="card usd">
                <div class="card-header">
                    <div class="card-icon usd">
                        <i class="fas fa-dollar-sign"></i>
                    </div>
                    <div class="card-info">
                        <h3>AQSH Dollari</h3>
                        <span class="card-code">USD</span>
                    </div>
                </div>
                <div class="rate">
                    {{ usd_rate }} <small>so'm</small>
                </div>
                <div class="card-footer">
                    <span><i class="far fa-calendar"></i> {{ usd_date }}</span>
                </div>
            </div>

            <!-- EUR -->
            <div class="card eur">
                <div class="card-header">
                    <div class="card-icon eur">
                        <i class="fas fa-euro-sign"></i>
                    </div>
                    <div class="card-info">
                        <h3>Yevro</h3>
                        <span class="card-code">EUR</span>
                    </div>
                </div>
                <div class="rate">
                    {{ eur_rate }} <small>so'm</small>
                </div>
                <div class="card-footer">
                    <span><i class="far fa-calendar"></i> {{ eur_date }}</span>
                </div>
            </div>

            <!-- RUB -->
            <div class="card rub">
                <div class="card-header">
                    <div class="card-icon rub">
                        <i class="fas fa-ruble-sign"></i>
                    </div>
                    <div class="card-info">
                        <h3>Rossiya Rubli</h3>
                        <span class="card-code">RUB</span>
                    </div>
                </div>
                <div class="rate">
                    {{ rub_rate }} <small>so'm (10 RUB)</small>
                </div>
                <div class="card-footer">
                    <span><i class="far fa-calendar"></i> {{ rub_date }}</span>
                </div>
            </div>
        </div>

        <!-- KRIPTOVA LYUTALAR -->
        <div class="section-title">
            <i class="fas fa-coins"></i>
            <h2>₿ Kriptovalyutalar</h2>
        </div>

        <div class="grid">
            <!-- Bitcoin -->
            <div class="card btc">
                <div class="card-header">
                    <div class="card-icon btc">
                        <i class="fab fa-bitcoin"></i>
                    </div>
                    <div class="card-info">
                        <h3>Bitcoin</h3>
                        <span class="card-code">BTC</span>
                    </div>
                </div>
                <div class="rate">
                    ${{ btc_price }} 
                </div>
                <div class="card-footer">
                    <span class="change {{ btc_change_class }}">
                        <i class="fas {{ btc_change_icon }}"></i> {{ btc_change }}%
                    </span>
                    <span>24 soat</span>
                </div>
            </div>

            <!-- Ethereum -->
            <div class="card eth">
                <div class="card-header">
                    <div class="card-icon eth">
                        <i class="fab fa-ethereum"></i>
                    </div>
                    <div class="card-info">
                        <h3>Ethereum</h3>
                        <span class="card-code">ETH</span>
                    </div>
                </div>
                <div class="rate">
                    ${{ eth_price }}
                </div>
                <div class="card-footer">
                    <span class="change {{ eth_change_class }}">
                        <i class="fas {{ eth_change_icon }}"></i> {{ eth_change }}%
                    </span>
                    <span>24 soat</span>
                </div>
            </div>

            <!-- Oltin -->
            <div class="card gold">
                <div class="card-header">
                    <div class="card-icon gold">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="card-info">
                        <h3>Oltin</h3>
                        <span class="card-code">XAU</span>
                    </div>
                </div>
                <div class="rate">
                    ${{ gold_price }}
                </div>
                <div class="card-footer">
                    <span class="change positive">
                        <i class="fas fa-arrow-up"></i> {{ gold_change }}%
                    </span>
                    <span>1 untsiya</span>
                </div>
            </div>
        </div>

        <!-- VALYUTA KONVERTERI -->
        <div class="converter">
            <div class="section-title">
                <i class="fas fa-calculator"></i>
                <h2>💱 Valyuta konverteri</h2>
            </div>

            <div class="converter-box">
                <div class="converter-item">
                    <label>Miqdor</label>
                    <input type="number" id="amount" value="1" min="0" step="0.01">
                </div>

                <div class="converter-item">
                    <label>Dan</label>
                    <select id="fromCurrency">
                        <option value="USD">USD - AQSH dollari</option>
                        <option value="EUR">EUR - Yevro</option>
                        <option value="RUB">RUB - Rossiya rubli</option>
                    </select>
                </div>

                <div class="converter-item">
                    <label>Ga</label>
                    <select id="toCurrency">
                        <option value="UZS">UZS - O'zbek so'mi</option>
                    </select>
                </div>

                <div class="converter-item">
                    <button onclick="convertCurrency()" class="convert-btn">
                        <i class="fas fa-exchange-alt"></i> Hisoblash
                    </button>
                </div>
            </div>

            <div id="result" class="result">
                1 USD = {{ usd_rate }} UZS
            </div>
        </div>

        <footer>
            <p><i class="fas fa-database"></i> Ma'lumotlar: O'zbekiston Markaziy Banki va CoinGecko</p>
            <p style="margin-top: 10px;">© 2024 Kurslar.uz - Barcha huquqlar himoyalangan</p>
        </footer>
    </div>

    <script>
        // Valyuta konverteri
        function convertCurrency() {
            const amount = document.getElementById('amount').value;
            const from = document.getElementById('fromCurrency').value;

            let rate = 0;

            {% if usd_rate_raw %}
                if (from === 'USD') rate = {{ usd_rate_raw }};
            {% endif %}
            {% if eur_rate_raw %}
                if (from === 'EUR') rate = {{ eur_rate_raw }};
            {% endif %}
            {% if rub_rate_raw %}
                if (from === 'RUB') rate = {{ rub_rate_raw }} / 10;
            {% endif %}

            const result = amount * rate;

            document.getElementById('result').innerHTML = 
                `${amount} ${from} = ${result.toLocaleString('uz-UZ', {minimumFractionDigits: 2, maximumFractionDigits: 2})} UZS`;
        }

        // Enter tugmasi bilan hisoblash
        document.getElementById('amount').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') convertCurrency();
        });

        // Select o'zgarishi bilan hisoblash
        document.getElementById('fromCurrency').addEventListener('change', convertCurrency);
        document.getElementById('amount').addEventListener('input', convertCurrency);
    </script>
</body>
</html>
'''


def get_cbu_rates():
    """O'zbekiston Markaziy Bankidan barcha valyuta kurslarini olish"""
    rates = {
        'usd': {'rate': '12500.00', 'date': datetime.now().strftime('%d.%m.%Y')},
        'eur': {'rate': '13500.00', 'date': datetime.now().strftime('%d.%m.%Y')},
        'rub': {'rate': '1350.00', 'date': datetime.now().strftime('%d.%m.%Y')}
    }

    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            for currency in data:
                if currency["Ccy"] == "USD":
                    rates['usd'] = {
                        'rate': f"{float(currency['Rate']):,.2f}",
                        'raw': float(currency['Rate']),
                        'date': currency['Date']
                    }
                elif currency["Ccy"] == "EUR":
                    rates['eur'] = {
                        'rate': f"{float(currency['Rate']):,.2f}",
                        'raw': float(currency['Rate']),
                        'date': currency['Date']
                    }
                elif currency["Ccy"] == "RUB":
                    rates['rub'] = {
                        'rate': f"{float(currency['Rate']):,.2f}",
                        'raw': float(currency['Rate']),
                        'date': currency['Date']
                    }
    except Exception as e:
        print(f"CBU API xatolik: {e}")

    return rates


def get_crypto_rates():
    """Kriptovalyuta narxlarini olish"""
    crypto = {
        'btc': {'price': '42,500', 'change': '+2.5', 'change_class': 'positive', 'change_icon': 'fa-arrow-up'},
        'eth': {'price': '2,250', 'change': '+1.8', 'change_class': 'positive', 'change_icon': 'fa-arrow-up'},
        'gold': {'price': '1,950.50', 'change': '0.5', 'change_class': 'positive', 'change_icon': 'fa-arrow-up'}
    }

    try:
        # Bitcoin
        btc_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        btc_response = requests.get(btc_url, timeout=5)
        if btc_response.status_code == 200:
            btc_data = btc_response.json()
            btc_price = f"{btc_data['bitcoin']['usd']:,.0f}"
            btc_change = btc_data['bitcoin'].get('usd_24h_change', 2.5)
            crypto['btc'] = {
                'price': btc_price,
                'change': f"{btc_change:+.1f}",
                'change_class': 'positive' if btc_change >= 0 else 'negative',
                'change_icon': 'fa-arrow-up' if btc_change >= 0 else 'fa-arrow-down'
            }

        # Ethereum
        eth_url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true"
        eth_response = requests.get(eth_url, timeout=5)
        if eth_response.status_code == 200:
            eth_data = eth_response.json()
            eth_price = f"{eth_data['ethereum']['usd']:,.0f}"
            eth_change = eth_data['ethereum'].get('usd_24h_change', 1.8)
            crypto['eth'] = {
                'price': eth_price,
                'change': f"{eth_change:+.1f}",
                'change_class': 'positive' if eth_change >= 0 else 'negative',
                'change_icon': 'fa-arrow-up' if eth_change >= 0 else 'fa-arrow-down'
            }
    except Exception as e:
        print(f"Crypto API xatolik: {e}")

    return crypto


@app.route('/')
def index():
    """Asosiy sahifa"""
    # Joriy vaqt
    current_time = datetime.now().strftime('%d %B %Y, %H:%M')

    # Valyuta kurslari
    rates = get_cbu_rates()

    # Kriptovalyutalar
    crypto = get_crypto_rates()

    return render_template_string(
        HTML_TEMPLATE,
        time=current_time,

        # USD
        usd_rate=rates['usd']['rate'],
        usd_rate_raw=rates['usd'].get('raw', 12500),
        usd_date=rates['usd']['date'],

        # EUR
        eur_rate=rates['eur']['rate'],
        eur_rate_raw=rates['eur'].get('raw', 13500),
        eur_date=rates['eur']['date'],

        # RUB
        rub_rate=rates['rub']['rate'],
        rub_rate_raw=rates['rub'].get('raw', 1350),
        rub_date=rates['rub']['date'],

        # Bitcoin
        btc_price=crypto['btc']['price'],
        btc_change=crypto['btc']['change'],
        btc_change_class=crypto['btc']['change_class'],
        btc_change_icon=crypto['btc']['change_icon'],

        # Ethereum
        eth_price=crypto['eth']['price'],
        eth_change=crypto['eth']['change'],
        eth_change_class=crypto['eth']['change_class'],
        eth_change_icon=crypto['eth']['change_icon'],

        # Oltin
        gold_price=crypto['gold']['price'],
        gold_change=crypto['gold']['change'],
        gold_change_class=crypto['gold']['change_class'],
        gold_change_icon=crypto['gold']['change_icon']
    )


@app.route('/api/rates')
def api_rates():
    """API - JSON format"""
    rates = get_cbu_rates()
    crypto = get_crypto_rates()

    return jsonify({
        'cbu': rates,
        'crypto': crypto,
        'update_time': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("🚀 Kurslar.uz ishga tushmoqda...")
    print("📱 Brauzerda oching: http://127.0.0.1:5000")
    print("💰 USD, EUR, RUB, BTC, ETH, GOLD kurslari mavjud")
    app.run(debug=True, host='127.0.0.1', port=5000)