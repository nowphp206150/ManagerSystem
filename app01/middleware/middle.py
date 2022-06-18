from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        '''
        写我们想要写的
        :return:
        '''
        if request.path_info in ['/login/','/imgcode/']:
            return
        if request.session.get('info'):
            return
        return redirect('/login/')

    def process_response(self,request,response):
        '''

        :param request:
        :param response:
        :return: response
        '''
        return response
