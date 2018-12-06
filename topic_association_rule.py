import pandas
import json
from apyori import apriori


# 数据导入和处理
with open('spider/data/user_following_topics.txt', 'r') as f:
    data = f.readlines()
    array = []
    for user in data:
        info = json.loads(user)
        if info['type'] == 'people':
            array.append({
                'id': info['id'],
                'name': info['name'],
                'following_topic_count': info['following_topic_count'],
                'following_topics': [item['title'] for item in info['following_topics']]
                })
df = pandas.DataFrame(array)
df = df[(df['following_topic_count'] != 0) & (len(df['following_topics']) > 0)]
df['rate'] = len(df['following_topics'])/df['following_topic_count']
df = df[df['rate'] > 0.8]
print(df.info())

# 关联规则分析
transactions = df['following_topics'].values
rules = apriori(transactions, min_support=0.03, min_confidence=0.5, min_lift=3, min_length=2)
results = list(rules)
for rec in results:
    for base, add  in [(i.items_base, i.items_add)  for i in rec.ordered_statistics]:
        items_base = '，'.join(base)
        items_add = '，'.join(add)
        print('已关注话题： {:\u3000<20} 推荐话题： {:<10}'.format(items_base, items_add))

