import pickle
import re


ALL_CHARACTERS = [5, 29, 48, 51, 59, 140, 168, 183, 205, 210, 219, 228, 242, 248, 271, 283, 284, 292, 306, 335, 337, 345, 358, 380, 396]
MAIN_CHARACTERS = [59, 183, 248, 292, 306, 335]

FIRST_PRONOUN = [
    "나",
    "나하고는",
    "나의",
    "저한테는",
    "나야",
    "나도",
    "나답지",
    "나와",
    "내가...",
    "제가",
    "나!",
    "\"난",
    "나라고",
    "날",
    "저예요",
    "나랑",
    "나한테",
    "나를",
    "내...",
    "나보다",
    "나한테도",
    "나는",
    "나에",
    "나,",
    "\"내가",
    "저한테",
    "나야?",
    "난,",
    "제",
    "저와",
    "내가",
    "내",
    "내게",
    "나보고",
    "저요?",
    "나는...",
    "저는...",
    "나한테는",
    "전",
    "저는",
    "나한텐",
    "난"
]




ENAME_TO_ID = {}
EID_TO_NAME = {}


def get_eid_by_mention(mention, speaker):
    mention = re.sub(r'[^\w]', ' ', mention).replace(' ', '').lower()

    #first-person pronoun match
    if (mention in FIRST_PRONOUN):
        if (speaker in ENAME_TO_ID):
            return ENAME_TO_ID[speaker]

    # all_match
    for ename_key in ENAME_TO_ID:
        r_ename_key = re.sub(r'[^\w]', ' ', ename_key).replace(' ', '').lower()
        if (r_ename_key in mention):
            return ENAME_TO_ID[ename_key]

    # first_name_match
    for ename_key in ENAME_TO_ID:
        names = ename_key.split()
        if (len(names) > 1):
            r_ename_key = re.sub(r'[^\w]', ' ', names[0]).replace(' ', '').lower()
            if (r_ename_key in mention):
                return ENAME_TO_ID[ename_key]
    return 1000


# entity_map
f = open('kor_data/friends_kor_entity_map.txt')

print('aaa')

for line in f:
    print(line.strip().split('\t'))
    eid, ename = line.strip().split('\t')
    eid = int(eid)
    if (eid not in ALL_CHARACTERS):
        continue
    ENAME_TO_ID[ename] = eid
    EID_TO_NAME[eid] = ename
f.close()


# Parse Prediction
with open('evaluate_result.pickle', 'rb') as handle:
    data = pickle.load(handle)
    predict_data2 = data['prediction']

# Parse Gold Data and
#f = open('data/friendsnew.english.v4_gold_conll','r',encoding='utf-8')
f = open('kor_data/friendskortest.english.v4_gold_conll','r',encoding='utf-8')
key = ''
nlp_datas = {}
gold_datas = []

for line in f:
    if ('#begin document' in line):
        #key = line[17:33] + '_' + str(int(line[-3:-1]))
        key = line[17:32] + '_' + str(int(line[-3:-1]))
        nlp_datas[key] = []
    elif ('#end document' not in line and len(line) > 1):
        items = line.strip().split()
        nlp_datas[key].append({'word':items[3],
                                'lemma':items[6],
                                'speaker': items[9].replace('_',' ')})

        entityid = items[-1]
        if ('(' in entityid):
            gold_datas.append({'st':len(nlp_datas[key]) - 1,
                               'en':-1,
                               'entityid':int(entityid.replace('(','').replace(')','')),
                               'doc_key':key})
        if (')' in entityid):
            gold_datas[-1]['en'] = len(nlp_datas[key]) - 1
f.close()

gold_datas2 = []
nlp_datas2 = {}

predict_data = {}
f = open('evaluate_result.txt','r',encoding='utf-8')
for line in f:
    if ('#begin document' in line):
        #key = line[17:33] + '_' + str(int(line[-3:-1]))
        key = line[17:32] + '_' + str(int(line[-3:-1]))
        nlp_datas2[key] = []
        predict_data[key] = []

    elif ('#end document' not in line and len(line) > 1):
        items = line.strip().split()
        nlp_datas2[key].append({'word':items[3],
                                'lemma':items[6],
                                'speaker': items[9].replace('_',' ')})

        entityid = items[-1]
        if ('(' in entityid):
            predict_data[key].append({'st':len(nlp_datas2[key]) - 1,
                               'en':-1,
                               'entityid':int(entityid.replace('(','').replace(')',''))})
        if (')' in entityid):
            predict_data[key][-1]['en'] = len(nlp_datas2[key]) - 1
f.close()

cluster_data = {}
for doc_key, mention_list in predict_data.items():
    max_idx = -1
    for men in mention_list:
        if men['entityid'] > max_idx:
            max_idx = men['entityid']
    cluster_data[doc_key] = []
    for i in range(max_idx+1):
        cluster_data[doc_key].append([])

    for men in mention_list:
        cluster_data[doc_key][int(men['entityid'])].append((men['st'],men['en']))

# majority voting
for doc_key, cluster_list in cluster_data.items():
    for cluster_idx,cluster in enumerate(cluster_list):
        eid_list = []
        for i,boundary in enumerate(cluster):
            st = boundary[0]
            en = boundary[1]
            speaker = nlp_datas[doc_key][st]['speaker']
            mention = ''
            for j in range(st,en+1):
                mention = mention + nlp_datas[doc_key][j]['word'] + ' '
            mention = mention.strip()

            inferred_eid = get_eid_by_mention(mention,speaker)
            if (inferred_eid < 1000):
                eid_list.append(inferred_eid)

        # set most common id to cluster id, unless all are 0
        cluster_eid =  max(set(eid_list), key=eid_list.count) if len(eid_list) > 0 else 1000
        cluster_data[doc_key][cluster_idx] = {'cluster_eid':cluster_eid,
                                              'cluster':cluster}

f_out = open('kor_data/sys_kor.out','w',encoding='utf-8')
for index,item in enumerate(gold_datas):
    doc_key = item['doc_key']
    st = item['st']
    en = item['en']
    speaker = nlp_datas[doc_key][st]['speaker']
    mention = ''
    for j in range(st, en + 1):
        mention = mention + nlp_datas[doc_key][j]['word'] + ' '
    mention = mention.strip()

    e_id = -1
    for cluster in cluster_data[doc_key]:
        for boundary in cluster['cluster']:
            if (boundary[0] == st and boundary[1] == en):
                e_id = cluster['cluster_eid']
                break
        if (e_id >= 0):
            break
    if (e_id < 0):
        e_id = get_eid_by_mention(mention, speaker)

    f_out.write(str(e_id))
    if (index < len(gold_datas)-1):
        f_out.write('\n')

f.close()
