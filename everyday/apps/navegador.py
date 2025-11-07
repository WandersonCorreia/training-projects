from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from apps.helpers import log


def marcar_ponto():
    ''' Abre o navegador, acessa o portal RH e marca o ponto.'''
    driver = webdriver.Edge()  # ou Chrome, Firefox
    driver.get("https://portalxxxxx.xxxxx.com")

    # Espera até que o botão esteja visível
    try:
        botao_mponto = driver.find_element(
            By.XPATH, "//div[span[text()='Marcar Ponto']]")
        botao_mponto.click()
        log("Botão 'Marcar Ponto' clicado com sucesso.")
        time.sleep(2)  # Aguarda carregamento do modal

        # Trocando o foco para a nova janela
        original_window = driver.current_window_handle
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        novas_janelas = driver.window_handles

        for janela in novas_janelas:
            if janela != original_window:
                driver.switch_to.window(janela)

        botao_cponto = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "Button1"))
        )
        botao_cponto.click()
        log("Ponto marcado com sucesso.")

    except Exception as e:
        log("Erro ao marcar ponto:", e)

    finally:
        time.sleep(5)
        driver.quit()
