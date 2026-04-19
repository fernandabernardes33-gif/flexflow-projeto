from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from fastapi.responses import StreamingResponse
from io import BytesIO
from datetime import datetime


def _st(name, **kw):
    return ParagraphStyle(name, **kw)


AZUL   = colors.HexColor('#2563EB')
ESCURO = colors.HexColor('#1B2B4B')
CINZA  = colors.HexColor('#F4F6FA')
BORDA  = colors.HexColor('#E5E7EB')
CINZA_TEXTO = colors.HexColor('#555555')

RODAPE_LGPD = (
    "Este documento contém dados pessoais protegidos pela Lei Geral de "
    "Proteção de Dados (LGPD — Lei nº 13.709/2018). As informações aqui "
    "presentes são de uso exclusivo para prestação do serviço descrito e "
    "não devem ser compartilhadas com terceiros sem autorização do titular."
)


def _cabecalho(el, subtitulo):
    el.append(Paragraph("AUssistencia",
        _st('h1', fontSize=20, fontName='Helvetica-Bold',
            textColor=AZUL, alignment=TA_CENTER, spaceAfter=2)))
    el.append(Paragraph("Assistencia Tecnica de Informatica",
        _st('h2', fontSize=10, fontName='Helvetica',
            textColor=CINZA_TEXTO, alignment=TA_CENTER, spaceAfter=12)))
    el.append(HRFlowable(width="100%", thickness=2, color=AZUL, spaceAfter=12))
    el.append(Paragraph(subtitulo,
        _st('sub', fontSize=14, fontName='Helvetica-Bold',
            textColor=ESCURO, spaceAfter=10)))


def _rodape(el):
    el.append(Spacer(1, 0.8*cm))
    el.append(HRFlowable(width="100%", thickness=0.5, color=BORDA, spaceAfter=6))
    el.append(Paragraph(RODAPE_LGPD,
        _st('lgpd', fontSize=7, fontName='Helvetica',
            textColor=colors.grey, alignment=TA_CENTER, leading=10)))
    el.append(Spacer(1, 4))
    el.append(Paragraph(
        f"Documento gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')} "
        "| AUssistencia — Assistencia Tecnica de Informatica",
        _st('footer', fontSize=7, fontName='Helvetica',
            textColor=colors.grey, alignment=TA_CENTER)))


