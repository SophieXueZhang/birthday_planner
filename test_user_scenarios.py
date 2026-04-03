#!/usr/bin/env python3
"""
深度用户场景测试
模拟5种不同类型的用户，发现潜在问题
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
console = Console()


def test_user_scenarios():
    """测试不同用户场景"""

    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   深度用户场景测试 - 寻找隐藏问题   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    issues = []

    # 场景1：技术小白 - 张阿姨（50岁）
    console.print("[bold yellow]━━━ 场景1：技术小白用户（张阿姨，50岁）━━━[/bold yellow]")
    console.print("背景：不熟悉电脑，想为孙女办派对\n")

    console.print("使用过程：")
    console.print("  1. 打开程序...")
    console.print("     💭 \"这些英文菜单看不懂...\"")
    issues.append("❌ 缺少新手引导和帮助文档")

    console.print("  2. 创建派对时...")
    console.print("     💭 \"YYYY-MM-DD是什么格式？我只记得5月1号\"")
    issues.append("❌ 日期输入不够友好，应支持多种格式")

    console.print("  3. 查看购物清单...")
    console.print("     💭 \"字太小了，我看不清...\"")
    issues.append("❌ 缺少字体大小调整选项")

    console.print("  4. 保存数据时...")
    console.print("     💭 \"文件保存在哪了？我找不到...\"")
    issues.append("❌ 文件位置不够明显\n")

    # 场景2：忙碌家长 - 李女士（工作日晚上10点）
    console.print("[bold yellow]━━━ 场景2：忙碌家长（李女士，晚上10点）━━━[/bold yellow]")
    console.print("背景：白天上班，只能晚上处理，时间有限\n")

    console.print("使用过程：")
    console.print("  1. 快速创建派对...")
    console.print("     💭 \"能不能一键用上次的设置？\"")
    issues.append("❌ 缺少'参考上次派对'快速创建功能")

    console.print("  2. 添加客人...")
    console.print("     💭 \"我想从手机通讯录导入，但只有电脑版...\"")
    issues.append("❌ 缺少从通讯录导入的功能")

    console.print("  3. 查看进度...")
    console.print("     💭 \"我想看总体完成度，但要点好几个菜单\"")
    issues.append("❌ 缺少仪表盘/总览视图")

    console.print("  4. 半夜想起遗漏...")
    console.print("     💭 \"想快速加个物品，但要进好几层菜单...\"")
    issues.append("❌ 缺少快捷操作模式\n")

    # 场景3：预算紧张 - 王女士（预算1000元）
    console.print("[bold yellow]━━━ 场景3：预算紧张用户（王女士，预算1000元）━━━[/bold yellow]")
    console.print("背景：单亲妈妈，想给孩子办派对但预算有限\n")

    console.print("使用过程：")
    console.print("  1. 看到购物清单...")
    console.print("     💭 \"预估1900元，超出预算了！哪些可以省？\"")
    issues.append("❌ 缺少省钱建议（哪些可以自制、哪些可以借）")

    console.print("  2. 想找便宜替代...")
    console.print("     💭 \"蛋糕200太贵了，超市蛋糕100可以吗？\"")
    issues.append("❌ 缺少物品替代建议")

    console.print("  3. 想比价...")
    console.print("     💭 \"不同商店价格差很多，但我不知道去哪买便宜\"")
    issues.append("❌ 缺少价格参考和比价功能")

    console.print("  4. 想分期采购...")
    console.print("     💭 \"我想先买便宜的，发工资再买贵的\"")
    issues.append("❌ 缺少分阶段采购计划\n")

    # 场景4：多孩家庭 - 刘女士（管理3个孩子的派对）
    console.print("[bold yellow]━━━ 场景4：多孩家庭（刘女士，3个孩子）━━━[/bold yellow]")
    console.print("背景：三个孩子生日接近，需要同时规划多个派对\n")

    console.print("使用过程：")
    console.print("  1. 创建第二个派对...")
    console.print("     💭 \"客人名单大部分一样，能不能复制？\"")
    issues.append("❌ 缺少派对模板和复制功能")

    console.print("  2. 切换派对...")
    console.print("     💭 \"我现在看的是哪个孩子的派对？容易搞混\"")
    issues.append("❌ 缺少多派对管理和切换界面")

    console.print("  3. 对比预算...")
    console.print("     💭 \"3个派对总共要花多少钱？\"")
    issues.append("❌ 缺少多派对汇总功能")

    console.print("  4. 共享资源...")
    console.print("     💭 \"有些装饰品可以三个派对共用\"")
    issues.append("❌ 缺少跨派对资源共享功能\n")

    # 场景5：新手家长 - 陈女士（第一次办派对）
    console.print("[bold yellow]━━━ 场景5：新手家长（陈女士，第一次办派对）━━━[/bold yellow]")
    console.print("背景：完全没经验，不知道从何开始\n")

    console.print("使用过程：")
    console.print("  1. 第一次打开...")
    console.print("     💭 \"我应该先做什么？\"")
    issues.append("❌ 缺少新手教程/向导模式")

    console.print("  2. 看到购物清单...")
    console.print("     💭 \"为什么需要买这些？有什么用？\"")
    issues.append("❌ 物品缺少说明和图片参考")

    console.print("  3. 看到检查清单...")
    console.print("     💭 \"每个任务具体怎么做？\"")
    issues.append("❌ 任务缺少详细操作指南")

    console.print("  4. 想看成功案例...")
    console.print("     💭 \"别人都是怎么办的？能给我参考吗？\"")
    issues.append("❌ 缺少成功案例库和灵感")

    console.print("  5. 遇到问题...")
    console.print("     💭 \"场地突然不能用了，怎么办？\"")
    issues.append("❌ 缺少应急预案和常见问题解答\n")

    # 汇总问题
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         发现的问题汇总         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    categories = {
        "易用性": [],
        "功能性": [],
        "实用性": [],
        "教育性": []
    }

    # 分类问题
    usability = ["新手引导", "日期格式", "字体大小", "文件位置", "快捷操作", "总览视图"]
    functionality = ["参考上次", "通讯录导入", "多派对管理", "派对模板", "汇总功能", "资源共享"]
    practicality = ["省钱建议", "替代建议", "比价", "分期采购"]
    education = ["新手教程", "物品说明", "操作指南", "成功案例", "应急预案"]

    for issue in issues:
        if any(keyword in issue for keyword in usability):
            categories["易用性"].append(issue)
        elif any(keyword in issue for keyword in functionality):
            categories["功能性"].append(issue)
        elif any(keyword in issue for keyword in practicality):
            categories["实用性"].append(issue)
        elif any(keyword in issue for keyword in education):
            categories["教育性"].append(issue)

    for category, issues_list in categories.items():
        if issues_list:
            console.print(f"[bold yellow]{category}问题（{len(issues_list)}个）：[/bold yellow]")
            for issue in issues_list:
                console.print(f"  {issue}")
            console.print()

    console.print(f"[bold red]总计发现 {len(issues)} 个潜在问题[/bold red]\n")

    # 优先级排序
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         建议的改进优先级         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[bold red]🔥 高优先级（严重影响使用）：[/bold red]")
    console.print("  1. 新手引导和帮助文档")
    console.print("  2. 仪表盘/总览视图")
    console.print("  3. 日期格式友好化")
    console.print("  4. 省钱建议和替代方案\n")

    console.print("[bold yellow]⚡ 中优先级（提升体验）：[/bold yellow]")
    console.print("  5. 参考上次派对快速创建")
    console.print("  6. 快捷操作模式")
    console.print("  7. 物品说明和图片")
    console.print("  8. 成功案例库\n")

    console.print("[bold green]💡 低优先级（锦上添花）：[/bold green]")
    console.print("  9. 多派对管理")
    console.print("  10. 通讯录导入")
    console.print("  11. 比价功能")
    console.print("  12. 字体大小调整\n")

    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         关键洞察         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[bold yellow]我们之前关注的是：[/bold yellow]")
    console.print("  • 功能完整性 ✅")
    console.print("  • 操作效率 ✅")
    console.print("  • 数据准确性 ✅\n")

    console.print("[bold red]但用户真正需要的还有：[/bold red]")
    console.print("  • 降低使用门槛（新手友好）")
    console.print("  • 提供决策支持（省钱建议）")
    console.print("  • 给予信心保障（成功案例）")
    console.print("  • 应对突发情况（应急预案）\n")

    console.print("[bold green]真正的5星体验 = 功能完善 + 人性关怀[/bold green]\n")

    return issues


if __name__ == "__main__":
    issues = test_user_scenarios()

    console.print("\n[bold magenta]💡 结论：[/bold magenta]")
    console.print("[yellow]技术上达到了5星，但用户体验还有提升空间。[/yellow]")
    console.print("[yellow]需要从\"能用\"升级到\"好用\"，再升级到\"贴心\"。[/yellow]")

    console.print("\n[bold cyan]接下来应该做什么？[/bold cyan]")
    console.print("1. 先实现4个高优先级改进")
    console.print("2. 再考虑中优先级的体验提升")
    console.print("3. 最后添加锦上添花的功能")
