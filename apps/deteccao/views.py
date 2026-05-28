from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from .models import Ocorrencia, Alerta
from .serializers import OcorrenciaSerializer, AlertaSerializer
from .services import processar_camera, gerar_alerta
from apps.cameras.models import Camera
import json
import base64
import uuid
import os


class OcorrenciaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

    def get_queryset(self):
        queryset = Ocorrencia.objects.all()
        camera_id = self.request.query_params.get('camera')
        tipo = self.request.query_params.get('tipo')
        status_param = self.request.query_params.get('status')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    @action(detail=False, methods=['post'])
    def processar(self, request):
        camera_id = request.data.get('camera_id')
        try:
            camera = Camera.objects.get(id=camera_id, ativa=True)
            processar_camera(camera)
            return Response({'mensagem': 'Camera processada com sucesso'})
        except Camera.DoesNotExist:
            return Response({'erro': 'Camera nao encontrada'}, status=404)


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

    def get_queryset(self):
        queryset = Alerta.objects.all()
        camera_id = self.request.query_params.get('camera')
        nivel = self.request.query_params.get('nivel')
        reconhecido = self.request.query_params.get('reconhecido')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        if nivel:
            queryset = queryset.filter(nivel=nivel)
        if reconhecido is not None:
            queryset = queryset.filter(reconhecido=reconhecido == 'true')
        return queryset

    @action(detail=True, methods=['patch'])
    def reconhecer(self, request, pk=None):
        from apps.authentication.utils import registrar_log
        alerta = self.get_object()
        alerta.reconhecido = True
        alerta.reconhecido_em = timezone.now()
        alerta.save()
        registrar_log(request, 'reconhecer_alerta', f'Alerta {alerta.id} da camera {alerta.camera.nome} reconhecido')
        return Response(AlertaSerializer(alerta).data)

    @action(detail=False, methods=['get'])
    def nao_reconhecidos(self, request):
        alertas = Alerta.objects.filter(reconhecido=False)
        return Response(AlertaSerializer(alertas, many=True).data)


@csrf_exempt
@require_POST
def receber_deteccao_api(request):
    try:
        dados = json.loads(request.body)

        camera_id = dados.get('camera_id')
        tipo = dados.get('tipo')
        status_ocorrencia = dados.get('status_ocorrencia')
        pessoas_detectadas = dados.get('pessoas_detectadas', 0)
        epis_ausentes = dados.get('epis_ausentes', [])
        frame_b64 = dados.get('frame_b64', '')
        status_camera = dados.get('status_camera', 'online')

        camera = Camera.objects.get(id=camera_id)
        camera.status = status_camera
        camera.save()



        return JsonResponse({'status': 'ok', 'ocorrencia_id': ocorrencia.id})

    except Camera.DoesNotExist:
        return JsonResponse({'erro': 'Camera nao encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gerar_relatorio_pdf(request):
    from apps.authentication.utils import registrar_log
    registrar_log(request, 'gerar_relatorio', f'Relatorio PDF gerado por {request.user.username}')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_guardiao_epi.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    elementos = []

    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Heading1'], fontSize=18,
        textColor=colors.HexColor('#003050'), spaceAfter=0.5*cm
    )
    subtitulo_style = ParagraphStyle(
        'Subtitulo', parent=styles['Normal'], fontSize=10,
        textColor=colors.HexColor('#64748B'), spaceAfter=1*cm
    )
    secao_style = ParagraphStyle(
        'Secao', parent=styles['Heading2'], fontSize=12,
        textColor=colors.HexColor('#003050'), spaceBefore=0.5*cm, spaceAfter=0.3*cm
    )

    elementos.append(Paragraph('Guardiao EPI', titulo_style))
    elementos.append(Paragraph(
        f'Relatorio de Monitoramento gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}',
        subtitulo_style
    ))

    cameras = Camera.objects.filter(ativa=True)
    ocorrencias = Ocorrencia.objects.all().order_by('-criado_em')
    alertas = Alerta.objects.all()

    total = ocorrencias.count()
    conformes = ocorrencias.filter(status='conforme').count()
    nao_conformes = ocorrencias.filter(tipo='epi_ausente').count()
    taxa = round((conformes / total) * 100, 1) if total > 0 else 0

    elementos.append(Paragraph('Resumo Geral', secao_style))

    dados_resumo = [
        ['Indicador', 'Valor'],
        ['Total de Ocorrencias', str(total)],
        ['Conformes', str(conformes)],
        ['Nao Conformes', str(nao_conformes)],
        ['Taxa de Conformidade', f'{taxa}%'],
        ['Total de Alertas', str(alertas.count())],
        ['Alertas Pendentes', str(alertas.filter(reconhecido=False).count())],
        ['Cameras Ativas', str(cameras.count())],
    ]

    tabela_resumo = Table(dados_resumo, colWidths=[10*cm, 6*cm])
    tabela_resumo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003050')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 0.5*cm))

    elementos.append(Paragraph('Ocorrencias de EPI Ausente', secao_style))

    ocorrencias_epi = Ocorrencia.objects.filter(tipo='epi_ausente').order_by('-criado_em')[:20]
    TRADUCAO = {
        'no helmet': 'sem capacete', 'no gloves': 'sem luvas',
        'no goggles': 'sem oculos', 'no vest': 'sem colete', 'no shoes': 'sem botina'
    }

    dados_epi = [['Data/Hora', 'Camera', 'EPIs Ausentes', 'Pessoas']]
    for o in ocorrencias_epi:
        epis = ', '.join([TRADUCAO.get(e, e) for e in o.epis_ausentes])
        dados_epi.append([o.criado_em.strftime('%d/%m/%Y %H:%M'), o.camera.nome, epis, str(o.pessoas_detectadas)])

    tabela_epi = Table(dados_epi, colWidths=[4*cm, 4*cm, 6*cm, 3*cm])
    tabela_epi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003050')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FEE2E2'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela_epi)
    elementos.append(Spacer(1, 0.5*cm))

    elementos.append(Paragraph('Falhas de Equipamento', secao_style))

    ocorrencias_falha = Ocorrencia.objects.filter(tipo='equipment_fault').order_by('-criado_em')[:10]
    dados_falha = [['Data/Hora', 'Camera', 'Status']]
    for o in ocorrencias_falha:
        dados_falha.append([o.criado_em.strftime('%d/%m/%Y %H:%M'), o.camera.nome, 'Camera Offline'])

    tabela_falha = Table(dados_falha, colWidths=[5*cm, 6*cm, 6*cm])
    tabela_falha.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003050')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FEF3C7'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela_falha)

    doc.build(elementos)
    return response