def _tabela_itens(itens):
    lbl = _st('lbl', fontSize=9, fontName='Helvetica-Bold')
    val = _st('val', fontSize=9, fontName='Helvetica')
    cab = [[
        Paragraph("Descricao", _st('th', fontSize=9, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph("Tipo",      _st('th2', fontSize=9, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph("Qtd",       _st('thc', fontSize=9, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_CENTER)),
        Paragraph("Valor Unit.", _st('thr', fontSize=9, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_RIGHT)),
        Paragraph("Subtotal",   _st('thr2', fontSize=9, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_RIGHT)),
    ]]
    linhas = []
    for item in itens:
        sub = item.get('quantidade', 1) * item.get('valor_unitario', 0)
        linhas.append([
            Paragraph(str(item.get("descricao", "")), val),
            Paragraph(str(item.get("tipo", "Servico")), val),
            Paragraph(str(item.get("quantidade", 1)),
                _st('c', fontSize=9, fontName='Helvetica', alignment=TA_CENTER)),
            Paragraph(f"R$ {item.get('valor_unitario', 0):.2f}",
                _st('r', fontSize=9, fontName='Helvetica', alignment=TA_RIGHT)),
            Paragraph(f"R$ {sub:.2f}",
                _st('r2', fontSize=9, fontName='Helvetica', alignment=TA_RIGHT)),
        ])
    tabela = Table(cab + linhas, colWidths=[7*cm, 2.5*cm, 2*cm, 2.75*cm, 2.75*cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, CINZA]),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDA),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return tabela


def _bloco_total(valor_total):
    t = Table([[
        Paragraph("TOTAL:", _st('tl', fontSize=12, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph(f"R$ {valor_total:.2f}",
            _st('tv', fontSize=12, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_RIGHT)),
    ]], colWidths=[13.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ESCURO),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def gerar_pdf_os(os_data: dict) -> StreamingResponse:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm)
    el = []
    lbl = _st('lbl', fontSize=9, fontName='Helvetica-Bold')
    val = _st('val', fontSize=9, fontName='Helvetica')

    _cabecalho(el, f"ORDEM DE SERVICO N {str(os_data.get('id', '')).zfill(4)}")

    # Info OS
    t_info = Table([
        [Paragraph("Data Abertura:", lbl),
         Paragraph(str(os_data.get("data_abertura", "")), val),
         Paragraph("Previsao Entrega:", lbl),
         Paragraph(str(os_data.get("data_previsao", "Nao informada")), val)],
        [Paragraph("Status:", lbl),
         Paragraph(str(os_data.get("status", "")), val),
         Paragraph("", lbl), Paragraph("", val)],
    ], colWidths=[4*cm, 5.5*cm, 4*cm, 3.5*cm])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CINZA),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDA),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    el.append(t_info)
    el.append(Spacer(1, 0.4*cm))

    # Cliente — LGPD: apenas nome e telefone
    el.append(Paragraph("Dados do Cliente",
        _st('sec', fontSize=11, fontName='Helvetica-Bold', textColor=ESCURO, spaceBefore=6, spaceAfter=6)))
    t_cli = Table([
        [Paragraph("Nome:", lbl), Paragraph(str(os_data.get("cliente_nome", "")), val)],
        [Paragraph("Telefone:", lbl), Paragraph(str(os_data.get("cliente_telefone", "Nao informado")), val)],
    ], colWidths=[4*cm, 13*cm])
    t_cli.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDA),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, BORDA),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    el.append(t_cli)
    el.append(Spacer(1, 0.4*cm))

    # Problema
    el.append(Paragraph("Problema Relatado",
        _st('sec2', fontSize=11, fontName='Helvetica-Bold', textColor=ESCURO, spaceBefore=6, spaceAfter=6)))
    t_prob = Table([[Paragraph(str(os_data.get("descricao_problema", "")),
        _st('prob', fontSize=9, fontName='Helvetica', leading=14))]], colWidths=[17*cm])
    t_prob.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDA),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    el.append(t_prob)
    el.append(Spacer(1, 0.4*cm))

    # Itens
    el.append(Paragraph("Itens / Servicos Realizados",
        _st('sec3', fontSize=11, fontName='Helvetica-Bold', textColor=ESCURO, spaceBefore=6, spaceAfter=6)))
    itens = os_data.get("itens", [])
    if itens:
        el.append(_tabela_itens(itens))
    else:
        el.append(Paragraph("Nenhum item registrado.",
            _st('vazio', fontSize=9, fontName='Helvetica', textColor=colors.grey)))

    el.append(Spacer(1, 0.3*cm))
    el.append(_bloco_total(os_data.get('valor_total', 0)))

    # Assinaturas
    el.append(Spacer(1, 1.5*cm))
    t_ass = Table([[
        Paragraph("_______________________\nAssinatura do Cliente",
            _st('ass', fontSize=8, fontName='Helvetica', alignment=TA_CENTER)),
        Paragraph("_______________________\nResponsavel Tecnico",
            _st('ass2', fontSize=8, fontName='Helvetica', alignment=TA_CENTER)),
    ]], colWidths=[8.5*cm, 8.5*cm])
    el.append(t_ass)

    _rodape(el)

    doc.build(el)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition":
            f"attachment; filename=OS_{str(os_data.get('id', '')).zfill(4)}.pdf"}
    )


def gerar_pdf_orcamento(orc_data: dict) -> StreamingResponse:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm)
    el = []
    lbl = _st('lbl', fontSize=9, fontName='Helvetica-Bold')
    val = _st('val', fontSize=9, fontName='Helvetica')

    _cabecalho(el, f"ORCAMENTO N {str(orc_data.get('id', '')).zfill(4)}")

    t_info = Table([
        [Paragraph("Data:", lbl), Paragraph(str(orc_data.get("data", "")), val),
         Paragraph("Validade:", lbl), Paragraph(str(orc_data.get("validade", "")), val)],
        [Paragraph("Status:", lbl), Paragraph(str(orc_data.get("status", "")), val),
         Paragraph("", lbl), Paragraph("", val)],
    ], colWidths=[4*cm, 5.5*cm, 4*cm, 3.5*cm])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CINZA),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDA),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    el.append(t_info)
    el.append(Spacer(1, 0.4*cm))

    el.append(Paragraph("Cliente",
        _st('sec', fontSize=11, fontName='Helvetica-Bold', textColor=ESCURO, spaceBefore=6, spaceAfter=6)))
    t_cli = Table([
        [Paragraph("Nome:", lbl), Paragraph(str(orc_data.get("cliente_nome", "")), val)],
    ], colWidths=[4*cm, 13*cm])
    t_cli.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, BORDA),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    el.append(t_cli)
    el.append(Spacer(1, 0.4*cm))

    el.append(Paragraph("Itens do Orcamento",
        _st('sec2', fontSize=11, fontName='Helvetica-Bold', textColor=ESCURO, spaceBefore=6, spaceAfter=6)))
    itens = orc_data.get("itens", [])
    if itens:
        el.append(_tabela_itens(itens))
    else:
        el.append(Paragraph("Nenhum item registrado.",
            _st('vazio', fontSize=9, fontName='Helvetica', textColor=colors.grey)))

    el.append(Spacer(1, 0.3*cm))
    el.append(_bloco_total(orc_data.get('valor_total', 0)))

    _rodape(el)

    doc.build(el)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition":
            f"attachment; filename=Orcamento_{str(orc_data.get('id', '')).zfill(4)}.pdf"}
    )
