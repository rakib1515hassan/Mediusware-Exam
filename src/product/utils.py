from rest_framework.response import Response


def api_success(results, status=200, message="Operation successful"):
    if results is None:
        results = {}
    data = {'success': True, "message": message}
    if "results" in results:
        data.update(results)
    else:
        data["results"] = results

    return Response(data, status=status)


def api_error(data, status=400, message="Something went wrong!"):
    if data is None:
        data = {}

    if not isinstance(data, dict):
        data = {'results': data}
    data['success'] = False
    data["message"] = message
    return Response(data, status=status)