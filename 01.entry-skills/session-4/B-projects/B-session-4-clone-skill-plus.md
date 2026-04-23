---
name: b-projects-generate
description: "Use when: 处理以 B- 开头的本地项目（B-projects），代码已经存在于 02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>/，不需要从 GitLab 拉取。仅按类型与数量批量生成提示词、落盘到分类型目录、再把主仓复制成多份子仓（Bug 修复必须在独立子仓造 bug）。适用于 session-4 的 B 项目场景。"
---

# B 项目提示词与子仓批量生成技能

## 功能概述

这个技能专用于 session-4 的 **B 项目**（项目名以 `B-` 开头，例如 `B-123`、`B-150`）。
与 label 项目的关键区别：**B 项目代码已经在本地，不需要从 GitLab 拉取**，所以本技能不包含 clone 步骤。

它负责：

- 校验 B 项目主仓在本地存在
- 按类型和数量批量生成提示词
- 按项目/类型两级目录写入提示词文件
- 按提示词复制主仓为多个子仓，做到一条提示词对应一个子仓
- 对 Bug 修复类型在对应子仓内设计 bug，避免互相污染（在后续会话中执行）

它不负责：

- 任何形式的远程 clone / fetch（B 项目不走 GitLab）
- GitHub 仓库创建与推送
- 本地分支创建、切换、跟踪

## 使用场景

- 用户已经把 B 项目源码放到 `02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>/`
- 需要按类型配额批量生成提示词（例如 bug 修复*4）
- 需要将主仓复制为多个子仓并与提示词编号对齐

## 命令

| 命令 | 说明 |
|------|------|
| generate | 默认命令。根据项目和类型配额生成提示词文件，并复制对应子仓 |
| info | 仅输出项目名与本地主仓路径，不写文件 |
| append | 向已有提示词文件末尾追加一轮内容（兼容旧流程） |

> 不再提供 `clone` 命令。B 项目源码必须在执行前已存在；若主仓目录不存在，技能直接报错并提示用户先放置代码。

