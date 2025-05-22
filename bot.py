import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from database import init_db, add_task_db, get_tasks_db, delete_task_db, complete_task_db, get_task_by_id_db

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    print("Hata: DISCORD_TOKEN ortam değişkeni bulunamadı.")
    print("Lütfen .env dosyası oluşturup içine DISCORD_TOKEN=YOUR_BOT_TOKEN yazın veya sistem ortam değişkeni olarak ayarlayın.")
    exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Bot hazır olduğunda çalışır."""
    print(f'{bot.user.name} Discord\'a bağlandı!')
    print(f'Bot ID: {bot.user.id}')
    init_db()
    print("Veritabanı hazır.")

@bot.command(name="add_task", help="Yeni bir görev ekler. Kullanım: !add_task <açıklama>")
async def add_task(ctx, *, description: str):
    """Yeni bir görev ekler."""
    if not description:
        await ctx.send("Lütfen bir görev açıklaması girin. Kullanım: `!add_task <açıklama>`")
        return
    
    task_id = add_task_db(description)
    await ctx.send(f"✅ Görev eklendi! ID: `{task_id}`. Görev: `{description}`")

@bot.command(name="show_tasks", help="Tüm görevleri listeler.")
async def show_tasks(ctx):
    """Tüm görevleri listeler."""
    tasks = get_tasks_db()
    if not tasks:
        await ctx.send("📋 Gösterilecek görev bulunmuyor.")
        return

    response = "📋 **Görev Listesi:**\n"
    for task in tasks:
        task_id, description, completed = task
        status_emoji = "✅" if completed else "❌"
        response += f"{task_id}: {description} {status_emoji}\n"
    
    await ctx.send(response)

@bot.command(name="delete_task", help="Belirli bir ID'ye sahip görevi siler. Kullanım: !delete_task <task_id>")
async def delete_task(ctx, task_id: int):
    """Belirli bir ID'ye sahip görevi siler."""
    try:
        task_id = int(task_id) 
        if delete_task_db(task_id):
            await ctx.send(f"🗑️ Görev `{task_id}` başarıyla silindi.")
        else:
            await ctx.send(f"⚠️ `{task_id}` ID'li görev bulunamadı.")
    except ValueError:
        await ctx.send("Lütfen geçerli bir görev ID'si girin. Örneğin: `!delete_task 1`")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")


@bot.command(name="complete_task", help="Belirli bir ID'ye sahip görevi tamamlandı olarak işaretler. Kullanım: !complete_task <task_id>")
async def complete_task(ctx, task_id: int):
    """Belirli bir ID'ye sahip görevi tamamlandı olarak işaretler."""
    try:
        task_id = int(task_id)
        task = get_task_by_id_db(task_id)

        if not task:
            await ctx.send(f"⚠️ `{task_id}` ID'li görev bulunamadı.")
            return
        
        if task[2] == 1:
            await ctx.send(f"ℹ️ `{task_id}` ID'li görev zaten tamamlanmış durumda.")
            return

        if complete_task_db(task_id):
            await ctx.send(f"✔️ Görev `{task_id}` tamamlandı olarak işaretlendi.")
        else:
            await ctx.send(f"⚠️ `{task_id}` ID'li görev tamamlanamadı veya bulunamadı.")
    except ValueError:
        await ctx.send("Lütfen geçerli bir görev ID'si girin. Örneğin: `!complete_task 1`")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Komut hatalarını yakalar."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Bilinmeyen komut. Yardım için `!help` yazabilirsiniz.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Eksik argüman. Komutun doğru kullanımı için `!help {ctx.command.name}` yazın.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"⚠️ Geçersiz argüman tipi. Komutun doğru kullanımı için `!help {ctx.command.name}` yazın.")
    else:
        print(f"Bir hata oluştu: {error}")
        await ctx.send("Beklenmedik bir hata oluştu. Lütfen daha sonra tekrar deneyin.")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)