# douban movie spider
A douban movie spider using gevent+requests+BeautifulSoup

## Install
```
$ pip install -r requirements.txt
```

## Usage
1. Crawl douban movie subject to ./cache/subjects
```
$ python spider.py --start 1888 --end 2016 --thread 20
```
2. change directory to ./cache/subjects, and join multi files
```
$ cd cache/subjects
$ find . -name '*.html' | xargs awk 1 > subjects.data
```
3. change directory to root, and run parser and specify file which you want to parse
```
$ cd ../../
$ python parser.py --file ./cahce/subjects/subjects.data
```
4. At last, you can see json data to the std. Also, you can redirect std to file. Use this command
```
$ python parser.py --file ./cache/subjects/subjects.data > file
```


## result
I parse HTML to JSON. If you don't like JSON, you can fork this resp, and rewrite it.
```json
{
    "playwright": "王刚 / 林黎胜 / 张家鲁 / 冯小刚",
    "language": "汉语普通话",
    "title": "天下无贼",
    "rating_num": "7.6",
    "cover": "https://img1.doubanio.com/view/movie_poster_cover/spst/public/p1910825177.jpg",
    "source_url": "https://movie.douban.com/subject/1291550/",
    "director": "冯小刚",
    "alias": "A World Without Thieves",
    "imdb_link": "tt0439884",
    "intro": "王薄（刘德华 饰）和王丽（刘若英 饰）本是一对最佳贼拍档，但因怀了王薄的孩子，王丽决定收手赎罪，两人产生分歧。在火车站遇到刚刚从城市里挣了一笔钱准备回老家用它盖房子娶媳妇的农村娃子傻根（王宝强 饰）后，王丽被他的单纯打动，决定暗中保护不使他的辛苦钱失窃，王薄却寻思找合适机会下手，但 最终因为“夫妻情深”归入了王丽的阵营。 不料傻根的钱早被以黎叔（葛优 饰）为头目的另一著名扒窃团伙盯上，于是一系列围绕傻根书包里的钞票、在王薄、王丽和黎叔团伙之间展开的强强斗争上演。",
    "actors": "刘德华 / 刘若英 / 王宝强 / 李冰冰 / 葛优 / 张涵予 / 尤勇 / 徐帆 / 傅彪 / 范伟 / 冯远征 / 林家栋",
    "year": "2004",
    "date": "2004-12-09(中国大陆/香港)",
    "regon": "中国大陆 / 香港",
    "movie_length": "113分钟 / 100分钟",
    "type": "剧情 / 动作 / 犯罪"
}
```

### English - chinese glossary of JSON key
| English Key        | Chinese Key           |
| -------------------|:---------------------:|
| playwright         | 编剧                  |
| language           | 语言                  |
| title              | 标题                  |
| rating_num         | 评分                  |
| cover              | 封面图片              |
| source_url         | 豆瓣电影源地址        |
| director           | 导演                  |
| alias              | 又名                  |
| imdb_link          | imdb 链接地址编号     |
| intro              | 电影简介              |
| actors             | 主演                  |
| year               | 上映年份              |
| date               | 上映日期              |
| regon              | 制片国家/地区         |
| movie_length       | 片长                  |
| type               | 电影类型              |


## License
The douban movie spider is licensed under the MIT license. See [License File](LICENSE) for more information.
