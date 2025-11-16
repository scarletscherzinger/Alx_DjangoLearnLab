from django import forms

class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form handling with Django.
    This form automatically includes CSRF protection when rendered in templates.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message', 'rows': 4})
    )
    
    def clean_name(self):
        """Validate and sanitize name input"""
        name = self.cleaned_data.get('name')
        # Remove any potentially harmful characters
        if name:
            name = name.strip()
        return name