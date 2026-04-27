from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(username=username, password=password)

        if usuario is None:
            return Response(
                {'erro': 'Credenciais invalidas'},
                status=401
            )

        if not usuario.is_active:
            return Response(
                {'erro': 'Usuario inativo'},
                status=403
            )

        refresh = RefreshToken.for_user(usuario)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'perfil': usuario.perfil,
            }
        })


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'mensagem': 'Logout realizado com sucesso'})
        except Exception:
            return Response({'erro': 'Token invalido'}, status=400)