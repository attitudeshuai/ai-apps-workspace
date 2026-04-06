# Session demo

该文件用于保存 session-demo 通过 PromptArchitect 生成的提示词。

追加规则：

- 新项目追加到文件末尾
- 支持一次处理多个项目，按项目逐条追加
- 若存在语义相近的旧提示词，先询问用户是否保留
- 默认不覆盖已有记录

---

## Q: label-02404

### 项目路径
D:\charles\program\ai\apps\02.work session\session-4\gitlab source\label-02404

### Prompt
现在项目有 README、API 文档、部署说明和启动脚本，但工程链路还是偏手工。基于现有 Java 17、Maven、Docker、JUnit 5 结构，提出一套更像正式项目的工程化方案，重点看配置分层、测试接入、打包发布、日志，做完之后需要检查对应的改动,确保项目能成功运行