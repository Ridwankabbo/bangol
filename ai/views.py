from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .agent_logic import run_ecommerce_agent
import traceback
# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_view(request):
    user_query = request.data.get('message')
    if not user_query:
        return Response({"error": "Message is required"}, status=400)

    context_query = f"User ID: {request.user.id}. Customer says: {user_query}"
    
    try:
        ai_response = run_ecommerce_agent(context_query)
        return Response({
            "reply":ai_response
        })
    except Exception as e:
        print("--- AGENT ERROR START ---")
        traceback.print_exc() 
        print("--- AGENT ERROR END ---")
        return Response({"error": str(e)}, status=500)