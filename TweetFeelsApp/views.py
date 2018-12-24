from django.shortcuts import render
from .classes.report import AnalysisReport

def home(request):
    return render(request, 'home.html', {})

def results(request):
    if (request.method == 'GET'):
        error = 'You did not type a query. Please type a query in the homepage.'
        return render(request, 'results.html', {'error':error})
    
    query = request.POST['query']
    
    analysisReport = AnalysisReport()
    analysisReport.CreateReport(query)

    return render(request, 'results.html', {'query': analysisReport.query, 'data': analysisReport.data, 'percentages': analysisReport.percentages, 'error': analysisReport.error})