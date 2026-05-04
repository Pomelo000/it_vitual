import os
import cv2
import subprocess
from pathlib import Path
from ultralytics import YOLO

VIDEO_PATH = r'C:\Users\Alety\Desktop\ld.mp4' 
PROJECT_ROOT = Path(r'C:\Users\Alety\Desktop\YOLO\ultralytics-main')
AUTO_LABEL_DIR = Path(r'C:\Users\Alety\Desktop\auto_label')

#改名
CLASSES = ['ld'] 

# 路径
TRAIN_SCRIPT = PROJECT_ROOT / 'project' / 'demo.py'
YAML_PATH = AUTO_LABEL_DIR / 'train.yaml'
DATASET_DIR = AUTO_LABEL_DIR / 'dataset'
IMAGES_DIR = DATASET_DIR / "images"
LABELS_DIR = DATASET_DIR / "labels"
SEED_MODEL = PROJECT_ROOT / 'runs' / 'detect' / 'debug_run' / 'weights' / 'best.pt'

def setup_config_and_fix_labels():
    """改名中···"""
    print(f"同步YAML配置: {YAML_PATH}")
    yaml_content = f"""
path: {DATASET_DIR.as_posix()}
train: images
val: images
nc: {len(CLASSES)}
names: {CLASSES}
"""
    with open(YAML_PATH, 'w', encoding='utf-8') as f:
        f.write(yaml_content.strip())

    print("标签索引纠错与classes.txt配置")
    txt_files = list(LABELS_DIR.glob("*.txt"))
    for txt_file in txt_files:
        if txt_file.name == "classes.txt":
            with open(txt_file, "w", encoding="utf-8") as f:
                f.write("\n".join(CLASSES))
            continue
        
      
        if txt_file.stat().st_size > 0:
            lines = []
            with open(txt_file, "r") as f:
                for line in f:
                    parts = line.split()
                    if parts:
                        parts[0] = "0" 
                        lines.append(" ".join(parts))
            with open(txt_file, "w") as f:
                f.write("\n".join(lines))
            
    cache_file = DATASET_DIR / "labels.cache"
    if cache_file.exists():
        os.remove(cache_file)
    print("缓存清理")

def auto_pipeline():
    # ---初始化---
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    LABELS_DIR.mkdir(parents=True, exist_ok=True)

    # ---抽帧---
    if not any(IMAGES_DIR.iterdir()):
        print("启动抽帧")
        cap = cv2.VideoCapture(VIDEO_PATH)
        count, saved_count = 0, 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            if count % 10 == 0:
                name = f"tower_monitor_{saved_count:05d}.jpg" 
                cv2.imwrite(str(IMAGES_DIR / name), frame)
                saved_count += 1
            count += 1
        cap.release()
        print(f"抽帧完成，生成 {saved_count} 张图片")
    else:
        print("images文件夹不为空，跳过抽帧。")

    # --- 阶段 2: 自动化死锁检测与点火 -------------------------ai
    setup_config_and_fix_labels() 
    
    # 检查手动标注
    valid_manual_labels = [f for f in LABELS_DIR.glob("*.txt") if f.name != 'classes.txt' and f.stat().st_size > 0]
    
    if not SEED_MODEL.exists():
        if len(valid_manual_labels) == 0:
            print("\n\033[91m🛑 [停止] 自动标注引擎点火失败！\033[0m")
            print(f"👉 请先打开 LabelImg，标 10 张图并保存到: {LABELS_DIR}")
            print("👉 确认生成的 .txt 文件里有内容（不是 0KB）。")
            return # 关键死锁：没标图绝对不许往下跑````````````````````````````````````````````````
        else:
            print(f"🔥 检测到 {len(valid_manual_labels)} 张有效手标数据，开始自动训练种子模型...")
            subprocess.run(['python', 'demo.py'], cwd=str(TRAIN_SCRIPT.parent), check=True)

    # 阶段3：---全量标注 ---
    if SEED_MODEL.exists():
        print("刷标签")
        model = YOLO(str(SEED_MODEL))
        for img_path in IMAGES_DIR.glob('*.jpg'):
            label_path = LABELS_DIR / f"{img_path.stem}.txt"
            if not label_path.exists() or label_path.stat().st_size == 0:
                results = model.predict(str(img_path), conf=0.5, verbose=False)
                if len(results[0].boxes) > 0:
                    results[0].save_txt(str(label_path))
        print(f"✅ 自动标注结束")

    # --- 阶段 4：全量训练
    print("🔥 [3/4] 启动正式训练...")
    subprocess.run(['python', 'demo.py'], cwd=str(TRAIN_SCRIPT.parent), check=True)
    print("🎉 [4/4] 流程圆满结束！")

if __name__ == "__main__":
    auto_pipeline()