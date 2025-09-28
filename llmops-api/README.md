# flask-migrate
## 初始化
pdm run flask init db
## 生成迁移脚本
pdm run flask db migrate -m "create_table"
-m "create_table" 是给这个迁移写一个注释
生成的迁移脚本中有两个参数：
- upgrade(): 把迁移中的改动应用到数据库中
- downgrade(): 将改动撤销

