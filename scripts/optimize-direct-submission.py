#!/usr/bin/env python3
"""Apply direct-submission packaging to the production batch.

This is a deterministic packaging pass:
- add opening guide paragraphs after the title;
- strengthen selected chapter-end hooks without visible internal labels;
- convert body prose to mobile-friendly one-sentence paragraphs;
- add a paywall-node map to tomato-submission.md for editorial tracking.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONFIG = {
    "prod_batch_01_autopsy_vow": {
        "lead": [
            "导语：我死在坠桥车里，灵魂被困在鉴定中心，看着事故鉴定师丈夫亲手拆我的车。",
            "他在报告上写下无被迫制动，却漏掉备胎舱里的胎心录音和十周产检单。",
            "等真相从残骸里响起，他才知道数据也会杀人。",
        ],
        "paywall": {
            4: "周聿在报告上写下无被迫制动时，备胎舱里的胎心录音还没有被任何人发现。",
            8: "产检单被攥出血痕那一刻，周聿第一次承认数据也会杀人。",
            12: "审讯室外的录音亮起红灯，许知夏亲口承认她动过那辆车。",
            15: "第五年冬天，空儿童安全座椅被摆上副驾驶，胎心录音却再也没有回应。",
        },
    },
    "prod_batch_02_abyss_profile": {
        "lead": [
            "导语：云衡医学院七天失踪一名女生，我伪装成晕血护理生入校。",
            "第一天，第七例标记就被送到我桌上，所有人都以为我怕血。",
            "没人知道，我是代号寒灯的法医侧写专家，来查这座学校的冷库。",
        ],
        "paywall": {
            4: "冷库外的新标签写着第七例林照，时间正好是今晚二十三点。",
            8: "纪白摘下口罩说跟我去冷库时，我才确认他只是第一只伸出来的手。",
            11: "纪白刚被押走，论坛后台弹出江砚的邀请：第八盏灯，来影像室。",
            14: "影像室门锁落下，江砚把入库和入会两个选项推到我面前。",
            16: "匿名账号发来我儿时病例扫描件，末尾只有四个字：欢迎归档。",
        },
    },
    "prod_batch_03_empress_exit": {
        "lead": [
            "导语：阿娘用雪铃命契替绝嗣汗王生下八个王子，却被他一次次推去替侧妃偿债。",
            "三枚雪铃裂尽后，她不再给王庭下一个孩子。",
            "十年后，我带着她留下的碎铃粉回到金帐，要把儿子、王位和血债一并讨回。",
        ],
        "paywall": {
            3: "南帐帘子落下时，我听见阿娘在雪地里吐血。",
            5: "剜雪瞳的银刀落下前，阿娘把我推到身后。",
            7: "最后一枚雪铃粉碎，我才知道她连哭声都留给了我。",
            8: "我跪在仇人脚边叫出额吉时，南帐所有人都以为我认了命。",
            10: "拓跋赫问我想要什么，我把手伸向了王储印。",
            12: "乌兰珠笑着掀开旧脉案，却没有看见我袖中的碎铃粉。",
            13: "我对汗王说，没有我娘，你一个儿子也不会有。",
            15: "金狼王印入手时，我掌心疼得像握着阿娘碎掉的雪铃。",
        },
    },
    "prod_batch_04_blossom_network": {
        "lead": [
            "导语：陆闻舟想用求婚稳住我，却把救援基金八成收益权交给白月光。",
            "外婆等着转诊，七年的陪伴只换来一句她懂事。",
            "我把婚姻、股权和旧家属身份一项项清算，带外婆离开他的世界。",
        ],
        "paywall": {
            4: "清算单签完那一刻，我第一次把离开变成了外婆的救命钱。",
            8: "股权协议交给中介后，陆闻舟才发现我没有拿它换婚礼。",
            12: "国内SIM卡落进机场垃圾桶时，陆闻舟已经没有任何号码能找到我。",
            15: "他追到新加坡诊室外，只看见我牵着外婆走向新的航线。",
        },
    },
    "prod_batch_05_allowance_truth": {
        "lead": [
            "导语：我每月给女儿转四千，却在旧视频里看见她蹲在楼梯间啃冷馒头。",
            "三年生活费只剩五百，丈夫和另一个孩子藏在流水背后。",
            "我从食堂明细、银行流水和旧车录音里，把他们偷走的三千五一笔笔追回来。",
        ],
        "paywall": {
            4: "柜员指着流水说每月三号都有三千五转出时，我终于知道女儿饿在哪里。",
            8: "出生证明被推到桌上后，许国成藏了三年的另一个家终于露出名字。",
            12: "录音里他说要让我女儿觉得，她妈只舍得给她五百。",
            14: "医生把家属谈话单递给许念时，我最想藏住的倒计时还是到了她手里。",
            15: "探视室玻璃后，许念第一次把父亲两个字从许国成身上撕下来。",
        },
    },
    "prod_batch_06_moon_spring": {
        "lead": [
            "导语：沈照棠被关进家庙三年，出门第一件事，是去接五岁的儿子。",
            "可丈夫陆衡舟为了恩人遗孀，亲手锁上药堂，把高烧的孩子挡在雪夜门外。",
            "孩子死后，她不求他回头，只把每一笔血债都藏成日后翻案的证据。",
        ],
        "paywall": {
            3: "而墙外巡夜的人影停住，正好看见她刻下的三道短痕。",
            6: "陆衡舟这才明白，他亲手护住的孩子，从一开始就不是陆家的血脉。",
            9: "她抬头看向跪在火光里的陆衡舟，终于想起自己最恨的那一声铜锁响。",
        },
    },
    "prod_batch_07_fake_princess_friends": {
        "lead": [
            "导语：我是假千金，沈家说我只配逛瓦舍、扎破灯、跟船夫混在一处。",
            "真千金砸了我的走马灯，还抢走我腰间的水师铜哨。",
            "她不知道，那盏灯连着靖王府，那枚哨子一响，连圣上都要问我在哪。",
        ],
        "paywall": {
            3: "谢兰舟抬眼看向沈云姣，声音淡得像雪：那就请她当着本王的面，再砸一次。",
            6: "圣旨还没宣完，沈云姣手里的铜哨已经开始发烫。",
            9: "门后没有野男人，只有一盏被宫里点名要看的真灯。",
            12: "两顶盖头摆在喜房里，沈云姣第一次不知道该抢哪一条路。",
        },
    },
    "prod_batch_08_hotel_group": {
        "lead": [
            "导语：五一音乐节当天，老客户周凯嫌我680元团建套票贵，拿480元裸营位价逼我退差价。",
            "他以为退订就能省钱，还当众威胁差评。",
            "我按合同放他走，转身接下120人研学团。",
            "等黑营地、黄牛车和安全事故找上门，他才知道贵的从来不是我的报价。",
        ],
        "paywall": {
            4: "周凯还不知道，他省下的那笔差价，马上要被第一张黄牛车票吃干净。",
            8: "黑营地老板笑着收走现金时，周凯手机里已经没有一条能报销的正规凭证。",
            12: "他站在满员告示前，终于发现自己亲手退掉的不是营位，是最后一条退路。",
            15: "警灯照进大厅时，他手里的刀还没放下，公司群已经弹出停职通知。",
        },
    },
    "prod_batch_09_streamer_exit": {
        "lead": [
            "导语：我捧陆呈九百万，把他从无人问津捧成短剧顶流。",
            "家宴上，他却牵着我妹妹的手嫌我老，还要我继续给他铺路。",
            "我当场撤掉他的S+男主位，转头把资源给了被他踩在脚下的男二。",
        ],
        "paywall": {
            4: "陆呈盯着后台曲线，第一次看见自己被替代得这么快。",
            8: "律师函送达那一刻，他才发现自己蹭过的每一个热度都有价码。",
            12: "首播战报滚上大屏时，陆呈被保安架出去，顾凛的名字却还在往上跳。",
            15: "顾凛递上新项目表时，陆呈的名字已经从所有候选名单里消失。",
        },
    },
    "prod_batch_10_tang_flower": {
        "lead": [
            "导语：五周年纪念日，陆沉舟签下交换同意书，用我的命去换林若宁。",
            "连我养大的孩子也说，要小姨当妈妈。",
            "他们以为我会哭着留下，可我早已把自己送进白塔计划，受保护离开他们的世界。",
        ],
        "paywall": {
            5: "台风卷走他的背影时，我终于知道，这个家没有一只手会拉住我。",
            9: "他说好，孩子也说好，于是我把最后一份犹豫也签进了撤离档案。",
            12: "录音播放到最后，陆沉舟才听见林若宁真正想要的不是救命，是我的死。",
            15: "火光扑上来时，他终于挡在我身前，可我已经不需要他证明爱了。",
        },
    },
    "prod_batch_11_drowning_divorce": {
        "lead": [
            "导语：婚礼落海那晚，傅寒舟先救了假千金。",
            "我在水下伸手等他，他却抱着许明珠上岸，让全城看我成了笑话。",
            "醒来后，我递上离婚协议，带走修复笔记和证据，连傅家的珠宝署名都不要了。",
        ],
        "paywall": {
            6: "三张图挂出去，全网才发现所谓抢婚的人，早就是合法妻子。",
            10: "实习生的录音放到一半，许明珠的哭声第一次盖不住真相。",
            12: "原片修复完成后，傅寒舟终于看见那只在水下伸向他的手。",
            15: "直播关掉前，许明珠被调查人员带走，傅寒舟却连一句解释都递不到我面前。",
        },
    },
    "prod_batch_12_top_scorer_report": {
        "lead": [
            "导语：我拿到全国法医技能赛金奖当天，养父母和哥哥的死亡记录被医院伪造成出院。",
            "真千金回家，未婚夫退婚，所有人都说我嫉妒到报警。",
            "可我报警不是为了争宠，而是因为仁和医院病理楼里，藏着三具尸体被改写的死亡时间。",
        ],
        "paywall": {
            4: "亲缘初检报告盖下来的那一刻，我的报警反而成了他们反咬我的刀。",
            8: "大屏弹出销毁申请时，发布会现场第一次安静到能听见呼吸。",
            12: "封条被割开的旧血样躺在冰柜里，说明有人比我更怕二次复核。",
            14: "检察官念出贺夫人名字时，贺闻川终于抬头看向他母亲。",
        },
    },
    "prod_batch_13_customs_package": {
        "lead": [
            "导语：我送进平台仓的三十斤碎茶样，被系统判成两千万茶王。",
            "平台要我先交八百万保价费，否则冻结店铺货款。",
            "他们以为一个小茶商只能认栽，我却让他们把货名、估值和收费依据全写进红章确认单。",
        ],
        "paywall": {
            4: "红章落下的瞬间，我没有去缴费，而是转身走向警务联络台。",
            8: "箱盖打开后，两千万茶王只剩一桌碎茶末，直播间的弹幕也停了。",
            12: "八百万分账流水调出来时，赵启明终于连后台密码都说不完整。",
            14: "退款到账那晚，我打开直播间，第一句话只说了一个字。",
        },
    },
    "prod_batch_14_spring_ming": {
        "lead": [
            "导语：裴景明弃我在北境三年，来接我时，我只剩一个月可活。",
            "前世我把命灯烧到最后，换来他一句太晚。",
            "重来一回，我回到爹娘尚在时，不再进王府，也不再等他爱我。",
        ],
        "paywall": {
            4: "那张写着我只剩一月的纸被丢进炭盆，我也彻底看清了他。",
            8: "三十七封信盖上御史台封印时，我终于不用再把委屈说给风听。",
            12: "命灯殿的门开了，我让他进来，不是为了原谅，是让他听清楚判词。",
            14: "裴景明在寺外一点点消失，而这一回，我没有回头。",
        },
    },
    "prod_batch_15_drug_mom_revenge": {
        "lead": [
            "导语：女儿开学那天，我刷到一篇匿名帖：怎么让丈母娘主动回老家，把亲妈换来带娃。",
            "晚上，我妈突然头晕，医院查不出病因，丈夫却顺势提出让婆婆搬来。",
            "我没有摊牌，只封存滤芯、调出水机日志，把他的每一次下手都留给警察。",
        ],
        "paywall": {
            5: "滤芯封进证物袋时，我知道下一次，他一定还会动手。",
            7: "警察问我怀疑谁，我说出丈夫两个字时，周峤终于不笑了。",
            10: "姐姐把门关上的声音很轻，却像替我们把那个家彻底隔开。",
            12: "法庭上，我妈抬头说出那句话时，周峤第一次不敢看她。",
        },
    },
}


def count_nonspace(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def extract_heading(text: str, fallback: str) -> tuple[str, str]:
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip(), "\n".join(lines[1:]).strip()
    return fallback, text.strip()


def split_paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def split_sentences(paragraph: str) -> list[str]:
    paragraph = re.sub(r"\s+", "", paragraph.strip())
    if not paragraph:
        return []
    if paragraph.startswith("#"):
        return [paragraph]

    result: list[str] = []
    start = 0
    i = 0
    while i < len(paragraph):
        ch = paragraph[i]
        if ch in "。！？!?；;":
            j = i + 1
            while j < len(paragraph) and paragraph[j] in "”’』」）》）】\"'":
                j += 1
            sentence = paragraph[start:j].strip()
            if sentence:
                result.append(sentence)
            start = j
            i = j
            continue
        i += 1

    tail = paragraph[start:].strip()
    if tail:
        result.append(tail)
    return result or [paragraph]


def one_sentence_paragraphs(text: str) -> list[str]:
    out: list[str] = []
    for paragraph in split_paragraphs(text):
        out.extend(split_sentences(paragraph))
    return out


def chapter_paths(story: Path) -> list[Path]:
    return sorted((story / "final-chapters").glob("ch*.md"))


def normalize_chapter(path: Path, chapter_no: int, hook: str | None) -> tuple[str, list[str], int]:
    title, body = extract_heading(path.read_text(encoding="utf-8"), f"第{chapter_no}章")
    paragraphs = one_sentence_paragraphs(body)
    if hook and hook not in paragraphs:
        paragraphs.append(hook)
    path.write_text(f"# {title}\n\n" + "\n\n".join(paragraphs).strip() + "\n", encoding="utf-8")
    return title, paragraphs, count_nonspace("\n".join(paragraphs))


def rebuild_final(story: Path, title: str, lead: list[str], chapters: list[tuple[str, list[str], int]]) -> None:
    lead_paragraphs: list[str] = []
    for item in lead:
        lead_paragraphs.extend(split_sentences(item))
    parts = [f"# {title}", *lead_paragraphs]
    for chapter_title, paragraphs, _chars in chapters:
        parts.append(f"## {chapter_title}")
        parts.extend(paragraphs)
    (story / "final.md").write_text("\n\n".join(parts).strip() + "\n", encoding="utf-8")


def update_chapter_map(story: Path, chapters: list[tuple[str, list[str], int]], paywall: dict[int, str]) -> None:
    lines = [
        f"# 章节映射 — {story.name}",
        "",
        "| 序号 | 文件 | 字数 | 节点 | 末句 |",
        "|---|---|---:|---|---|",
    ]
    for index, (title, paragraphs, chars) in enumerate(chapters, start=1):
        hook = paragraphs[-1] if paragraphs else title
        flag = "自然卡点" if index in paywall else "常规悬念"
        lines.append(f"| {index:02d} | `final-chapters/ch{index:02d}.md` | {chars} | {flag} | {hook} |")
    lines.extend(
        [
            "",
            "## 覆盖检查",
            "",
            f"- 章节数：{len(chapters)}",
            f"- 钩子数：{len(chapters)}",
            "- 钩子覆盖率：100%",
            "- 正文格式：直接投稿版，一句一段；付费节点不在正文显式标注。",
        ]
    )
    (story / "final-chapters" / "_chapters-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_tomato_submission(story: Path, paywall: dict[int, str]) -> None:
    path = story / "tomato-submission.md"
    text = path.read_text(encoding="utf-8").rstrip() if path.exists() else "# 番茄投稿包"
    text = re.sub(
        r"\n+## 付费节点地图（直接投稿版）\n.*$",
        "",
        text,
        flags=re.DOTALL,
    ).rstrip()
    lines = [
        text,
        "",
        "## 付费节点地图（直接投稿版）",
        "",
        "正文不显式标注付费点，节点已自然落在章末或强悬念句上。",
        "",
        "| 节点 | 位置 | 自然卡点 |",
        "|---|---|---|",
    ]
    for idx, (chapter_no, hook) in enumerate(sorted(paywall.items()), start=1):
        lines.append(f"| {idx} | 第 {chapter_no} 章末 | {hook} |")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def append_craft_note(story: Path) -> None:
    path = story / "craft-notes.md"
    text = path.read_text(encoding="utf-8").rstrip() if path.exists() else "# Craft Notes"
    marker = "## 直接投稿版优化记录"
    if marker in text:
        text = re.sub(r"\n+## 直接投稿版优化记录\n.*$", "", text, flags=re.DOTALL).rstrip()
    note = "\n".join(
        [
            "",
            marker,
            "",
            "- 补入开篇导语，标题后即抛出核心冲突和反击承诺。",
            "- 正文统一为一句一段，适配移动端直接投稿阅读节奏。",
            "- 强化付费节点为自然章末悬念，不在正文加入内部标记。",
            "- 投稿包新增付费节点地图，便于审稿时确认卡点分布。",
        ]
    )
    path.write_text(text + note + "\n", encoding="utf-8")


def main() -> int:
    for slug, cfg in CONFIG.items():
        story = ROOT / "stories" / slug
        final_text = (story / "final.md").read_text(encoding="utf-8")
        title, _body = extract_heading(final_text, slug)
        paths = chapter_paths(story)
        chapters = [
            normalize_chapter(path, idx, cfg["paywall"].get(idx))
            for idx, path in enumerate(paths, start=1)
        ]
        rebuild_final(story, title, cfg["lead"], chapters)
        update_chapter_map(story, chapters, cfg["paywall"])
        update_tomato_submission(story, cfg["paywall"])
        append_craft_note(story)
        print(f"{slug}: chapters={len(chapters)} chars={count_nonspace((story / 'final.md').read_text(encoding='utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
