# BERT for Character Identification

[BERT for Coreference Resolution: Baselines and Analysis](https://arxiv.org/abs/1908.09091) 를 기반으로 한 인물 식별 모델입니다.

## Task Definition

-

## Datasets

-

### Format

All datasets follow the CoNLL 2012 Shared Task data format. Documents are delimited by the comments in the following format:

```
#begin document (<Document ID>)[; part ###]
...
#end document
```

Each sentence is delimited by a new line ("\n") and each column indicates the following:

1. Document ID: `/-` (e.g., `/friends-s01e01`).
2. Scene ID: the ID of the scene within the episode.
3. Token ID: the ID of the token within the sentence.
4. Word form: the tokenized word.
5. Part-of-speech tag: the part-of-speech tag of the word (auto generated).
6. Constituency tag: the Penn Treebank style constituency tag (auto generated).
7. Lemma: the lemma of the word (auto generated).
8. Frameset ID: not provided (always `_`).
9. Word sense: not provided (always `_`).
10. Speaker: the speaker of this sentence.
11. Named entity tag: the named entity tag of the word (auto generated).
12. Start time: start time of the sentence on video. (millisecond)
13. End time: start time of the sentence on video. (millisecond)
14. Video file: Pre-processed sequence of image file from the video corresponding to the sentence. This column represents the file name of the pickle object (Pickle object will be released on 08/01)
15. Entity ID: the entity ID of the mention, that is consistent across all documents.

Here is a sample from the training dataset:

```
/friends-s01e01  0  0  He     PRP   (TOP(S(NP*)    he     -  -  Monica_Geller   *  55422 59256 00005.pickle (284)
/friends-s01e01  0  1  's     VBZ          (VP*    be     -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  2  just   RB        (ADVP*)    just   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  3  some   DT        (NP(NP*    some   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  4  guy    NN             *)    guy    -  -  Monica_Geller   *  55422 59256 00005.pickle (284)
/friends-s01e01  0  5  I      PRP  (SBAR(S(NP*)    I      -  -  Monica_Geller   *  55422 59256 00005.pickle (248)
/friends-s01e01  0  6  work   VBP          (VP*    work   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  7  with   IN     (PP*))))))    with   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  8  !      .             *))    !      -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  0  C'mon  VB   (TOP(S(S(VP*))  c'mon  -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  1  ,      ,                 *  ,      -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  2  you    PRP           (NP*)  you    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle (248)
/friends-s01e01  0  3  're    VBP            (VP*  be     -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  4  going  VBG            (VP*  go     -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  5  out    RP           (PRT*)  out    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  6  with   IN             (PP*  with   -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  7  the    DT             (NP*  the    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  8  guy    NN            *))))  guy    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle (284)
/friends-s01e01  0  9  !      .               *))  !      -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
```

A mention may include more than one word:

```
/friends-s01e02  0  0  Ugly         JJ   (TOP(S(NP(ADJP*  ugly         -  -  Chandler_Bing  *  332158 334460 00038.pickle (380
/friends-s01e02  0  1  Naked        JJ                *)  naked        -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  2  Guy          NNP               *)  Guy          -  -  Chandler_Bing  *  332158 334460 00038.pickle 380)
/friends-s01e02  0  3  got          VBD             (VP*  get          -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  4  a            DT              (NP*  a            -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  5  Thighmaster  NN               *))  thighmaster  -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  6  !            .                *))  !            -  -  Chandler_Bing  *  332158 334460 00038.pickle -
```

The mapping between the entity ID and the actual character can be found in [`friends_entity_map.txt`]( https://github.com/machinereading/BERT-for-character-idetification/blob/master/data/friendsnew_entity_map.txt )

## Setup

- Install python3 requirements: `pip install -r requirements.txt`
- `./setup_all.sh`: This builds the custom kernels



## Train

- data 폴더 내에 train, dev, test data set을 각각 `friendstrain.english.v4_gold_conll` `friendstrain.english.v4_gold_conll` `friendstrain.english.v4_gold_conll` 로 저장
- data 폴더 내에 `friends_entity_map.txt`를 확인.
- models 폴더 내에 BERT 모델을 다운로드.
- `./setup_training.sh`: sh파일 내에 vocab_file 경로가 올바른지 확인 한 후 실행.
-  Experiment configurations을 ` experiments.conf `에 설정.
-  Training: `GPU=0 python train.py <experiment>` 



## Evaluation

- evaluate를 진행할 모델을 복사.
- ` experiments.conf ` 내에 복사된 이름의 experiment를 설정.
-  `GPU=0 python evaluate.py <experiment> `.  
- 생성된 `evaluate_result.txt`로 결과 확인.
- `python link_character_friendsnew.py`, `python character_evaluate_friendsnew.py` 실행을 통해 인물인식 성능을 확인.