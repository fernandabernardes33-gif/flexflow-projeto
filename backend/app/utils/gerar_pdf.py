from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from fastapi.responses import StreamingResponse
from io import BytesIO
from datetime import datetime


def gerar_pdf_os(os_data: dict) -> StreamingResponse:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elementos = []

    titulo_style = ParagraphStyle('titulo', fontSize=16, alignment=TA_CENTER,
                                   spaceAfter=12, fontName='Helvetica-Bold')
    elementos.append(Paragraph("AUssistencia - Ordem de Servico", titulo_style))
    elementos.append(Spacer(1, 0.5*cm))

    dados = [
        ["N OS:", str(os_data.get("id", ""))],
        ["Data de Abertura:", str(os_data.get("data_abertura", ""))],
        ["Previsao de Entrega:", str(os_data.get("data_previsao", ""))],
        ["Status:", str(os_data.get("status", ""))],
        ["Cliente:", str(os_data.get("cliente_nome", ""))],
        ["Problema Relatado:", str(os_data.get("descricao_problema", ""))],
    ]
    tabela_info = Table(dados, colWidths=[5*cm, 12*cm])
    tabela_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elementos.append(tabela_info)
    elementos.append(Spacer(1, 0.5*cm))

    elementos.append(Paragraph("Itens", ParagraphStyle('subtitulo', fontSize=12,
                                fontName='Helvetica-Bold', spaceAfter=6)))
    itens = os_data.get("itens", [])
    if itens:
        cabecalho = [["Descricao", "Qtd", "Valor Unit.", "Subtotal"]]
        linhas = [[
            item.get("descricao", ""),
            str(item.get("quantidade", 1)),
            f"R$ {item.get('valor_unitario', 0):.2f}",
            f"R$ {item.get('subtotal', 0):.2f}",
        ] for item in itens]
        tabela_itens = Table(cabecalho + linhas, colWidths=[9*cm, 2*cm, 3*cm, 3*cm])
        tabela_itens.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6FA')]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elementos.append(tabela_itens)

    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(Paragraph(
        f"Total: R$ {os_data.get('valor_total', 0):.2f}",
        ParagraphStyle('total', fontSize=12, alignment=TA_LEFT, fontName='Helvetica-Bold')))
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph(
        f"Documento gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
        ParagraphStyle('rodape', fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))

    doc.build(elementos)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=OS_{os_data.get('id', '')}.pdf"}
    )


def gerar_pdf_orcamento(orc_data: dict) -> StreamingResponse:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elementos = []

    titulo_style = ParagraphStyle('titulo', fontSize=16, alignment=TA_CENTER,
                                   spaceAfter=12, fontName='Helvetica-Bold')
    elementos.append(Paragraph("AUssistencia - Orcamento", titulo_style))
    elementos.append(Spacer(1, 0.5*cm))

    dados = [
        ["N Orcamento:", str(orc_data.get("id", ""))],
        ["Data:", str(orc_data.get("data", ""))],
        ["Validade:", str(orc_data.get("validade", ""))],
        ["Status:", str(orc_data.get("status", ""))],
        ["Cliente:", str(orc_data.get("cliente_nome", ""))],
    ]
    tabela_info = Table(dados, colWidths=[5*cm, 12*cm])
    tabela_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela_info)
    elementos.append(Spacer(1, 0.5*cm))

    itens = orc_data.get("itens", [])
    if itens:
        cabecalho = [["Descricao", "Qtd", "Valor Unit.", "Subtotal"]]
        linhas = [[
            i.get("descricao", ""), str(i.get("quantidade", 1)),
            f"R$ {i.get('valor_unitario', 0):.2f}", f"R$ {i.get('subtotal', 0):.2f}"
        ] for i in itens]
        tabela_itens = Table(cabecalho + linhas, colWidths=[9*cm, 2*cm, 3*cm, 3*cm])
        tabela_itens.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elementos.append(tabela_itens)

    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(Paragraph(
        f"Total: R$ {orc_data.get('valor_total', 0):.2f}",
        ParagraphStyle('total', fontSize=12, fontName='Helvetica-Bold')))
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph(
        f"Documento gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}",
        ParagraphStyle('rodape', fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))

    doc.build(elementos)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Orcamento_{orc_data.get('id', '')}.pdf"}
    )
