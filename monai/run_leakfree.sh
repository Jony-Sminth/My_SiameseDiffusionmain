#!/bin/bash
# 激活环境
source ~/miniconda3/etc/profile.d/conda.sh
conda activate xcontrol

# 全新的隔离输出目录
RESULT_DIR="$HOME/seg_experiments_leakfree/results"
CKPT_DIR="$HOME/seg_experiments_leakfree/checkpoints"
LOG_DIR="$HOME/seg_experiments_leakfree/logs"
mkdir -p "$RESULT_DIR" "$CKPT_DIR" "$LOG_DIR"

# 设定要跑的 N（你可以改成 20, 40, 80, 100）
N=80

echo "======== 开始纯净版 N=${N} Ours 实验 (10 seeds) ========"
for SEED in {1..10}; do
    python train_seg.py \
      --exp_id "LKF-N${N}_s42_seed${SEED}_ours" \
      --data_root ~/isic2016_downstream \
      --n_real ${N} --out_channels 1 \
      --seed $SEED \
      --use_ours_gen \
      --result_dir "$RESULT_DIR" \
      --checkpoint_dir "$CKPT_DIR" \
      --log_dir "$LOG_DIR"
done
