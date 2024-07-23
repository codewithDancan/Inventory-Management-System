def global_context(request):
    return {
        'base_url': request.build_absolute_uri('/') [:-1].strip('/')
    }
    
# end def