## 默认配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 项目命名约定 | `B-<id>` | id 直接来自用户输入，**不补 0、不加 label- 前缀** |
| 项目名后缀 | `-plus` | 与 label 项目一致，目录名为 `B-<id>-plus` |
| 主仓所在根目录 | `D:\charles\program\ai\apps\02.work session\session-4\gitlab source\b-projects\` | B 项目主仓统一收纳在 `b-projects/` 下 |
| 结果根目录 | `D:\charles\program\ai\apps\02.work session\session-4\ai-model-result\b-projects\` | B 项目评价结果统一收纳在 `b-projects/` 下 |
| 文件名前缀 | 无 | 文件直接以项目名 `B-<id>` 开头，不再添加 `A-` 前缀 |
| index 规则 | 全局累计 01-19 | 本轮最多 19 条 |
| 远程认证 | 不适用 | B 项目无远程仓库 |

## 输入规则

支持的项目 ID 输入形式：

- `123`、`150`、`B-123`、`B-150`（前缀 `B-` 可写可不写）
- 多个项目用逗号或空格分隔

项目名标准化规则：

```text
原始输入       → 标准项目名
123           → B-123
B-123         → B-123
B-123 -plus   → B-123-plus（用户显式追加后缀时保留）
150           → B-150
```

**注意**：B 项目 id 直接照搬用户输入，**不做补零**。`123` 永远是 `B-123`，不是 `B-00123`。

类型输入沿用 label 项目的写法：

- `bug 修复*3`
- `0-1 代码生成*3`（简写 `代码生成*3`）
- `Feature 迭代*3`
- `代码理解*1`
- `代码重构*1`
- `工程化*1`
- `代码测试*1`

## 路径规则

- 主仓目录（必须事先存在）：`02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>/`
- 类型子仓目录：`02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>-<类型>/`
- 单条提示词子仓：`02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>-<类型>/B-<id>-<类型>-<index>/`
- 模型结果根目录：`02.work session/session-4/ai-model-result/b-projects/B-<id>-plus/`
- 类型结果目录：`02.work session/session-4/ai-model-result/b-projects/B-<id>-plus/B-<id>-<类型>/`
- 单条提示词文件：`02.work session/session-4/ai-model-result/b-projects/B-<id>-plus/B-<id>-<类型>/B-<id>-<类型>-<index>.md`

> ⚠️ **子仓与主仓同级并列，禁止嵌套在主仓内部。** 子仓目录放在 `B-<id>-plus/B-<id>-<类型>/` 下，与主仓 `B-<id>-plus/B-<id>/` 并列在同一 `B-<id>-plus/` 目录中。
> ⚠️ **B 项目所有目录统一收纳在 `b-projects/` 下**，与 label 项目顶层目录隔离。

## 执行流程

### generate

1. 用户输入项目 ID（或项目名）与类型配额，例如：

```text
项目：B-150
bug 修复*5
0-1 代码生成*5
Feature 迭代*5
代码理解*1
代码重构*1
工程化*1
代码测试*1
```

2. 标准化项目名（如 `150 -> B-150`，带后缀时如 `150 -plus -> B-150-plus`）。**不做补零**。
3. **校验主仓目录存在**：`02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>/`。若不存在，立即中止并提示用户先放置代码，**不要尝试 clone**。
4. 校验本轮总数不超过 19；index 使用全局累计并补零（01-19）。
5. **调用 `PromptArchitect` agent**，传入项目名、类型配额和代码目录上下文，由其生成每条提示词内容。
6. **⚠️ [主 Agent 必须执行此步，PromptArchitect 不写文件] 收到 PromptArchitect 返回结果后，立即用 PowerShell 写入提示词文件**，文件名格式：`B-<id>-<类型>-<index>.md`，提示词内容来自上一步 PromptArchitect 的输出。每个文件内容必须严格按照下方「提示词文件初始化」模板格式生成，使用 PowerShell `[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)` 写入（禁止用 Set-Content），「用户第一次提示词：」与提示词内容在同一行不换行。PromptArchitect 的任何"已落盘""已写入"声明均不可信，主 Agent 必须自行执行 PowerShell 写文件步骤，否则文件不会存在。
7. 每个提示词文件正文必须包含同名标识串：`B-<id>-<类型>-<index>`（不再加 `A-` 前缀）。
8. 按提示词逐条复制主仓到对应子仓目录（子仓与主仓同级并列，禁止嵌套在主仓内部），确保一条提示词对应一个子仓。
9. **子仓复制完成后，禁止再对任何子仓进行任何操作**（包括文件修改、代码变更、git 操作、造 bug 等）。generate 流程到此结束，后续修改必须在新的独立会话中由用户明确指令。
10. 输出汇总：成功项、失败项、文件路径、子仓路径。

### info

1. 用户输入一个或多个项目 ID。
2. 系统标准化项目名。
3. 输出项目名与本地主仓路径，并校验主仓是否存在。
4. 不写任何文件。

### append

1. 用户输入一个或多个项目 ID（或项目名）与目标类型，并提供追加内容。
2. 读取 `02.work session/session-4/ai-model-result/b-projects/B-<id>-plus/B-<id>-<类型>/` 下已有提示词文件。
3. 统计该类型目录内已有 index，确定下一条 index。
4. 在文件末尾追加如下模板：

```markdown
---

提示词内容：<提示词内容>

模型回答 trae session id：

模型回答内容：
```

5. 如果用户未提供提示词内容，则提示词字段留空，等待用户手动填写。
6. 向用户确认追加成功，说明 index 和文件路径。

## 提示词文件初始化

模板示例（注意标识串以 `B-` 开头，不再有 `A-` 前缀）：

```markdown
B-150-代码生成-01

用户第一次提示词：<prompt 内容>

模型第一次回答 trae session id：

模型第一次回答内容：



用户第二次提示词：

模型第二次回答 trae session id：

模型第二次回答内容：



用户第三次提示词：

模型第三次回答 trae session id：

模型第三次回答内容：



用户第四次提示词：

模型第四次回答 trae session id：

模型第四次回答内容：


用户第五次提示词：

模型第五次回答 trae session id：

