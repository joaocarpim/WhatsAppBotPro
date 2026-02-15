import os
import time
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class WhatsAppBot:
    def __init__(self):
        self.driver = None
        self.base_dir = os.path.abspath(os.getcwd())
        self.session_dir = os.path.join(self.base_dir, "whatsapp_session")

    def limpar_sessao(self):
        """Remove sessão corrompida do WhatsApp"""
        try:
            import shutil
            if os.path.exists(self.session_dir):
                print("[INFO] Limpando sessão antiga...")
                shutil.rmtree(self.session_dir, ignore_errors=True)
                print("[INFO] Sessão limpa com sucesso")
                return True
        except Exception as e:
            print(f"[AVISO] Erro ao limpar sessão: {e}")
        return False

    def iniciar(self, headless=False):
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

        options = Options()
        if headless:
            options.add_argument("--headless=new")

        options.add_argument(f"--user-data-dir={self.session_dir}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            print("[SISTEMA] Inicializando Driver...")
            driver_path = ChromeDriverManager().install()

            service = Service(driver_path)
            if os.name == 'nt':
                service.creation_flags = subprocess.CREATE_NO_WINDOW

            self.driver = webdriver.Chrome(service=service, options=options)
            print("[SISTEMA] Acessando WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            return True

        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha ao iniciar: {e}")
            return False

    def aguardar_login(self):
        print("[LOGIN] Aguardando autenticação...")
        inicio = time.time()

        while (time.time() - inicio) < 120:
            try:
                if len(self.driver.find_elements(By.ID, "pane-side")) > 0:
                    return True
                if len(self.driver.find_elements(By.XPATH, "//header//img")) > 0:
                    return True
                if len(self.driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')) > 0:
                    return True
                time.sleep(1)
            except:
                time.sleep(1)
        return False

    def formatar_numero(self, numero):
        numero = re.sub(r"\D", "", numero)
        if len(numero) < 10:
            return None, "Número muito curto"
        if len(numero) > 15:
            return None, "Número muito longo"
        if len(numero) in [10, 11]:
            numero = "55" + numero
        return numero, "OK"

    def enviar(self, numero, mensagem):
        try:
            print(f"\n[ENVIO] Iniciando envio para: {numero}")

            # 1. Valida e Navega
            num_fmt, status = self.formatar_numero(numero)
            if not num_fmt:
                return False, status

            url = f"https://web.whatsapp.com/send?phone={num_fmt}"
            self.driver.get(url)

            # 2. Aguarda Chat Carregar
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
            except TimeoutException:
                invalid = self.driver.find_elements(
                    By.XPATH, '//div[contains(text(), "número de telefone")]|//div[contains(text(), "phone number")]')
                if invalid:
                    return False, "Número inválido/Sem Whats"
                return False, "Timeout (Internet/Whats lento)"

            time.sleep(1.5)

            # 3. ENVIA TEXTO
            if mensagem and mensagem.strip():
                box = self.driver.find_element(
                    By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')

                linhas = mensagem.split("\n")
                for i, linha in enumerate(linhas):
                    box.send_keys(linha)
                    if i < len(linhas) - 1:
                        ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(
                            Keys.ENTER).key_up(Keys.SHIFT).perform()

                time.sleep(0.5)
                try:
                    btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]')))
                    btn.click()
                except:
                    box.send_keys(Keys.ENTER)

                time.sleep(2)
                return True, "✅ Texto enviado"

            return True, "✅ Enviado com sucesso"

        except Exception as e:
            print(f"[ENVIO] ERRO: {e}")
            return False, f"❌ Erro: {str(e)}"

    def fechar(self):
        if self.driver:
            self.driver.quit()
