def registrar_log(request, acao, descricao=''):
    try:
        from .models import LogAuditoria
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        LogAuditoria.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            acao=acao,
            descricao=descricao,
            ip=ip
        )
    except Exception:
        pass