from django import forms


my_date_format = '%d/%m/%Y' 
my_time_format = '%H:%M' 

class MyDateField(forms.DateField):
    
    def __init__(self, label=None, required=False):
        super(MyDateField, self).__init__(required=required, input_formats=[my_date_format,], widget=forms.widgets.DateInput(format=my_date_format), label=label)

class MySplitDateTimeField(forms.SplitDateTimeField):
    
    def __init__(self, label=None, required=False):
        super(MySplitDateTimeField, self).__init__(required=required, input_date_formats=[my_date_format,], input_time_formats=[my_time_format,], widget=forms.widgets.SplitDateTimeWidget(date_format=my_date_format, time_format=my_time_format), label=label)