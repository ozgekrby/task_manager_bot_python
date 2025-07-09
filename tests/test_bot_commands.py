import unittest
import os
import sys
import asyncio
from unittest.mock import Mock, patch, AsyncMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import init_db, clear_tasks_table, get_tasks_db

class TestBotCommands(unittest.TestCase):
    TEST_DB_NAME = "test_bot_commands.db"

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.TEST_DB_NAME):
            os.remove(cls.TEST_DB_NAME)
        init_db(db_name=cls.TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.TEST_DB_NAME):
            os.remove(cls.TEST_DB_NAME)

    def setUp(self):
        clear_tasks_table(db_name=self.TEST_DB_NAME)
        self.mock_ctx = Mock()
        self.mock_ctx.send = AsyncMock()

    def test_add_task_command_valid_description(self):
        from bot import add_task
        description = "Test task description"
        
        with patch('bot.add_task_db') as mock_add_task:
            mock_add_task.return_value = 1
            
            asyncio.run(add_task(self.mock_ctx, description=description))
            
            mock_add_task.assert_called_once_with(description)
            self.mock_ctx.send.assert_called_once_with(f"✅ Görev eklendi! ID: `1`. Görev: `{description}`")

    def test_add_task_command_empty_description(self):
        from bot import add_task
        
        asyncio.run(add_task(self.mock_ctx, description=""))
        
        self.mock_ctx.send.assert_called_once_with("Lütfen bir görev açıklaması girin. Kullanım: `!add_task <açıklama>`")

    def test_add_task_command_whitespace_description(self):
        from bot import add_task
        
        with patch('bot.add_task_db') as mock_add_task:
            mock_add_task.return_value = 1
            
            asyncio.run(add_task(self.mock_ctx, description="   "))
            
            mock_add_task.assert_called_once_with("   ")
            self.mock_ctx.send.assert_called_once_with("✅ Görev eklendi! ID: `1`. Görev: `   `")

    def test_add_task_command_special_characters(self):
        from bot import add_task
        description = "Task with !@#$%^&*()"
        
        with patch('bot.add_task_db') as mock_add_task:
            mock_add_task.return_value = 1
            
            asyncio.run(add_task(self.mock_ctx, description=description))
            
            mock_add_task.assert_called_once_with(description)

    def test_add_task_command_unicode_characters(self):
        from bot import add_task
        description = "Görev with émojis 🎉"
        
        with patch('bot.add_task_db') as mock_add_task:
            mock_add_task.return_value = 1
            
            asyncio.run(add_task(self.mock_ctx, description=description))
            
            mock_add_task.assert_called_once_with(description)

    def test_show_tasks_command_no_tasks(self):
        from bot import show_tasks
        
        with patch('bot.get_tasks_db') as mock_get_tasks:
            mock_get_tasks.return_value = []
            
            asyncio.run(show_tasks(self.mock_ctx))
            
            mock_get_tasks.assert_called_once()
            self.mock_ctx.send.assert_called_once_with("📋 Gösterilecek görev bulunmuyor.")

    def test_show_tasks_command_with_tasks(self):
        from bot import show_tasks
        tasks = [(1, "Task 1", 0), (2, "Task 2", 1)]
        
        with patch('bot.get_tasks_db') as mock_get_tasks:
            mock_get_tasks.return_value = tasks
            
            asyncio.run(show_tasks(self.mock_ctx))
            
            mock_get_tasks.assert_called_once()
            expected_response = "📋 **Görev Listesi:**\n1: Task 1 ❌\n2: Task 2 ✅\n"
            self.mock_ctx.send.assert_called_once_with(expected_response)

    def test_delete_task_command_valid_id(self):
        from bot import delete_task
        
        with patch('bot.delete_task_db') as mock_delete_task:
            mock_delete_task.return_value = True
            
            asyncio.run(delete_task(self.mock_ctx, task_id=1))
            
            mock_delete_task.assert_called_once_with(1)
            self.mock_ctx.send.assert_called_once_with("🗑️ Görev `1` başarıyla silindi.")

    def test_delete_task_command_invalid_id(self):
        from bot import delete_task
        
        with patch('bot.delete_task_db') as mock_delete_task:
            mock_delete_task.return_value = False
            
            asyncio.run(delete_task(self.mock_ctx, task_id=999))
            
            mock_delete_task.assert_called_once_with(999)
            self.mock_ctx.send.assert_called_once_with("⚠️ `999` ID'li görev bulunamadı.")

    def test_delete_task_command_non_numeric_id(self):
        from bot import delete_task
        
        asyncio.run(delete_task(self.mock_ctx, task_id="abc"))
        
        self.mock_ctx.send.assert_called_once_with("Lütfen geçerli bir görev ID'si girin. Örneğin: `!delete_task 1`")

    def test_delete_task_command_negative_id(self):
        from bot import delete_task
        
        with patch('bot.delete_task_db') as mock_delete_task:
            mock_delete_task.return_value = False
            
            asyncio.run(delete_task(self.mock_ctx, task_id=-1))
            
            mock_delete_task.assert_called_once_with(-1)
            self.mock_ctx.send.assert_called_once_with("⚠️ `-1` ID'li görev bulunamadı.")

    def test_complete_task_command_valid_id(self):
        from bot import complete_task
        
        with patch('bot.get_task_by_id_db') as mock_get_task:
            mock_get_task.return_value = (1, "Task 1", 0)
            
            with patch('bot.complete_task_db') as mock_complete_task:
                mock_complete_task.return_value = True
                
                asyncio.run(complete_task(self.mock_ctx, task_id=1))
                
                mock_get_task.assert_called_once_with(1)
                mock_complete_task.assert_called_once_with(1)
                self.mock_ctx.send.assert_called_once_with("✔️ Görev `1` tamamlandı olarak işaretlendi.")

    def test_complete_task_command_already_completed(self):
        from bot import complete_task
        
        with patch('bot.get_task_by_id_db') as mock_get_task:
            mock_get_task.return_value = (1, "Task 1", 1)
            
            asyncio.run(complete_task(self.mock_ctx, task_id=1))
            
            mock_get_task.assert_called_once_with(1)
            self.mock_ctx.send.assert_called_once_with("ℹ️ `1` ID'li görev zaten tamamlanmış durumda.")

    def test_complete_task_command_non_existing_id(self):
        from bot import complete_task
        
        with patch('bot.get_task_by_id_db') as mock_get_task:
            mock_get_task.return_value = None
            
            asyncio.run(complete_task(self.mock_ctx, task_id=999))
            
            mock_get_task.assert_called_once_with(999)
            self.mock_ctx.send.assert_called_once_with("⚠️ `999` ID'li görev bulunamadı.")

    def test_complete_task_command_invalid_id(self):
        from bot import complete_task
        
        asyncio.run(complete_task(self.mock_ctx, task_id="abc"))
        
        self.mock_ctx.send.assert_called_once_with("Lütfen geçerli bir görev ID'si girin. Örneğin: `!complete_task 1`")

    def test_complete_task_command_negative_id(self):
        from bot import complete_task
        
        with patch('bot.get_task_by_id_db') as mock_get_task:
            mock_get_task.return_value = None
            
            asyncio.run(complete_task(self.mock_ctx, task_id=-1))
            
            mock_get_task.assert_called_once_with(-1)
            self.mock_ctx.send.assert_called_once_with("⚠️ `-1` ID'li görev bulunamadı.")

    def test_complete_task_command_failure(self):
        from bot import complete_task
        
        with patch('bot.get_task_by_id_db') as mock_get_task:
            mock_get_task.return_value = (1, "Task 1", 0)
            
            with patch('bot.complete_task_db') as mock_complete_task:
                mock_complete_task.return_value = False
                
                asyncio.run(complete_task(self.mock_ctx, task_id=1))
                
                mock_get_task.assert_called_once_with(1)
                mock_complete_task.assert_called_once_with(1)
                self.mock_ctx.send.assert_called_once_with("⚠️ `1` ID'li görev tamamlanamadı veya bulunamadı.")

    def test_command_error_handling(self):
        from bot import on_command_error
        from discord.ext import commands
        
        error = commands.CommandNotFound()
        
        asyncio.run(on_command_error(self.mock_ctx, error))
        
        self.mock_ctx.send.assert_called_once_with("❓ Bilinmeyen komut. Yardım için `!help` yazabilirsiniz.")

    def test_missing_argument_error_handling(self):
        from bot import on_command_error
        from discord.ext import commands
        
        error = commands.MissingRequiredArgument(Mock())
        self.mock_ctx.command.name = "test_command"
        
        asyncio.run(on_command_error(self.mock_ctx, error))
        
        self.mock_ctx.send.assert_called_once_with("⚠️ Eksik argüman. Komutun doğru kullanımı için `!help test_command` yazın.")

    def test_bad_argument_error_handling(self):
        from bot import on_command_error
        from discord.ext import commands
        
        error = commands.BadArgument()
        self.mock_ctx.command.name = "test_command"
        
        asyncio.run(on_command_error(self.mock_ctx, error))
        
        self.mock_ctx.send.assert_called_once_with("⚠️ Geçersiz argüman tipi. Komutun doğru kullanımı için `!help test_command` yazın.")

    def test_generic_error_handling(self):
        from bot import on_command_error
        
        error = Exception("Test error")
        
        asyncio.run(on_command_error(self.mock_ctx, error))
        
        self.mock_ctx.send.assert_called_once_with("Beklenmedik bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

if __name__ == '__main__':
    unittest.main() 