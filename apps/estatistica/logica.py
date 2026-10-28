import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
import io
import urllib, base64
from apps.cerebro.models import Consulta
from datetime import datetime, date
from django.utils import timezone


def tabela(ano=None):
    if ano is None:
        ano = datetime.now().year

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    dados_mensais = []
    agora = timezone.now()

    for mes in range(1, 13):
        data_do_mes = date(ano, mes, 1).isoformat()
        consulta_mes = Consulta.objects.filter(
            data_hora__year=ano, data_hora__month=mes, data_hora__lt=agora
        )
        ofertada = consulta_mes.filter(
            consulta_status__in=[
                "consulta_disponivel",
                "agendada",
                "na_unidade",
                "faltou",
                "compareceu",
            ]
        ).count()
        agendada = consulta_mes.filter(
            consulta_status__in=["agendada", "na_unidade", "faltou", "compareceu"]
        ).count()
        compareceu = consulta_mes.filter(consulta_status="compareceu").count()
        perda_primaria = ofertada - compareceu
        relacao = ((ofertada - agendada) / ofertada) * 100 if ofertada > 0 else 0
        faltou_porcentagem = (
            ((agendada - compareceu) / agendada) * 100 if agendada > 0 else 0
        )
        faltou = agendada - compareceu
        taxa_ocupacao = (
            ((ofertada - perda_primaria) / ofertada) * 100 if ofertada > 0 else 0
        )
        dados_mensais.append(
            {
                "data": data_do_mes,
                "NumMes": mes,
                "meses": meses[mes - 1],
                "agendada": agendada,
                "ofertada": ofertada,
                "compareceu": compareceu,
                "perda_primaria": perda_primaria,
                "relacao": relacao,
                "faltou_porcentagem": faltou_porcentagem,
                "faltou": faltou,
                "taxa_ocupacao": taxa_ocupacao,
            }
        )

    total_ofertada = sum(i["ofertada"] for i in dados_mensais)
    total_agendada = sum(i["agendada"] for i in dados_mensais)
    total_compareceu = sum(i["compareceu"] for i in dados_mensais)
    total_faltou = sum(i["faltou"] for i in dados_mensais)
    total_perda_primaria = sum(i["perda_primaria"] for i in dados_mensais)
    total_relacao = (
        ((total_ofertada - total_agendada) / total_ofertada) * 100
        if total_ofertada > 0
        else 0
    )
    total_faltou_porcentagem = (
        (total_faltou / total_agendada) * 100 if total_agendada > 0 else 0
    )
    total_taxa_ocupacao = (
        ((total_ofertada - total_perda_primaria) / total_ofertada) * 100
        if total_ofertada > 0
        else 0
    )
    total_dados = {
        "meses": "total anual",
        "ofertada": total_ofertada,
        "agendada": total_agendada,
        "compareceu": total_compareceu,
        "faltou": total_faltou,
        "perda_primaria": total_perda_primaria,
        "relacao": total_relacao,
        "faltou_porcentagem": total_faltou_porcentagem,
        "taxa_ocupacao": total_taxa_ocupacao,
    }
    return {"mensal": dados_mensais, "total_dados": total_dados}


def converter_grafico():
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    string_imagem = base64.b64encode(buffer.read())
    grafico = urllib.parse.quote(string_imagem)
    plt.close()
    return grafico


def grafico_de_barra(
    dados_mensais, data_key, y_label, title, color, is_percentage=False
):
    dados = [i[data_key] for i in dados_mensais]
    meses = [i["meses"] for i in dados_mensais]
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f7f5f0")
    barra = ax.bar(meses, dados, color=color)
    ax.set_xlabel("MESES")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")

    if is_percentage:
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.0f%%"))
        ax.set_ylim(0, 100)
        formato_texto = lambda altura: f"{altura:.0f}%"
    else:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylim(bottom=0)
        formato_texto = lambda altura: f"{int(altura)}"

    if dados:
        max_val = max(dados)
        if max_val > 0:
            ax.set_ylim(top=max_val * 1.1)
        elif not is_percentage:
            ax.set_ylim(top=10)

    for i in barra:
        altura = i.get_height()
        if altura > 0:
            ax.text(
                i.get_x() + i.get_width() / 2.0,
                altura,
                formato_texto(altura),
                ha="center",
                va="bottom",
            )

    return converter_grafico()


