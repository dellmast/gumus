# Gümüş fiyat bildirimi (Telegram)

Gram gümüş fiyatını TL cinsinden takip eder. Telegram'a mesaj gönderir:
- her saat başı özet,
- fiyat son referans noktasından 1 TL arttığında uyarı.

Fiyat, ons gümüş (USD) ile USD/TRY kurundan hesaplanır. Ziraat Bankası'nın alış/satış
farkı yüzünden uygulamadaki fiyattan biraz farklı olur.

## Kurulum

### 1. Telegram botu
1. Telegram'da **@BotFather**'a `/newbot` yaz, adını seç. Sana bir **token** verir.
2. Oluşturduğun bota Telegram'dan bir kere `/start` yaz.
3. Tarayıcıda şu adresi aç (TOKEN yerine kendi token'ın):
   `https://api.telegram.org/botTOKEN/getUpdates`
   Çıktıdaki `"chat":{"id": 123456789` sayısı senin **chat id**'n.

### 2. GitHub deposu
1. GitHub'da **public** yeni bir depo oluştur (neden public: aşağıdaki nota bak).
2. Bu klasördeki üç dosyayı depoya yükle:
   - `monitor.py`
   - `.github/workflows/silver-alert.yml`
   - `README.md` (isteğe bağlı)
3. Depoda **Settings → Secrets and variables → Actions → New repository secret** ile şunları ekle:
   - `TELEGRAM_BOT_TOKEN`: BotFather'ın verdiği token
   - `TELEGRAM_CHAT_ID`: yukarıdaki chat id
   - `GRAMS` (isteğe bağlı): elindeki gümüş miktarı (örn. `250`). Eklersen mesajlarda toplam TL değeri de görünür.
4. **Actions** sekmesinden `silver-alert` iş akışını aç ve **Run workflow** ile bir kere elle çalıştır. Telegram'a "Gümüş takibi başladı" mesajı gelmeli.

Sonrası otomatik: 5 dakikada bir kontrol edilir.

## Notlar
- **Public depo öner­ilir:** public depolarda Actions ücretsiz ve sınırsızdır. Private depoda aylık ücretsiz dakika
  (2000) 5 dakikalık kontrole yetmez. Token'lar secret olarak saklandığı için görünmez. Depoda sadece
  `state.json` (son referans fiyat) görünür. `GRAMS` secret olduğu için miktarın da gizli kalır.
- **Saat başı mesajı tam saatinde gelmeyebilir.** GitHub zamanlanmış işleri yoğunlukta 5–15 dakika geciktirebilir.
  Mesaj, yeni saatteki ilk çalışmada gelir.
- **Referans fiyat** düşüşü takip eder: fiyat düşerse referans da düşer, sonra oradan 1 TL yükselince uyarı gelir.
- **Eşiği değiştirmek** için `monitor.py` içindeki `STEP_TL` değerini düzenle.
- Depo 60 gün hiç hareketsiz kalırsa GitHub zamanlanmış işleri durdurabilir. `state.json` güncellemeleri
  genelde bunu engeller. Durursa Actions sekmesinden yeniden etkinleştir.
