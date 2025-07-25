# Chatbot/AIchat/forms.py
from django import forms

class ChatInputForm(forms.Form):
    """
    Form for user input in the chat.
    """
    user_input = forms.CharField(
        label='Your Message',
        max_length=1000,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your message here...',
            'class': 'form-control'
        })
    )

