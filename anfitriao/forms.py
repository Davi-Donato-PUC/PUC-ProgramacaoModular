from django import forms


class AnfitriaoForm(forms.Form) :
    nome = forms.CharField(label='Nome', max_length=100)
    senha    = forms.CharField(label='senha', max_length=100)


class HotelForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    preco = forms.CharField(label='Preço', max_length=100)
    descricao = forms.CharField(label='Descrição', max_length=100)



