import urllib.parse
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class YTMusicPlayer:
    def __init__(self):
        self.driver = None

    def _initialize_browser(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")

        self.driver = uc.Chrome(
            options=options,
            headless=False,
            version_main=None
        )
        self.driver.get("https://music.youtube.com")
        time.sleep(3)

    def search_and_play(self, query):
        try:
            if not self.driver:
                self._initialize_browser()

            print("🔍 Buscando música...")
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://music.youtube.com/search?q={encoded_query}"
            self.driver.get(search_url)

            print("⌛ Esperando resultados de busca...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytmusic-card-shelf-renderer"))
            )

            print("▶️ Tentando clicar no botão play...")
            play_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ytmusic-card-shelf-renderer #play-button"))
            )
            play_button.click()
            time.sleep(2)
            return True

        except Exception as e:
            print(f"❌ Erro ao reproduzir música: {str(e)}")
            return False

    def pause_resume(self):
        """Pausa ou retoma a música usando a tecla Space"""
        if self.driver:
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.SPACE)
                time.sleep(1)
                return True
            except Exception as e:
                print(f"Erro ao pausar/retomar: {e}")
                return False

    def next_track(self):
        """Pula para a próxima música"""
        if self.driver:
            try:
                # Tentativa com novo seletor (YouTube Music atualizado)
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "ytmusic-player-bar .next-button"))
                )
                next_button.click()
                time.sleep(2)  # Aumente o tempo de espera
                return True
            except Exception as e:
                print(f"Erro ao avançar música (tentativa 1): {e}")
                try:
                    # Fallback para seletor alternativo
                    next_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "tp-yt-iron-icon.next-button"))
                    )
                    next_button.click()
                    time.sleep(2)
                    return True
                except Exception as e2:
                    print(f"Erro ao avançar música (tentativa 2): {e2}")
                    return False

    def close(self):
        if self.driver:
            self.driver.quit()
            print("🛑 Navegador fechado")