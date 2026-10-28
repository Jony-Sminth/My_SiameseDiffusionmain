import os, glob, re
import numpy as np

RESULT_DIR = os.path.expanduser("~/seg_experiments_leakfree/results")
OUT = os.path.expanduser("~/seg_experiments_leakfree/SUMMARY.md")

# 存储结果的数据结构
results = {}

for path in glob.glob(os.path.join(RESULT_DIR, "*_result.txt")):
    exp_name = os.path.basename(path).replace("_result.txt", "")
    
    # 解析结果文件
    with open(path) as f:
        content = f.read()
    dice = float(re.search(r"Dice=([\d.]+)", content).group(1))
    iou  = float(re.search(r"IoU=([\d.]+)", content).group(1))
    hd95 = float(re.search(r"HD95=([\d.]+)", content).group(1))
    
    # 提取实验组（去掉 seed 部分，用于分组计算）
    # 例如 LKF-N80_s42_seed1_ours -> LKF-N80_s42_ours
    group_name = re.sub(r"seed\d+_", "", exp_name)
    
    if group_name not in results:
        results[group_name] = []
    
    results[group_name].append({
        "exp": exp_name,
        "dice": dice,
        "iou": iou,
        "hd95": hd95
    })

with open(OUT, "w") as f:
    f.write("# 纯净隔离版 (Leak-Free) 实验结果汇总\n\n")
    
    f.write("## 📊 均值与标准差 (Mean ± Std)\n\n")
    f.write("| 实验组 | 样本数 (Seeds) | Dice ↑ | IoU ↑ | HD95 ↓ |\n")
    f.write("|---|---|---|---|---|\n")
    
    for group in sorted(results.keys()):
        data = results[group]
        dices = [d["dice"] for d in data]
        ious  = [d["iou"] for d in data]
        hd95s = [d["hd95"] for d in data]
        
        f.write(f"| **{group}** | {len(data)} | "
                f"{np.mean(dices):.4f} ± {np.std(dices):.4f} | "
                f"{np.mean(ious):.4f} ± {np.std(ious):.4f} | "
                f"{np.mean(hd95s):.2f} ± {np.std(hd95s):.2f} |\n")
    
    f.write("\n---\n\n")
    f.write("## 📝 详细种子记录\n\n")
    f.write("| 实验 ID | Dice | IoU | HD95 |\n")
    f.write("|---|---|---|---|\n")
    
    for group in sorted(results.keys()):
        for d in sorted(results[group], key=lambda x: x["exp"]):
            f.write(f"| {d['exp']} | {d['dice']:.4f} | {d['iou']:.4f} | {d['hd95']:.2f} |\n")

print(f"✅ 汇总已写入: {OUT}")
print(f"✅ 共处理了 {sum(len(v) for v in results.values())} 个结果文件")
