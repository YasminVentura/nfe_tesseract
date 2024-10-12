import cv2
import pytesseract
import pandas as pd

def desenhar_retangulo(event, x, y, flags, param):
    global x_inicial, y_inicial, desenhando, imagem_original

    if event == cv2.EVENT_LBUTTONDOWN: #ve se o mouse ta ativo
        desenhando = True
        x_inicial, y_inicial = x, y

    elif event == cv2.EVENT_MOUSEMOVE: #reconhece o movimento
        if desenhando:
            imagem_copy = imagem_original.copy()
            cv2.rectangle(imagem_copy, (x_inicial, y_inicial), (x, y), (0, 255, 0), 2)
            cv2.imshow("Selecione as areas de interesse", imagem_copy)

    elif event == cv2.EVENT_LBUTTONUP: #ve se o mouse ta inativo
        desenhando = False
        cv2.rectangle(imagem_original, (x_inicial, y_inicial), (x, y), (0, 255, 0), 2)
        coordenadas.append((x_inicial, y_inicial, x, y))
        cv2.imshow("Selecione as areas de interesse", imagem_original)


x_inicial, y_inicial = -1, -1
desenhando = False
coordenadas = []

# variaveis para armazenar os daods extraídos
emitente = ""
cnpj = ""
data_emissao = ""
valor_total = ""

imagem_original = cv2.imread('nfe/amz.png')

cv2.namedWindow("Selecione as areas de interesse")
cv2.setMouseCallback("Selecione as areas de interesse", desenhar_retangulo) #ferramenta do opencv q gera uma janela

cv2.imshow("Selecione as areas de interesse", imagem_original)
cv2.waitKey(0)
cv2.destroyAllWindows()

variaveis = ['emitente', 'cnpj', 'data_emissao', 'valor_total']


for i, (x_inicial, y_inicial, x_final, y_final) in enumerate(coordenadas):
    regiao_texto = imagem_original[y_inicial:y_final, x_inicial:x_final]

    texto_detectado = pytesseract.image_to_string(regiao_texto).strip() #tesseract

    #passa a info extraida para a variavel correspondente
    if i < len(variaveis):
        if variaveis[i] == 'emitente':
            emitente = texto_detectado
        elif variaveis[i] == 'cnpj':
            cnpj = texto_detectado
        elif variaveis[i] == 'data_emissao':
            data_emissao = texto_detectado
        elif variaveis[i] == 'valor_total':
            valor_total = texto_detectado


print(f"Emitente: {emitente}")
print(f"CNPJ: {cnpj}")
print(f"Data de Emissão: {data_emissao}")
print(f"Valor Total: {valor_total}")

dados = {
    "Emitente": [emitente],
    "CNPJ": [cnpj],
    "Data de Emissão": [data_emissao],
    "Valor": [valor_total]
}

df = pd.DataFrame(dados)
df.to_csv('dadosextraidos.csv', mode='a', header=False, index=False, encoding='utf-8')
