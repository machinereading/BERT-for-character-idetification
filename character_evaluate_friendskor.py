import os
import sys
import argparse
from collections import Counter


OTHER = -1
MAIN = [59, 183, 248, 292, 306, 335]
TRAIN_ALL = [5, 29, 48, 51, 59, 140, 168, 183, 205, 210, 219, 228, 242, 248, 271, 283, 284, 292, 306, 335, 337, 345, 358, 380, 396]
ENTITY_LIST = [
"애비",
"알",
"알 코스텔릭",
"알 민세르",
"알 파치노",
"알란",
"알버트 아인슈타인",
"알렉스",
"모두",
"앰버",
"앰거",
"앤디 맥도웰",
"안드",
"안드레",
"안드레아",
"안드레아의 친구",
"앤드류",
"안젤라 델베키오",
"애나벨",
"아르텔레",
"애슐리",
"에드나 숙모",
"아이리스 숙모",
"릴리안 숙모",
"필리스 숙모",
"실 숙모",
"오로라",
"에이버리",
"바바라",
"배리",
"벤",
"버니 스펠만",
"베스트맨",
"베델",
"베티",
"빅 불리",
"빌 클린턴",
"빌리 드레스킨의 아빠",
"빌리 드레스킨",
"빙",
"비숍 투투",
"블랙 바트",
"밥",
"바비 러쉬",
"보스 빙",
"브래드",
"브레브먼",
"브렌트 무스버거",
"브라이언",
"브리타니",
"칼",
"캐롤 윌릭",
"캐롤과 수잔의 음식 제공자",
"캐롤의 할머니",
"캐롤라인",
"케이시",
"캐스팅 가이",
"케이시 베이츠",
"실리아",
"챈들러 빙",
"챈들러의 데이트상대",
"챈들러의 데이트상대의 남편",
"챈들러의 데이트상대의 남편의 비서",
"챈들러의 전여자친구",
"챈들러의 여자친구",
"챈들러의 상상 속 친구",
"챈들러의 비서",
"찰스 빙",
"크리시",
"크리스틴",
"코마남",
"손님",
"다몬",
"댄",
"다나",
"다니엘",
"대니 아르샥",
"다릴 한나",
"데이브 토마스",
"데이빗 핫셀호프",
"뎁",
"데비",
"데브라",
"디",
"데미 무어",
"데니스 디마르코",
"딕 클락",
"딜런",
"감독",
"감독의 보조",
"도나 리드",
"도로시",
"발다라 박사",
"베이지다 박사",
"라모레이 박사",
"플린 박사",
"프란즈블라우 박사",
"호튼 박사",
"미첼 박사",
"오버만 박사",
"르모레 박사",
"로즌 박사",
"웡 박사",
"드류 베리모어",
"더들리 무어",
"던컨",
"에드",
"에드 베글리",
"에디",
"에디 미노윅",
"에디 모스코위치",
"에디의 전여자친구",
"에디의 전룸메이트",
"엠마",
"에릭 에스트라다",
"에릭 프라우어",
"에릭 포드",
"어네스트 보그나인",
"에르",
"에러",
"에스텔",
"에스텔 레나드",
"에스더 리빙스턴",
"이던",
"에벌린 더머",
"유잉",
"가짜 모니카",
"플레쉬맨",
"플린치",
"비행기 탑승객",
"플로렌스 헨더슨",
"포그혼 레그혼",
"프랭크 부페이",
"프랭키",
"프래니",
"프로이트",
"바비",
"게일",
"조지",
"조지 베일리",
"조지 스테파노폴로스",
"소녀",
"소녀들",
"글로리아 트리비아니",
"할머니",
"건터",
"사내",
"사내 1",
"사내들",
"한니발 렉터",
"헬렌",
"헨리",
"옴브레맨",
"하워드",
"휴이 루이스",
"휴 그랜트",
"잉그리드 버그만",
"인터컴",
"인터뷰어",
"아이브",
"잭",
"잭 1",
"잭 2",
"잭 겔러",
"제이드",
"제임스 본드",
"제이미",
"제인",
"제니스",
"제니터",
"제이슨 카스탈라노",
"제이슨 헐리",
"제이 레노",
"지니",
"질",
"질 구데이커",
"질 그린",
"177 질의 엄마",
"짐 크로치",
"지미 하우저",
"조안 콜린즈",
"조안나",
"조안나의 아빠",
"조이 트리비아니",
"조이 트리비아니 경",
"조이의 동료",
"조이의 사촌",
"조이의 데이트상대",
"조이의 데이트상대의 친구",
"조이의 재단사",
"존 세비지",
"존 보잇",
"조니 샤피로",
"조디",
"조셉 스탈린",
"주디 겔러",
"주디 젯슨",
"줄리",
"줄리의 친구",
"카렌",
"꼬마",
"킵",
"크리스틴 1",
"로리 스케이퍼",
"레온",
"레오나드 그린",
"리로이",
"레슬리",
"리암 니슨",
"립슨",
"릴리 부페이",
"린다",
"립슨 1",
"Little Bully",
"리지",
"로라",
"로리",
"론 그린",
"로레인",
"로웰",
"루이사",
"루이사의 상사",
"리디아",
"리디아의 아기",
"리디아의 남편",
"리디아의 엄마",
"말리부 켄",
"남자",
"남자 1",
"남자 2",
"마르셀",
"마르셀 마르소",
"마크",
"마르샤",
"마티",
"메리 타일러 무어",
"맥스",
"멜라니",
"메시에",
"마이클",
"미셸",
"밀튼",
"민디",
"미라",
"미스 부페이",
"까다로운 여자",
"미스 키티",
"모니카",
"모니카 겔러",
"모니카의 전남자친구",
"모니카의 할머니",
"몰리 세이퍼",
"252 마더 테레사",
"무버",
"에이들맨 씨",
"클린 씨",
"더글라스 씨",
"그린 씨",
"헤클스 씨",
"피넛 씨",
"래스태터 씨",
"로저 씨",
"로퍼 씨",
"솔티 씨",
"트리거 씨",
"트리비아니 씨",
"와인버그 씨",
"에이들맨 부인",
"빙 부인",
"부페인 부인",
"콥 부인",
"겔러 부인",
"그린 부인",
"그린 부인 1",
"트리비아니 부인",
"월레스 부인",
"월레스 부인의 여동생",
"와인버그 부인",
"미스 토마스",
"네이선",
"니나 부크바인더",
"노르만 메일러",
"간호사",
"파올로",
"폴",
"폴의 전부인",
"파울라",
"파울로",
"사람 1",
"사람 2",
"피트",
"피트 카니",
"피비 부페이",
"피비 그리고 레이첼",
"피비의 보조",
"피비의 친구들",
"피비의 남자친구",
"피비의 데이트상대",
"피비의 친구",
"피비의 할머니",
"피비의 할머니의 남자친구",
"피비의 미용사",
"피비의 의붓아빠",
"피비, 조이, 그리고 로스",
"피자 가이",
"제작자",
"레이첼 그린",
"레이첼 그리고 피비",
"레이첼의 데이트상대",
"레이첼의 친구",
"레이첼의 인터뷰어",
"레이첼의 인터뷰어의 사촌",
"레이첼의 여동생",
"라디오",
"라몬",
"랜디 브라운",
"접수원",
"리차드",
"리차드 버크",
"리차드의 아들",
"릭",
"밥",
"롭 도난",
"롭 로이",
"로비",
"로버트 필만",
"로드 스티저",
"로드니 맥도웰",
"로드리고",
"로저",
"롤랜드",
"로나",
"로니 라팔로노",
"로즈",
"로즈 마리",
"로스 겔러",
"로스의 데이트상대",
"로스의 할머니",
"러스",
"라이언",
"산드라 그린",
"샌디",
"스캇 알렉산더",
"보안 요원",
"새논 쿠퍼",
"쉘리",
"쉬얼리",
"시드니 막스",
"실비안",
"수피 세일",
"스파이크 리",
"스테이시 로스",
"스태피 그래프",
"스텔라 니드먼",
"스테파니",
"스티브",
"상점 가이",
"외부인",
"수잔 번치",
"수잔 살라도레",
"수지",
"타냐",
"문신 예술가",
"선생님",
"테리",
"가이들",
"전체 파티",
"틸리",
"티나",
"티나의 남편",
"토비",
"타미 롤러슨",
"토니",
"토니 디마르코",
"토니 랜달",
"토바 보그나인",
"트레이시",
"트레이너",
"트레비스",
"Tso",
"못난이 벌거숭이",
"우마 서먼",
"프레디 이모부",
"살 삼촌",
"살 삼촌의 부인",
"언더독",
"언노운",
"우르술라",
"반담",
"비달 부페이",
"웨이터",
"웨이트리스",
"워렌 비티",
"웨딩 플래너",
"웬디",
"위브",
"여자",
"여자 1",
"야마구치",
"야스민 블릭",
"젊은 이던"
]



