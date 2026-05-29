#!/usr/bin/env bash
# build-corpus.sh -- 从 /Users/dengxianghua/Downloads/4.10/*.txt 构建 corpus/
#
# 本脚本负责:
#   1. 为每篇原文创建 corpus/{slug}/ 目录
#   2. 把原文拷贝为 corpus/{slug}/source.md
#   3. 预创建 analysis/ 子目录
#   4. 维护 corpus/_manifest.tsv (slug ↔ 原文件名映射)
#   5. 初始化 corpus/_index.json 骨架 (由后续 Phase 1 运行填充)
#
# 用法:
#   ./scripts/build-corpus.sh                 # 默认扫描 /Users/dengxianghua/Downloads/4.10
#   ./scripts/build-corpus.sh --src <dir>     # 指定不同的源目录
#   ./scripts/build-corpus.sh --dry-run       # 仅打印会做什么
#
# 产出目录结构:
#   corpus/
#   ├── _manifest.tsv       slug ↔ filename 映射
#   ├── _index.json         汇总索引(待 dissector 填充)
#   └── {slug}/
#       ├── source.md       原文
#       └── analysis/       空目录, 待 Phase 1 产出 beat-sheet/style-dna 等
#
# 后续对每篇 corpus/{slug}/ 单独跑 Phase 1:
#   pipeline.sh --story corpus/{slug} --phase 1

set -euo pipefail

# ---------- 默认 ----------
SRC_DIR="/Users/dengxianghua/Downloads/4.10"
CORPUS_DIR="$(cd "$(dirname "$0")/.." && pwd)/corpus"
DRY_RUN=false

# ---------- 参数 ----------
while [[ $# -gt 0 ]]; do
    case $1 in
        --src)      SRC_DIR="$2"; shift 2 ;;
        --corpus)   CORPUS_DIR="$2"; shift 2 ;;
        --dry-run)  DRY_RUN=true; shift ;;
        -h|--help)
            echo "用法: $0 [--src <dir>] [--corpus <dir>] [--dry-run]"
            echo ""
            echo "默认源目录: /Users/dengxianghua/Downloads/4.10"
            echo "默认 corpus 目录: <仓库根>/corpus"
            exit 0 ;;
        *)  echo "未知参数: $1" >&2; exit 10 ;;
    esac
done

# ---------- 校验 ----------
if [[ ! -d "$SRC_DIR" ]]; then
    echo "错误: 源目录不存在: $SRC_DIR" >&2
    exit 11
fi

# ---------- 工具:生成 slug ----------
# macOS 默认 bash 3.2 不支持 declare -A, 用 case 语句做映射
slug_for() {
    local fn="$1"
    case "$fn" in
        "《不再是你的笼中雀》.txt") echo "ancient_bird_cage" ;;
        "《东瓶西镜放，恨不能遗忘》.txt") echo "ancient_forget_regret" ;;
        "《为高考后能继承千万遗产特寻失踪弟弟》.txt") echo "gaokao_inheritance_brother" ;;
        "《云满春山关残月》.txt") echo "ancient_moon_spring" ;;
        "《因为落水老公没救我我提了离婚》.txt") echo "husband_drowning_divorce" ;;
        "《夫君被断腿后，我摇魔丸爹娘杀疯了》.txt") echo "ancient_mojo_revenge" ;;
        "《她代号深渊》.txt") echo "abyss_codename" ;;
        "《娘亲脱离世界后，父皇悔疯了》.txt") echo "ancient_mother_emperor_regret" ;;
        "《我死后，老公亲手解剖了我的尸体，却没发现我怀孕了》.txt") echo "dead_autopsy_pregnant" ;;
        "《末世让我滚出基地后，所有人都死了》.txt") echo "apocalypse_exile_revenge" ;;
        "《残梦不暖九冬寒》.txt") echo "ancient_be_winter_dream" ;;
        "《物业涨租逼我走，全家撤场让他慌》.txt") echo "property_rent_exit" ;;
        "《盼我流年，花满蹊径》.txt") echo "ancient_sweet_blossom" ;;
        "《纵有星光坠落时》.txt") echo "ancient_starlight_fall" ;;
        "《背尸六年为姐姐治病，我离开后她们疯了》.txt") echo "corpse_six_years_sister" ;;
        "一手捧红的男主播嫌我老，我砸钱转捧更年轻的弟弟.txt") echo "live_streamer_age_revenge" ;;
        "五一订房嫌贵？可我有百人旅游团.txt") echo "hotel_may_100_group" ;;
        "保他30万货还嫌我碍事？我撤单后他悔疯了.txt") echo "logistics_30w_withdraw" ;;
        "天生微醺的我带球跑后，嫁入了百年世家.txt") echo "tipsy_pregnant_ancient_family" ;;
        "姐姐新生之时，是我的死亡之日.txt") echo "sister_rebirth_my_death" ;;
        "愚人节是他的放纵日.txt") echo "fools_day_indulgence" ;;
        "成为高考状元却接到断亲书后，我举报全家被灭门.txt") echo "top_scorer_disown_revenge" ;;
        "我是姐姐的对照组.txt") echo "sister_control_group" ;;
        "我每月给女儿四千，她却只能啃馒头.txt") echo "daughter_4000_bun" ;;
        "我穷得吃不起饭，妈妈却说每月给我三千.txt") echo "poor_mom_3000" ;;
        "春和不负景明.txt") echo "ancient_spring_ming" ;;
        "晚风别忆旧时人.txt") echo "ancient_evening_wind" ;;
        "棠花落尽不相逢.txt") echo "ancient_tang_flower" ;;
        "海关说我的破包是爱马仕，那就按爱马仕赔吧.txt") echo "hermes_customs_package" ;;
        "皇后要遁走.txt") echo "empress_escape" ;;
        "相府假千金一事无成，可她朋友多啊.txt") echo "fake_princess_friends" ;;
        "瞒着老公空降公司，他竟带小三上台官宣，我当场笑疯.txt") echo "airdrop_company_ceo" ;;
        "磕到了！钓系总裁他撩疯了！.txt") echo "ceo_fishing_sweet" ;;
        "老伴在ICU等救命,他拿手术费给宠物狗买墓地.txt") echo "icu_husband_dog_grave" ;;
        "老公给我妈下药后，我杀疯了.txt") echo "husband_drug_mom_revenge" ;;
        "花落月都星已沉.txt") echo "ancient_flower_moon_star" ;;
        "货主坑我超载罚三千，我拉走一吨沉香他疯了.txt") echo "overload_incense_revenge" ;;
        *) echo "" ;;
    esac
}

