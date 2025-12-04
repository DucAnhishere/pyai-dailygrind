SERVER="192.168.80.25"
USER="a4000"
REMOTE_BASE="/home/a4000/Data/tung/Datasets/Classification/car_corner_classification_01"
LOCAL_BASE="/Users/testadmin/Desktop/Desktop-Mac/Python/data/car-corner"

MAINS=("train" "test" "val")
SUBS=("45_phai_sau" "45_phai_truoc" "45_trai_sau" "45_trai_truoc" "phai_sau_toan_canh" "phai_toan_canh" "phai_truoc_toan_canh" "sau_toan_canh" "trai_sau_toan_canh" "trai_toan_canh" "trai_truoc_toan_canh" "truoc_toan_canh")

# Total images parameter
TOTAL_IMAGES=6000

# Ratios: Train 75%, Val 12.5%, Test 12.5% (using integer fractions)
TOTAL_TRAIN=$(( TOTAL_IMAGES * 3 / 4 ))
TOTAL_VAL=$(( TOTAL_IMAGES / 8 ))
TOTAL_TEST=$(( TOTAL_IMAGES - TOTAL_TRAIN - TOTAL_VAL ))

# Images per subfolder (12 subfolders per main)
TRAIN_COUNT=$(( TOTAL_TRAIN / 12 ))
VAL_COUNT=$(( TOTAL_VAL / 12 ))
TEST_COUNT=$(( TOTAL_TEST / 12 ))

echo "Total images: $TOTAL_IMAGES"
echo "Train: $TOTAL_TRAIN images ($TRAIN_COUNT per subfolder)"
echo "Val: $TOTAL_VAL images ($VAL_COUNT per subfolder)"
echo "Test: $TOTAL_TEST images ($TEST_COUNT per subfolder)"

for main in "${MAINS[@]}"; do
  if [ "$main" = "train" ]; then
    COUNT=$TRAIN_COUNT
  elif [ "$main" = "val" ]; then
    COUNT=$VAL_COUNT
  else
    COUNT=$TEST_COUNT
  fi
  
  for sub in "${SUBS[@]}"; do
    REMOTE_DIR="$REMOTE_BASE/$main/$sub"
    LOCAL_DIR="$LOCAL_BASE/$main/$sub"

    mkdir -p "$LOCAL_DIR"

    # Use xargs with -P for parallel downloads (4 threads)
    ssh "$USER@$SERVER" "ls '$REMOTE_DIR' | head -$COUNT" | xargs -I {} -P 4 scp "$USER@$SERVER:$REMOTE_DIR/{}" "$LOCAL_DIR/"
  done
done

echo "Download complete!"