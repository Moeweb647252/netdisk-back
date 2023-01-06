from django.http.response import JsonResponse

STATUS_CODE = {
  1000: {"code": 1000}, 
  2000: {"code": 2000}, 
  2001: {"code": 2001}, 
  2101: {"code": 2101}, 
}


def generateApiResponse(code:int=100,data:object=None):
  """_summary_

  Args:
    code (int, optional): _description_. Defaults to 100.
    data (object, optional): _description_. Defaults to None.
  
  Code:
    1000: Success.
    2000: Error.
    2001: Error: Missing parameter.
    2101: Error: File or Directory not found.
 
  Returns:
    _type_: _description_
  """ 
  if not code in STATUS_CODE.keys():
    raise Exception("Status Code not found.")
  respBody = STATUS_CODE[code].copy()
  respBody["data"] = data
  return JsonResponse(respBody)