
class ResponseInfo(object):
    def __init__(self,user=None,**args) -> None:
        self.response = {
            "statusCode": args.get('statusCode', 200),
            "status": args.get('status', True),
            "message": args.get('message', 'success'),
            "data": args.get('data', [])
        }

        
