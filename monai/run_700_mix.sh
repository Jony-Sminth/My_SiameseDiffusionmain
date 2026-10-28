#!/bin/bash
cd ~/SiameseDiffusionmain/monai
source ~/miniconda3/etc/profile.d/conda.sh
conda activate xcontrol

RESULT_DIR="$HOME/seg_experiments_leakfree/results"
CKPT_DIR="$HOME/seg_experiments_leakfree/checkpoints"
LOG_DIR="$HOME/seg_experiments_leakfree/logs"
mkdir -p "$RESULT_DIR" "$CKPT_DIR" "$LOG_DIR"

for SEED in 1 2 3; do
    echo "======== 跑 N=700 纯真实 V2 (Seed $SEED) ========"
    python train_seg.py \
      --exp_id "LKF-N700_V2_seed${SEED}_real" \
      --data_root ~/isic2016_downstream \
      --n_real 700 --out_channels 1 \
      --seed $SEED \
      --result_dir "$RESULT_DIR" --checkpoint_dir "$CKPT_DIR" --log_dir "$LOG_DIR"
      
    echo "======== 跑 N=700真+700生成 V2 (Seed $SEED) ========"
    python train_seg.py \
      --exp_id "LKF-N700_V2_seed${SEED}_mix_ours" \
      --data_root ~/isic2016_downstream \
      --n_real 700 --out_channels 1 \
      --seed $SEED \
      --use_ours_gen \
      --result_dir "$RESULT_DIR" --checkpoint_dir "$CKPT_DIR" --log_dir "$LOG_DIR"
done
