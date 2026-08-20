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
    perfumes = Perfume.objects.select_related('marca').order_by('-id')

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

    ia_identificado = None
    ia_resultados = []
    ia_erro = None
    ia_nome_pesquisado = ''

    if request.method == 'POST':
        ia_identificado, ia_resultados, ia_erro, ia_nome_pesquisado = _buscar_perfume_ia(request)

    context = {
        'perfumes': perfumes,
        'marcas': marcas,
        'genero_selecionado': genero,
        'marca_selecionada': marca_slug,
        'ia_identificado': ia_identificado,
        'ia_resultados': ia_resultados,
        'ia_erro': ia_erro,
        'ia_nome_pesquisado': ia_nome_pesquisado,
    }
    return render(request, 'core/colecao.html', context)


MAX_RESULTADOS = 3
# Nome do modelo Gemini usado para identificar perfumes. Se a Google descontinuar
# esse nome no futuro, basta trocar aqui (ou usar um alias tipo 'gemini-flash-latest').
GEMINI_MODEL = 'gemini-3.1-flash-lite'


def _catalogo_para_texto(catalogo):
    linhas = [
        f"{p.id} | {p.nome} | Marca: {p.marca.nome} | Genero: {p.get_genero_display()} | "
        f"Notas: {p.notas_saida or '-'}, {p.notas_coracao or '-'}, {p.notas_fundo or '-'}"
        for p in catalogo
    ]
    return "\n".join(linhas)


def _prompt_foto(catalogo):
    return (
        "Voce e um especialista em perfumes. Analise a foto enviada (frasco, caixa ou rotulo) e "
        "tente identificar a marca e o nome do perfume, mesmo que ele nao esteja na lista abaixo.\n\n"
        "Depois, escolha ate 3 perfumes da lista do CATALOGO abaixo que sejam mais parecidos em "
        "estilo olfativo com o perfume identificado na foto (considere as notas, o genero e o estilo).\n\n"
        "CATALOGO (formato: ID | Nome | Marca | Genero | Notas):\n"
        + _catalogo_para_texto(catalogo) +
        "\n\nResponda ESTRITAMENTE em JSON valido, sem nenhum texto antes ou depois, neste formato:\n"
        '{"identificado": "marca e nome do perfume identificado na foto, ou null se nao for possivel reconhecer", '
        '"similares_ids": [lista de ate 3 IDs do catalogo acima, do mais para o menos parecido]}'
    )


def _prompt_nome(nome_pesquisado, catalogo):
    return (
        "Voce e um especialista em perfumes. Um cliente esta procurando um perfume chamado "
        f'"{nome_pesquisado}".\n\n'
        "Com base no que voce sabe sobre esse perfume (notas olfativas, estilo, marca), escolha ate 3 "
        "perfumes da lista do CATALOGO abaixo que sejam mais parecidos em estilo olfativo com ele "
        "(considere as notas, o genero e o estilo).\n\n"
        "CATALOGO (formato: ID | Nome | Marca | Genero | Notas):\n"
        + _catalogo_para_texto(catalogo) +
        "\n\nResponda ESTRITAMENTE em JSON valido, sem nenhum texto antes ou depois, neste formato:\n"
        '{"identificado": "marca e nome do perfume que voce entendeu que o cliente procura, ou null se nao reconhecer", '
        '"similares_ids": [lista de ate 3 IDs do catalogo acima, do mais para o menos parecido]}'
    )


def _extrair_json(texto_resposta):
    texto = texto_resposta.strip()
    if texto.startswith('```'):
        texto = texto.strip('`')
        if '\n' in texto:
            _primeira_linha, texto = texto.split('\n', 1)
    import json
    return json.loads(texto)


def _buscar_perfume_ia(request):
    """Processa uma busca por foto ou nome enviada via POST e devolve
    (identificado, resultados, erro, nome_pesquisado)."""
    import os

    foto = request.FILES.get('foto')
    nome_pesquisado = (request.POST.get('nome') or '').strip()
    api_key = os.environ.get('GEMINI_API_KEY')

    if not foto and not nome_pesquisado:
        return None, [], None, nome_pesquisado

    if not api_key:
        return None, [], "A busca ainda não está disponível no momento. Fale com a gente pelo WhatsApp.", nome_pesquisado

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        catalogo = list(Perfume.objects.select_related('marca').all())
        model = genai.GenerativeModel(GEMINI_MODEL)

        if foto:
            from PIL import Image
            with Image.open(foto) as img:
                imagem = img.convert('RGB')
                imagem.thumbnail((768, 768))
                resposta = model.generate_content([_prompt_foto(catalogo), imagem])
        else:
            resposta = model.generate_content(_prompt_nome(nome_pesquisado, catalogo))

        dados = _extrair_json(resposta.text)
        identificado = dados.get('identificado') or None

        perfumes_por_id = {p.id: p for p in catalogo}
        ids_sugeridos = dados.get('similares_ids') or []
        resultados = [perfumes_por_id[i] for i in ids_sugeridos if i in perfumes_por_id][:MAX_RESULTADOS]

        erro = None
        if not identificado and not resultados:
            erro = "Não conseguimos identificar isso. Tente outra foto/nome ou fale com a gente pelo WhatsApp."

        return identificado, resultados, erro, nome_pesquisado
    except Exception:
        erro = "Não foi possível processar sua busca agora. Tente novamente em instantes ou fale com a gente pelo WhatsApp."
        return None, [], erro, nome_pesquisado