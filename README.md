# TaskMorph - README

O **TaskMorph** é um pacote Python desenvolvido para automatizar interações com o navegador, com foco em testes e automação de tarefas. Ele utiliza a biblioteca `Selenium` para manipulação do navegador e `pyautogui` para interações baseadas em imagens ou coordenadas na tela.

## Funcionalidades

### 1. Gerenciamento de Driver
- **start_driver()**: Inicializa o driver do navegador com opções configuráveis.
- **close_driver()**: Fecha o driver e encerra a sessão do navegador.
  
### 2. Busca de Elementos
- **find_element()**: Encontra um único elemento na página com base em um localizador.
- **find_elements()**: Encontra múltiplos elementos na página com base em um localizador.
- **find_element_clickable()**: Encontra um elemento clicável e o retorna.
- **find_element_or_none()**: Encontra um elemento ou retorna `None` se não for encontrado.

### 3. Interação com IFrames
- **change_iframe()**: Muda para um iframe específico ou volta para o contexto principal.

### 4. Logs e Execução de Scripts
- **get_all_headers()**: Retorna os cabeçalhos de rede da página.
- **get_performance_logs()**: Retorna os logs de desempenho da página.
- **get_console_logs()**: Retorna os logs do console do navegador.
- **execute_script()**: Executa um script JavaScript no navegador.
- **execute_async_script()**: Executa um script assíncrono no navegador.

### 5. Scroll e Armazenamento Local
- **scroll_page()**: Realiza o scroll da página para cima ou para baixo.
- **get_local_storage()**: Retorna os itens do armazenamento local do navegador.
- **set_local_storage()**: Define um valor no armazenamento local.

### 6. Alertas
- **accept_alert()**: Aceita um alerta na página.
- **dismiss_alert()**: Rejeita um alerta na página.

### 7. Captura de Tela
- **capture_screenshot()**: Captura uma captura de tela da página e salva em um arquivo.

### 8. Localização e Interação com Imagens
- **locate_image()**: Localiza uma imagem na tela usando `pyautogui`.
- **navigate_and_interact()**: Localiza uma imagem na tela e realiza uma ação como 'click', 'close', ou 'double_click'.
  
### 9. Interação com a Tela
- **center_mouse_and_click()**: Move o mouse para o centro da tela e opcionalmente clica.

## Requisitos

Para utilizar o pacote **TaskMorph**:

```bash
pip install TaskMorph
```

Caso queria usar as funções de `localização` e `interação com a tela` recomendo que **instale**:

- `pyautogui`: Para interações baseadas em imagens ou coordenadas.
- `opencv-python`: Necessário para o `pyautogui` funcionar corretamente.

```bash
pip install pyautogui opencv-python
```

## Como Usar

1. **Inicializando o Driver:**

```python
from TaskMorph.morph import TaskMorph

# Inicializa o driver com opções configuradas
driver = TaskMorph.start_driver(options=options, driver_path="caminho/do/driver")

# Realiza tarefas no navegador...
```

2. **Buscando Elementos:**

```python
element = TaskMorph.find_element(by='xpath', value='//div[@id="elemento"]')
```

3. **Interação com IFrames:**

```python
TaskMorph.change_iframe(by='id', value='iframe_id')
```

4. **Captura de Tela:**

```python
TaskMorph.capture_screenshot(filename="screenshot.png", download_path="/caminho/diretorio")
```

5. **Localização e Interação com Imagens:**

```python
TaskMorph.navigate_and_interact(image='caminho/da/imagem', action='click')
```

6. **Interação com a Tela:**

```python
TaskMorph.center_mouse_and_click()
```
