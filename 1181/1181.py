n = int(input())

lst = [input() for _ in range(n)]

# �ߺ� ���� ��, ���� -> ������ ����
# sorted() �� .sort() �� key �Լ��� ��ȯ�ϴ� ���� �������� �������� ����
# �� key �Լ��� ������ �� ��� x�� ���� Ʃ�� (len(x), x) �� ��ȯ
# ù ��° ��ҵ��� �� �� �ٸ��� �̰ɷ� ���� ����
# ù ��° ��ҵ��� ������ �� �� ��° ��ҵ��� ��

lst = sorted(set(lst), key=lambda x: (len(x), x))

for word in lst:
    print(word)