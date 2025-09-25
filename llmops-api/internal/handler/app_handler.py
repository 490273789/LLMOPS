from dataclasses import dataclass
import uuid
from injector import inject
from openai import OpenAI
from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppsService
from pkg.response import success_json, validate_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""

    app_service: AppsService

    def create_app(self):
        app = self.app_service.create_app()
        return success_message(f"应用已成功创建，应用Id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        print(app)
        return success_message(f"应用name为{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"更新后名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"删除成功，删除id为{app.id}")

    def completion(self):
        """聊天窗口"""
        # 1. 验证请求参数 post
        req = CompletionReq()
        if not req.validate():
            return validate_json(errors=req.errors)
        # 2. 创建OpenAI客户端
        client = OpenAI()
        # 3. 得到请求响应，将响应返回给前端
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "你是OpenAI聊天机器人，请根据用户的输入回复对应的信息。",
                },
                {"role": "user", "content": req.query.data},
            ],
        )

        content = completion.choices[0].message.content

        return success_json(data={"content": content})

    def ping(self):
        raise FailException(message="数据未找到")
        # return {"ping": "pong"}
