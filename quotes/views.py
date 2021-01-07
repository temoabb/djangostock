from django.shortcuts import render, redirect
from . models import Stock
from . forms import StockForm
from django.contrib import messages


def home(request):
	import requests  
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get('https://api.fda.gov/food/enforcement.json?limit=10') # " " + ticker + " "

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."

		return render(request, 'home.html', {'api': api['results'][0]})

	else:
		return render(request, 'home.html', {'ticker': "Enter a ticker symbol above.."})

	

	# api_request = requests.get('https://official-joke-api.appspot.com/jokes/ten')


def about(request):
	return render(request, 'about.html', {})



def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ('Stock Has Been Added!'))
			return redirect('add_stock')

	else:
		context_ticker = Stock.objects.all()
		output = []

		for ticker_item in context_ticker:
			api_request = requests.get('https://api.fda.gov/food/enforcement.json?limit=10') # " " + str(ticker_item) + " "

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': context_ticker, 'output': output})




def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ('Item das been deleted!'))
	return redirect('delete_stock')



def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})




# TOKEN: pk_85661c0a91dc4d3ea1cff4baace0acc2
# api: https://cloud/iexapis.com/stable/stock/aapl/quote?token=pk_85661c0a91dc4d3ea1cff4baace0acc2