def grafico_agendada(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="agendada",
        y_label="CONSULTAS AGENDADAS",
        title="QUANTIDADE MENSAL DE CONSULTAS AGENDADAS",
        color="#5bce5b",
        is_percentage=False,
    )


def grafico_compareceu(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="compareceu",
        y_label="PACIENTES",
        title="QUANTIDADE MENSAL DE PRESENÇA DOS PACIENTES NAS CONSULTAS",
        color="#5bce5b",
        is_percentage=False,
    )


def grafico_faltou(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="faltou",
        y_label="PACIENTES",
        title="QUANTIDADE MENSAL DE FALTAS DOS PACIENTES NAS CONSULTAS",
        color="#da1414",
        is_percentage=False,
    )


def grafico_absenteismo(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="faltou_porcentagem",
        y_label="ABSENTEÍSMO (%)",
        title="ABSENTEÍSMO MENSAL",
        color="#da1414",
        is_percentage=True,
    )


def grafico_ofertada(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="ofertada",
        y_label="CONSULTAS OFERTADAS",
        title="QUANTIDADE MENSAL DE CONSULTAS OFERTADAS",
        color="#4749d8",
        is_percentage=False,
    )


def grafico_perda_primaria(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="perda_primaria",
        y_label="PERDA PRIMÁRIA",
        title="QUANTIDADE MENSAL DE PERDA PRIMÁRIA",
        color="#4749d8",
        is_percentage=False,
    )


def grafico_relacao(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="relacao",
        y_label="RELAÇÃO (%)",
        title="RELAÇÃO MENSAL",
        color="#4749d8",
        is_percentage=True,
    )


def grafico_taxa_ocupacao(dados_mensais):
    return grafico_de_barra(
        dados_mensais,
        data_key="taxa_ocupacao",
        y_label="TAXA DE OCUPAÇÃO (%)",
        title="QUANTIDADE MENSAL DE TAXA DE OCUPAÇÃO",
        color="#4749d8",
        is_percentage=True,
    )


def grafico_total(total_dados):
    agendada = total_dados["agendada"]
    compareceu = total_dados["compareceu"]
    faltou = total_dados["faltou"]
    valores = [compareceu, faltou]
    categorias = ["Realizadas", "Faltas"]
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f7f5f0")
    barra = ax.bar(categorias, valores, color=["#5bce5b", "#da1414"])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("STATUS DA CONSULTA")
    ax.set_ylabel("CONSULTAS AGENDADAS (ANUAL)")
    ax.set_title("PROPORÇÃO DE PRESENÇA VS. FALTAS (ANUAL)")
    ax.axhline(
        y=agendada,
        color="#00008B",
        linestyle="--",
        label=f"Consultas Agendadas ({agendada})",
    )
    limite_max = max(agendada, compareceu)
    ax.set_ylim(0, limite_max * 1.1)
    ax.legend()

    for i in barra:
        altura = i.get_height()
        if altura > 0:
            ax.text(
                i.get_x() + i.get_width() / 2.0,
                altura,
                f"{int(altura)}",
                ha="center",
                va="bottom",
            )

    return converter_grafico()


def grafico_pizza(dados_mensais):
    compareceu = sum(i["compareceu"] for i in dados_mensais)
    faltou = sum(i["faltou"] for i in dados_mensais)

    if compareceu == 0 and faltou == 0:
        return None

    plt.figure(figsize=(7, 4))
    plt.pie(
        [compareceu, faltou],
        explode=(0, 0.1),
        labels=["Realizadas", "Faltas"],
        colors=["#5bce5b", "#da1414"],
        autopct="%1.1f%%",
        startangle=100,
    )
    plt.title("PROPORÇÃO DE PRESENÇA VS. FALTAS (ANUAL)")
    plt.axis("equal")
    return converter_grafico()
