import json
response = '''
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 3,
        "records": [
            {
                "id": 1001,
                "planCode": "PP-2026-001",
                "status": 2,
                "product": {"name": "芯片A", "model": "X100"},
                "tasks": ["切割", "封装", "测试"]
            },
            {
                "id": 1002,
                "planCode": "PP-2026-002",
                "status": 1,
                "product": {"name": "芯片B", "model": "X200"},
                "tasks": ["切割", "焊接"]
            },
            {
                "id": 1003,
                "planCode": "PP-2026-003",
                "status": 0,
                "product": None,
                "tasks": []
            }
        ]
    }
}
'''
response_json = json.loads(response)
def validate_api_response(response_json, expected_total,  expected_fields=None):

   expected_total = len(response_json["data"]["records"])

   print(f"总记录数: {expected_total}")
   for record in response_json["data"]["records"]:
     for tasks in record["tasks"]:
        if len(tasks) >=2:
           planCode = record["planCode"]
           print(f"计划编号: {planCode}")
     if record["status"] == 0:
      print(f"计划编号: {record['product']} 状态: {record['status']}")