#GPU=0 python train.py f25
#GPU=1 python train.py f30

GPU=0 python evaluate.py f10-test
python link_character_friendsnew.py
python character_evaluate_friendsnew.py >> 10.txt