log() {
    local level="$1"; shift
    echo "[$(date '+%H:%M:%S')] [$level] $*"
}

mkdir -p "$CORPUS_DIR"
MANIFEST="$CORPUS_DIR/_manifest.tsv"
INDEX="$CORPUS_DIR/_index.json"

# 初始化 manifest 表头
if [[ ! -f "$MANIFEST" ]] && ! $DRY_RUN; then
    echo -e "slug\tfilename\tword_count\tstatus" > "$MANIFEST"
fi

# 初始化 index.json 骨架(若不存在)
if [[ ! -f "$INDEX" ]] && ! $DRY_RUN; then
    cat > "$INDEX" <<'EOF'
{
  "_meta": {
    "description": "跨篇章检索索引。每条记录对应 corpus/{slug}/ 一个案例,由 Phase 1 dissector 填充后更新。",
    "schema_version": "1.0",
    "fields": {
      "slug": "目录名",
      "filename": "原文件名",
      "source_path": "corpus/{slug}/source.md 路径",
      "word_count": "原文字数",
      "status": "pending / dissected / validated",
      "genre": "题材枚举(见 workspace.yaml::genre_profiles)",
      "title_formula": "标题公式 T1-T5 或 ancient_couplet",
      "reversal_mechanisms": "反转机制 ID 列表,如 [\"M1\",\"M3\"]",
      "hook_type": "H1-H4",
      "hook_strength": "/10",
      "emotion_curve_shape": "U型 / 双峰型 / 阶梯型 / 其他"
    }
  },
  "entries": []
}
EOF
fi

# ---------- 主流程 ----------
count=0
skipped=0
created=0

while IFS= read -r -d '' filepath; do
    filename=$(basename "$filepath")

    # 查人工映射表
    slug=$(slug_for "$filename")
    if [[ -z "$slug" ]]; then
        # 回退:取文件名前 20 字符 + md5 前 8 位
        md5=$(echo -n "$filename" | md5 -q 2>/dev/null || echo -n "$filename" | md5sum | cut -d' ' -f1)
        slug="auto_${md5:0:8}"
        log "WARN" "文件无人工 slug,使用回退: $filename → $slug"
    fi

    target_dir="$CORPUS_DIR/$slug"
    target_file="$target_dir/source.md"

    if [[ -f "$target_file" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    count=$((count + 1))

    if $DRY_RUN; then
        log "INFO" "[DRY] 将创建: $target_dir (来自 $filename)"
        continue
    fi

    mkdir -p "$target_dir/analysis"
    # 拷贝原文, 顶部加元数据头
    {
        echo "---"
        echo "source_file: \"$filename\""
        echo "slug: \"$slug\""
        echo "imported_at: \"$(date '+%Y-%m-%d %H:%M:%S')\""
        echo "---"
        echo ""
    } > "$target_file"
    cat "$filepath" >> "$target_file"

    # 计算字数(中文字符数近似值)
    word_count=$(wc -m < "$filepath" | tr -d ' ')

    # 追加到 manifest
    echo -e "${slug}\t${filename}\t${word_count}\tpending" >> "$MANIFEST"

    created=$((created + 1))
    log "INFO" "创建 corpus/$slug/ ($word_count 字)"

done < <(find "$SRC_DIR" -maxdepth 1 -type f -name "*.txt" -print0)

log "INFO" "完成: 新建 $created, 跳过 $skipped, 共处理 $count 个文件"
log "INFO" "下一步: 对 corpus/{slug}/ 逐一跑 Phase 1 解构"
log "INFO" "  例: ./pipeline.sh --story corpus/hermes_customs_package --phase 1"
log "INFO" "Phase 1 完成后, 可手工或用 scripts/update-corpus-index.py (待建) 把 dissection.md 数据归入 _index.json"
