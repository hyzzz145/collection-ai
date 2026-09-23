# task-0 的学习记录
## 9 月 19 日

我先整体预览一遍本章吧

- 文档1
    - 整理笔记.

## 9 月 20 日
- 学习一下 Lambds 函数
- 我感觉用两块屏幕学习还挺还，左屏放 ai 和 编程教程，右边 vscode 和 github
- 在复习一下正则表达式

## 9 月 21 日
- 昨天和上午过了一遍 OOP
- **娜比娅偷吃事件**
    - 已 clone Nabia_Snack_Incident ,一开始我不知道怎么克隆一个仓库文件的某个特定文件夹，问了 Deepseek AI, 复制了大概流程
        - **如下，deepseek model 生成**
        ```terminal
        git clone --filter=blob:none --no-checkout https://github.com/west2-online/learn-AI.git
        cd learn-AI
        git sparse-checkout init --cone
        git sparse-checkout set "tasks(2026)/foundation/Nabia_Snack_Incident"
        git checkout main
        ```
    - 我去，这个代码检查是不是有点太严格了，做第一个 display_status 时，好像只是打印的字有个符号不一样，也不行
    - 认识到 raise 的作用
    - *任务二*独立完成
    - *任务三* easy！
    - 完成*任务四*和*任务五*，感觉还好。
## 9月 22 日
- **娜比娅偷吃事件**
    - 完成了剩下的任务，但最后一个我检测很多遍，就是找不到问题
    - 哦，原来是 < 写成 == 了。
    - 通过本练习，我学会了要判断输入数据的合法性
    - 欸，怎么一直是长门胜利
- 了解一下列表推导式，类型注释,还有生成器
- 接触作业 2 ，校园 if 恋。
- ok ，已克隆。
- **GalGame**
    - 完成了小白的 choice 。
## 9月 23 日
- **GalGame**
    - 花了几个小时完成这个作业，完成还行，修bug才是最痛苦的。
    - 自嘲一下，在调用 character 的实例方法时，下面写的全是 character ，我真是傻了
    - "奇怪的石头": {default: -10} 原程序这么写还导致报错欸