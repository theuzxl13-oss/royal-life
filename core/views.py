from django.shortcuts import render
from django.db.utils import ProgrammingError, OperationalError
from .models import Perfume, Campanha, Marca

def home(request):
    # Traz os perfumes cadastrados mais recentes primeiro (máximo 10)
    lancamentos = Perfume.objects.all().order_by('-id')[:10]

    # Busca a campanha ativa
    try:
        campanha_ativa = Campanha.objects.filter(ativa=True).first()
    except (ProgrammingError, OperationalError):
        campanha_ativa = None

    context = {
        'lancamentos': lancamentos,
        'campanha_ativa': campanha_ativa,
    }
    return render(request, 'core/home.html', context)


def colecao(request):
    # Ordena do mais recente para o mais antigo na coleção
    perfumes = Perfume.objects.all().order_by('-id')
    
    genero = request.GET.get('genero')
    marca_slug = request.GET.get('marca')

    if genero:
        perfumes = perfumes.filter(genero=genero)
    if marca_slug:
        perfumes = perfumes.filter(marca__slug=marca_slug)

    try:
        marcas = Marca.objects.all().order_by('nome')
    except (ProgrammingError, OperationalError):
        marcas = []

    context = {
        'perfumes': perfumes,
        'marcas': marcas,
        'genero_selecionado': genero,
        'marca_selecionada': marca_slug,
    }
    return render(request, 'core/colecao.html', context)


MAX_RESULTADOS = 3
# Nome do modelo Gemini usado para identificar perfumes. Se a Google descontinuar
# esse nome no futuro, basta trocar aqui.
GEMINI_MODEL = 'gemini-2.0-flash'


def _montar_prompt(catalogo):
    linhas = [
        f"{p.id} | {p.nome} | Marca: {p.marca.nome} | Genero: {p.get_genero_display()} | "
        f"Notas: {p.notas_saida or '-'}, {p.notas_coracao or '-'}, {p.notas_fundo or '-'}"
        for p in catalogo
    ]
    return (
        "Voce e um especialista em perfumes. Analise a foto enviada (frasco, caixa ou rotulo) e "
        "tente identificar a marca e o nome do perfume, mesmo que ele nao esteja na lista abaixo.\n\n"
        "Depois, escolha ate 3 perfumes da lista do CATALOGO abaixo que sejam mais parecidos em "
        "estilo olfativo com o perfume identificado na foto (considere as notas, o genero e o estilo).\n\n"
        "CATALOGO (formato: ID | Nome | Marca | Genero | Notas):\n"
        + "\n".join(linhas) +
        "\n\nResponda ESTRITAMENTE em JSON valido, sem nenhum texto antes ou depois, neste formato:\n"
        '{"identificado": "marca e nome do perfume identificado na foto, ou null se nao for possivel reconhecer", '
        '"similares_ids": [lista de ate 3 IDs do catalogo acima, do mais para o menos parecido]}'
    )


def busca_foto(request):
    resultados = []
    identificado = None
    erro = None

    if request.method == 'POST' and request.FILES.get('foto'):
        import os
        api_key = os.environ.get('GEMINI_API_KEY')

        if not api_key:
            erro = "A busca por foto ainda não está disponível no momento. Fale com a gente pelo WhatsApp."
        else:
            try:
                import json
                from PIL import Image
                import google.generativeai as genai

                genai.configure(api_key=api_key)

                with Image.open(request.FILES['foto']) as img:
                    imagem = img.convert('RGB')
                    imagem.thumbnail((768, 768))

                    catalogo = list(Perfume.objects.select_related('marca').all())
                    prompt = _montar_prompt(catalogo)

                    model = genai.GenerativeModel(GEMINI_MODEL)
                    resposta = model.generate_content([prompt, imagem])

                texto = resposta.text.strip()
                if texto.startswith('```'):
                    texto = texto.strip('`')
                    if '\n' in texto:
                        primeira_linha, texto = texto.split('\n', 1)

                dados = json.loads(texto)
                identificado = dados.get('identificado') or None

                perfumes_por_id = {p.id: p for p in catalogo}
                ids_sugeridos = dados.get('similares_ids') or []
                resultados = [perfumes_por_id[i] for i in ids_sugeridos if i in perfumes_por_id][:MAX_RESULTADOS]

                if not identificado and not resultados:
                    erro = "Não conseguimos identificar essa foto. Tente outra imagem ou fale com a gente pelo WhatsApp."
            except Exception:
                erro = "Não foi possível processar essa imagem agora. Tente novamente em instantes ou fale com a gente pelo WhatsApp."

    return render(request, 'core/busca_foto.html', {
        'resultados': resultados,
        'identificado': identificado,
        'erro': erro,
    })