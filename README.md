# Task Manager Bot

Küçük ekipler için görevleri yönetmeye yardımcı olacak bir Discord botu.

## Özellikler

-   `!add_task <açıklama>`: Yeni bir görev ekler.
-   `!show_tasks`: Tüm görevleri listeler.
-   `!delete_task <görev_id>`: Belirli bir görevi siler.
-   `!complete_task <görev_id>`: Belirli bir görevi tamamlandı olarak işaretler.

## Önkoşullar

-   Python 3.8 veya üzeri
-   pip

## Kurulum ve Yapılandırma

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/ozgekrby/task_manager_bot_python.git
    cd task_manager_bot_python
    ```

2.  **Sanal Ortam Oluşturun ve Aktive Edin (Önerilir):**
    ```bash
    python -m venv venv
    # Windows için:
    venv\Scripts\activate
    # macOS/Linux için:
    source venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Kurun:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Discord Botu Oluşturun ve Token Alın:**
    *   [Discord Developer Portal](https://discord.com/developers/applications) adresine gidin.
    *   "New Application" butonuna tıklayarak yeni bir uygulama oluşturun.
    *   Uygulamanızı seçtikten sonra sol menüden "Bot" sekmesine gidin.
    *   "TOKEN" başlığı altında "Copy" butonuna tıklayarak bot token'ınızı kopyalayın. **Bu token'ı kimseyle paylaşmayın!**
    *   Aynı sayfada, "Privileged Gateway Intents" bölümü altında **"Message Content Intent"** seçeneğini etkinleştirin. Bu, botun mesaj içeriklerini okuyabilmesi için gereklidir.

5.  **`.env` Dosyasını Yapılandırın:**
    Proje ana dizininde (`task_manager_bot_python/`) `.env` adında bir dosya oluşturun ve içine kopyaladığınız bot token'ını yapıştırın:
    ```env
    DISCORD_TOKEN=BURAYA_KOPYALADIGINIZ_BOT_TOKENINI_YAPISTIRIN
    ```

6.  **Botu Sunucunuza Davet Edin:**
    *   Discord Developer Portal'da uygulamanızın sayfasında, sol menüden "OAuth2" -> "URL Generator" sekmesine gidin.
    *   "SCOPES" bölümünden `bot` seçeneğini işaretleyin.
    *   Aşağıda açılan "BOT PERMISSIONS" bölümünden botunuz için gerekli izinleri seçin. En azından şunlar gereklidir:
        *   `Send Messages`
        *   `Read Message History`
        *   (Eğer embed kullanacaksanız `Embed Links`)
    *   Sayfanın en altında oluşan URL'yi kopyalayın, bir tarayıcıda açın ve botu istediğiniz sunucuya davet edin.

## Botu Çalıştırma

Proje ana dizinindeyken (ve sanal ortamınız aktifken) aşağıdaki komutu çalıştırın:
```bash
python bot.py
```
Botunuz Discord'a bağlanacak ve komutları dinlemeye başlayacaktır.

## Veritabanı

Bu bot, görevleri saklamak için `tasks.db` adında bir SQLite veritabanı kullanır. Bu dosya, bot ilk kez çalıştırıldığında proje ana dizininde otomatik olarak oluşturulur.

## Testler

Proje için yazılmış birim testlerini çalıştırmak için proje ana dizinindeyken aşağıdaki komutu kullanın:
```bash
python -m unittest discover tests
```