main_entities = set(MAIN + [OTHER])
all_entities  = set(TRAIN_ALL + [OTHER])

def parse_key_file(filepath):
    with open(filepath, "rb") as f:
        keys = []
        for line in f:
            line = line.strip()
            if not line: return keys
            try:
                keys.append(int(line))
            except ValueError:
                print('Invalid key: "'+line+'" in '+filepath)
                return None
        return keys
    return None

def measure_macro_f1(entities, correct_counts, auto_counts, gold_counts):
    f1s = dict()
    for entity in entities.intersection(gold_counts.keys()):
        if correct_counts[entity] != 0:
            p = float(correct_counts[entity]) / auto_counts[entity]
            r = float(correct_counts[entity]) / gold_counts[entity]
            f1s[entity] = [p, r, 2.0 * p * r / (p + r)]
        else:
            f1s[entity] = [0.0] * 3;
    return f1s

def main():
    #parser = argparse.ArgumentParser(description="SemEval 2018 Task 4: Character Identification Evaluation Script")
    #parser.add_argument("ref_out",  type=str, help="Path to the input directory that contains ref/answer.txt and res/answer.txt, that are the gold and the system output files")
    #parser.add_argument("sys_out", type=str, help="Path to the output directory where scores.txt will be saved")
    #args = parser.parse_args()

    # read key files
    gold_file = 'kor_data/ref_kor.out'#os.path.join(args.ref_out)
    auto_file = 'kor_data/sys_kor.out'#os.path.join(args.sys_out)
    gold_keys = parse_key_file(gold_file)
    auto_keys = parse_key_file(auto_file)

    if not auto_keys:
        return

    if len(gold_keys) != len(auto_keys):
        print('Key mismatch: gold = %d keys, system = %d keys' % (len(gold_keys), len(auto_keys)))
        return

    # count correct entities
    main_correct     = Counter()
    all_correct      = Counter()
    gold_main_counts = Counter()
    gold_all_counts  = Counter()
    auto_main_counts = Counter()
    auto_all_counts  = Counter()

    for auto_key, gold_key in zip(auto_keys, gold_keys):
        # all entities
        auto_all_key = auto_key if auto_key in all_entities else OTHER
        gold_all_key = gold_key if gold_key in all_entities else OTHER

        auto_all_counts[auto_all_key] += 1
        gold_all_counts[gold_all_key] += 1
        if auto_all_key == gold_all_key: all_correct[auto_all_key] += 1

        # main + other entities
        auto_main_key = auto_key if auto_key in main_entities else OTHER
        gold_main_key = gold_key if gold_key in main_entities else OTHER

        auto_main_counts[auto_main_key] += 1
        gold_main_counts[gold_main_key] += 1
        if auto_main_key == gold_main_key: main_correct[auto_main_key] += 1

    # measure label accuracy
    total_count = len(gold_keys)
    all_accuracy  = float(sum(all_correct.values()))  / total_count
    main_accuracy = float(sum(main_correct.values())) / total_count

    # measure macro F1 scores
    all_f1  = measure_macro_f1(all_entities, all_correct, auto_all_counts, gold_all_counts)
    main_f1 = measure_macro_f1(main_entities, main_correct, auto_main_counts, gold_main_counts)

    all_avg_f1  = float(sum([prf[2] for prf in all_f1.values()]))  / len(all_f1)  if len(all_f1)  > 0 else 0.0
    main_avg_f1 = float(sum([prf[2] for prf in main_f1.values()])) / len(main_f1) if len(main_f1) > 0 else 0.0

    # print evaluation
    eval = [
        '********** Main + Other Entities **********',
        'Label Accuracy  : %6.2f (%d/%d)' % (100.0 * main_accuracy, sum(main_correct.values()), total_count),
        'Average Macro F1: %6.2f' % (100.0 * main_avg_f1),
        '************** All Entities ***************',
        'Label Accuracy  : %6.2f (%d/%d)' % (100.0 * all_accuracy, sum(all_correct.values()), total_count),
        'Average Macro F1: %6.2f' % (100.0 * all_avg_f1)]

    eval.append('***** Main + Other Entities F1 Scores *****')
    for key in sorted(main_f1.keys()):
        prf = main_f1[key]
        name = ENTITY_LIST[key] if key >= 0 else '##OTHERS##'
        s = '%40s: P = %6.2f (%4d/%4d), R = %6.2f (%4d/%4d), F1 = %6.2f' % (name, prf[0] * 100.0, main_correct[key], auto_main_counts[key], prf[1] * 100.0, main_correct[key], gold_main_counts[key], prf[2] * 100.0)
        eval.append(s)

    eval.append('********* All Entities F1 Scores **********')
    for key in sorted(all_f1.keys()):
        prf = all_f1[key]
        name = ENTITY_LIST[key] if key >= 0 else '##OTHERS##'
        s = '%40s: P = %6.2f (%4d/%4d), R = %6.2f (%4d/%4d), F1 = %6.2f' % (name, prf[0] * 100.0, all_correct[key], auto_all_counts[key], prf[1] * 100.0, all_correct[key], gold_all_counts[key], prf[2] * 100.0)
        eval.append(s)

    print('\n'.join(eval))
    # fout = open(os.path.join(args.output_dir, 'scores.txt'), 'w')
    # fout.write('accuracy:{0}\n'.format(100.0 * all_avg_f1))
    # fout.close()

    return all_accuracy, main_accuracy, all_avg_f1, main_avg_f1

if __name__ == "__main__":
    main()