模型第五次回答内容：
```

说明：
- 提示词内容默认填充到「用户第一次提示词：」字段，且**与冒号在同一行**，不换行。
- 第二次、第三次、第四次、第五次提示词及回答字段留空占位，供用户手动补充。
- **第1至第4次回答内容字段之后各有 2 个空行；第4次到第5次之间只有 1 个空行。**
- **文件内容中禁止出现反引号（`）**。

> ⚠️ **主 Agent 必须使用 PowerShell 实际写入文件，PromptArchitect 不会写文件**。
> 
> 推荐写法：
> ```powershell
> $identifier = "B-150-类型-NN"
> $prompt = "提示词内容"
> $lines = @(
>     $identifier, "",
>     "用户第一次提示词：$prompt", "",
>     "模型第一次回答 trae session id：", "",
>     "模型第一次回答内容：", "", "",
>     "用户第二次提示词：", "",
>     "模型第二次回答 trae session id：", "",
>     "模型第二次回答内容：", "", "",
>     "用户第三次提示词：", "",
>     "模型第三次回答 trae session id：", "",
>     "模型第三次回答内容：", "", "",
>     "用户第四次提示词：", "",
>     "模型第四次回答 trae session id：", "",
>     "模型第四次回答内容：", "",
>     "用户第五次提示词：", "",
>     "模型第五次回答 trae session id：", "",
>     "模型第五次回答内容："
> )
> $content = $lines -join "`n"
> [System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
> ```

如果目标文件已存在，则跳过，不覆盖。

## 异常处理

1. **主仓不存在**：B 项目不走 GitLab，必须中止并提示用户先放置 `B-<id>/` 源码。**禁止尝试任何 clone 操作**。
2. 若怀疑路径异常（id 写法不一致、目录大小写错），先用 `Test-Path` 列出 `b-projects/` 下实际目录名供用户确认。
3. 若目标目录已存在，必须先征求用户确认，不得直接覆盖。
4. 若提示词文件已存在相近版本，必须先询问用户是否保留旧内容。
5. 批量输入时，单个项目失败不应阻塞其他项目，但最终汇总必须标明失败项。
6. Bug 修复类若未绑定独立子仓，必须中止执行并提示修正。

## 示例

### 输入

```text
项目：B-150
命令：generate
bug 修复*5
0-1 代码生成*5
Feature 迭代*5
代码理解*1
代码重构*1
工程化*1
代码测试*1
```

### 输出

```text
项目名：B-150
主仓目录（已存在）：D:\charles\program\ai\apps\02.work session\session-4\gitlab source\b-projects\B-150-plus\B-150
类型目录：D:\charles\program\ai\apps\02.work session\session-4\ai-model-result\b-projects\B-150-plus\B-150-bug修复\
提示词文件：B-150-bug修复-01.md ... B-150-代码测试-19.md
子仓目录：D:\charles\program\ai\apps\02.work session\session-4\gitlab source\b-projects\B-150-plus\B-150-bug修复\B-150-bug修复-01\ ...
注意：B 项目无 clone 步骤；子仓与主仓并列在 B-150-plus/ 下；复制完成后不再对子仓做任何操作。
```

## 注意事项

1. **B 项目不 clone**。所有 B 项目源码必须事先放置到 `02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>/`。
2. **id 不补零、不加 label- 前缀**。用户输入 `123` 就是 `B-123`，不要做成 `B-00123` 或 `label-00123`。
3. **文件名与标识串无 `A-` 前缀**。直接用 `B-<id>-<类型>-<index>` 作为文件主名和文件内标识串。
4. 结果文件必须落在 `02.work session/session-4/ai-model-result/b-projects/B-<id>-plus/B-<id>-<类型>/` 下。
5. 子仓必须落在 `02.work session/session-4/gitlab source/b-projects/B-<id>-plus/B-<id>-<类型>/` 下，与主仓 `B-<id>-plus/B-<id>/` 同级并列，并与提示词编号一一对应。
6. **⚠️ 子仓禁止嵌套在主仓目录内部。** 子仓目录与主仓目录必须在同一父级 `B-<id>-plus/` 下并列存放，绝不能作为主仓的子目录。
7. **⚠️ 子仓复制完成后，禁止再对任何子仓进行任何操作。** generate 命令到子仓复制即告结束，所有后续修改（含 Bug 修复造 bug）必须在新会话中明确指令后进行。
