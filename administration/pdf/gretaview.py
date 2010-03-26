from django.core.exceptions import ObjectDoesNotExist
import common

class GretaView(object):
    
    def _optionalField(self, field):
        try:
            result = eval(field)
            if result:
                return result
            return ''
        except ObjectDoesNotExist:
            return ''
        
    def _optionalDateField(self, field):
        result = self._optionalField(field)
        if result:
            return result.strftime(common.date_format)
        return '' 