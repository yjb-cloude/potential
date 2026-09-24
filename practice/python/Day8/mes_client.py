# Day 8: 封装 MES 接口客户端类
# =====================================================
# 封装企业级写法，和 lesson_requests.py 的 ApiClient 风格一致

import requests
import time


class MesClient:
    """MES 制造执行系统接口客户端"""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "blade-auth": token,
        })
        print(f"[MesClient] 初始化完成，服务器: {self.base_url}")

    def save_flow_record(
        self,
        work_order_code: str,
        process_code: str,
        flow_code: str,
        operator_id: str,
        result: str = "OK",
    ) -> tuple:
        """
        提交一道工序的流转记录

        返回：(success: bool, msg: str)
        """
        url = f"{self.base_url}/mes-manufact/flowProRecord/saveFlowRecord"
        payload = {
            "workOrderCode": work_order_code,
            "processCode": process_code,
            "flowCode": flow_code,
            "operatorId": operator_id,
            "result": result,
        }

        try:
            resp = self.session.post(url, json=payload, timeout=10)
            try:
                body = resp.json()
            except Exception:
                body = {}

            # 判断业务成功：HTTP 200 + success 不为 false + code 为 200 或缺失
            ok = resp.status_code == 200
            if "success" in body and body["success"] is not True:
                ok = False
            if body.get("code") not in (None, 200):
                ok = False

            msg = body.get("msg", "") or resp.text[:200]
            return (ok, msg)

        except Exception as e:
            return (False, str(e))

    def batch_run_processes(
        self,
        work_order_code: str,
        flow_code: str,
        process_codes: list,
        operator_id: str,
        result: str = "OK",
        wait_seconds: float = 1,
    ) -> dict:
        """
        一个流转码依次跑完所有工序

        返回：{
            "flow_code": str,
            "total": int,
            "success": int,
            "fail": int,
            "details": [(process_code, ok, msg), ...]
        }
        """
        details = []
        success = 0
        fail = 0

        print(f"\n===== 流转码 {flow_code} 开始 =====")

        for i, process_code in enumerate(process_codes):
            ok, msg = self.save_flow_record(
                work_order_code, process_code, flow_code, operator_id, result
            )
            details.append((process_code, ok, msg))

            if ok:
                success += 1
            else:
                fail += 1

            status_icon = "OK" if ok else "FAIL"
            print(f"  {process_code} → {status_icon} {msg}")

            # 最后一道工序不等待
            if i < len(process_codes) - 1:
                print(f"  等待 {wait_seconds}s...")
                time.sleep(wait_seconds)

        print(f"===== 流转码 {flow_code} 完成：成功 {success}，失败 {fail} =====\n")

        return {
            "flow_code": flow_code,
            "total": len(process_codes),
            "success": success,
            "fail": fail,
            "details": details,
        }
