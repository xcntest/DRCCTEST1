import jsonpath
jsonstr= {
    "code": 100000,
    "message": "成功",
    "result": {
        "id": 20,
        "name": "查询资产组用资产组1",
        "desc": "查询资产组用资产组"
    }
}


data  = jsonpath.jsonpath(jsonstr,"$.result.id")
print(data)

