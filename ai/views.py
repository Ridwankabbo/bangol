from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .agent_logic import run_ecommerce_agent
import re, json, traceback
from .models import ChatHistory
# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_view(request):
    user_query = request.data.get('message')
    user = request.user
    if not user_query:
        return Response({"error": "Message is required"}, status=400)

    context_query = f"User ID: {request.user.id}. Customer says: {user_query}"
    
    past_messages = ChatHistory.objects.filter(user=user).order_by('-created_at')[:5]
    history_list = []
    for msg in reversed(past_messages):
        history_list.append(('human', msg.message))
        history_list.append(('ai', msg.response))
        
    
    try:
        ai_response = run_ecommerce_agent(context_query, history_list)
        
        ChatHistory.objects.create(
            user = user,
            message = user_query,
            response = ai_response
        )
        
        message_match = re.search(r"MESSAGE:\s*(.*?)(?=DATA:|$)", ai_response, re.DOTALL)
        data_match = re.search(r"DATA:\s*(\[.*\])", ai_response, re.DOTALL)
        
        chat_text = message_match.group(1).strip() if message_match else ai_response
        
        product_data = []
        
        if data_match:
            try:
                product_data = json.loads(data_match.group(1))
            except:
                product_data = []
        return Response({
            "reply":chat_text,
            "product_data": product_data,
        })
    except Exception as e:
        print("--- AGENT ERROR START ---")
        traceback.print_exc() 
        print("--- AGENT ERROR END ---")
        return Response({"error": str(e)}, status=500)